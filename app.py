#Importing libraries: Flask, pvlib and pandas
from flask import Flask, request, render_template
app = Flask(__name__)

import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import pandas as pd


#Function that returns content
# and use Flask's app.route decorator to map the URL route / to that function:
# Index.html is rendered
@app.route("/")
def index():
    return render_template('index.html')

#Processing input data from index.html
@app.route('/process', methods=['POST'])
def process():
    # Hier verarbeiten Sie die Daten aus dem Formular
    latitude_input = request.form['latitude_input']
    longitude_input = request.form['longitude_input']
    surface_tilt_input = request.form['surface_tilt_input']
    surface_azimuth_input = request.form['surface_azimuth_input']
    quantity = request.form['quantity']

    # Führen Sie Ihr Python-Skript aus und erhalten Sie das Ergebnis
    result = process_data(latitude_input, longitude_input, surface_tilt_input, surface_azimuth_input, quantity)

    # Geben Sie das Ergebnis an die Ergebnisseite weiter
    return render_template('result.html', result=result)

def process_data(latitude_input, longitude_input, surface_tilt_input, surface_azimuth_input, quantity):

    #latitude_input = 50.94138776328743
    #longitude_input = 6.958524886753683
    #surface_tilt_input = 45
    #surface_azimuth_input = 180
    float(latitude_input)
    float(longitude_input)
    float(surface_azimuth_input)
    float(surface_tilt_input)
    int(quantity)

    #Create an instance of Location Class
    location = Location(latitude = latitude_input, longitude = longitude_input, tz='Europe/Berlin', altitude = 80, name = 'Cologne Cathedral')

    # Set PV modules and inverters databases
    sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
    cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

    # Set modules and inverters
    module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
    inverter = cec_inverters['ABB__PVI_3_0_OUTD_S_US__208V_']

    # Set temperature parameters by temperature data provided by pvlib
    temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

    #Gettig irrad data from PVGIS
    poa_data_2020, meta, inputs = pvlib.iotools.get_pvgis_hourly(latitude=latitude_input, longitude=longitude_input, start=2020, end=2020, raddatabase="PVGIS-SARAH2", components=True, 
                                                    surface_tilt=surface_tilt_input, surface_azimuth=0, 
                                                    outputformat='json', usehorizon=True, userhorizon=None, 
                                                    pvcalculation=False, peakpower=None, pvtechchoice='crystSi', 
                                                    mountingplace='free', loss=0, trackingtype=0, 
                                                    optimal_surface_tilt=False, optimalangles=False, 
                                                    url='https://re.jrc.ec.europa.eu/api/v5_2/', map_variables=True, 
                                                    timeout=30)

    poa_data_2020['poa_diffuse'] = poa_data_2020['poa_sky_diffuse'] + poa_data_2020['poa_ground_diffuse']
    poa_data_2020['poa_global'] = poa_data_2020['poa_diffuse'] + poa_data_2020['poa_direct']

    #poa_data_2020.to_csv("poa_data_2020.csv")

    # Create an instance of PVSystem Class
    # Additionally add modules per string = wie viel Module sind in Reihe geschaltet
    # Addiotionally add strings per inverter = wie viel viele Module sind an einem Wechselumrichter?
    system = PVSystem(surface_tilt = surface_tilt_input, surface_azimuth = surface_azimuth_input, module_parameters = module, 
                    inverter_parameters = inverter, temperature_model_parameters = temperature_parameters,
                    modules_per_string = 1, strings_per_inverter = 1)

    # Create an Instance of ModelChain Class
    modelchain = ModelChain(system, location)

    #print(modelchain)

    #Combine irradiance data with modelchain to see AC output of pv system. 
    # AC = energy yield in watts behind inverter. 
    # So to say the end of your PV system which will be connected to rest of a house system

    #modelchain.run_model(clear_sky)
    #modelchain.results.ac.plot(figsize=(16,9))

    modelchain.run_model_from_poa(poa_data_2020)

    #modelchain.results.ac.plot(figsize=(16,9))

    # Summe erzeugter Strom in Watt

    kwh = (sum(modelchain.results.ac)/1000)*quantity
    return kwh

if __name__ == '__main__':
    app.run(debug=True)