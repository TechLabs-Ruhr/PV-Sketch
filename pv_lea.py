import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import matplotlib as plt
import pandas as pd
# hier müssen entsprechende Wetterdaten für die bestimmte Location extrahiert werden
# AUTOMATISCH TMY FÜR EINE BESTIMMTE LOCATION ERHALTEN
tmydata= pvlib.iotools.get_pvgis_tmy(latitude=51.478, longitude=7.223,
                                 outputformat=‘json’, usehorizon=True, userhorizon=None,
                                 startyear=None, endyear=None, map_variables=True,
                                url=‘https://re.jrc.ec.europa.eu/api/’, timeout=30)
# da nur die erste Position des Tuples der Datensatz ist den man braucht, diesen Teil in tmy speichern
tmy = pd.DataFrame(tmydata[0])
tmy.index=pd.date_range(start=“2021-01-01 00:00”, end=“2021-12-31 23:00", freq=“h”)
# unbennenen des Index mit einem ausgedachten Referenzjahr 2021
tmy = tmy.drop(‘relative_humidity’, axis=1)
tmy = tmy.drop(‘IR(h)’, axis=1)
tmy = tmy.drop(‘wind_direction’, axis=1)
tmy = tmy.drop(‘pressure’, axis=1)
tmy.index=pd.to_datetime(tmy.index)
print(tmy)
#sonneneinstrahung in Abhänigkeit von der Zeit / Winkel, Dachneigung /Ausrichtung
#tilt = Dachniegung
#azimuth = Himmelsrichtung
# location obkejt erstellen
location= pvlib.location.Location(latitude=51.478, longitude=7.223,)
times=tmy.index-pd.Timedelta(“30min”)
solar_position=location.get_solarposition(times)
solar_position.index += pd.Timedelta(“30min”)
print(solar_position)
#tilt = Dachniegung
#azimuth = Himmelsrichtung
df_gesamt=pvlib.irradiance.get_total_irradiance(surface_tilt=20,
                                                surface_azimuth=180,
                                                solar_zenith=solar_position[“apparent_zenith”],
                                                solar_azimuth=solar_position[“azimuth”],
                                                dni=tmy[“dni”], ghi=tmy[“ghi”], dhi=tmy[“dhi”])
tracker_gesamt= df_gesamt[“poa_global”]
# Was passiert wenn die Sonne auf die PV Anlage scheint? Aufheizen der Anlage hat Auswirkungen auf die Anlage
temperature_parameters=TEMPERATURE_MODEL_PARAMETERS[“sapm”][“open_rack_glass_glass”]
cell_temperature = pvlib.temperature.sapm_cell(tracker_gesamt, tmy[“temp_air”], tmy[“wind_speed”], **temperature_parameters)
#1kW array with the temperature coefficient of -0,4/Celsiusgrad
gamma_pdc=-0.004 #durch 100 dividieren um von %/Celsiusgrad auf 1/Celsiusgrad zu kommen
nameplate=1000
array_power=pvlib.pvsystem.pvwatts_dc(tracker_gesamt, cell_temperature, nameplate, gamma_pdc)
# gibt power für ein array in Watt aus
array_power.resample(“M”).plot()
print(“Die Summe der produzierten Energie beträgt: ” ,array_power.sum(), “W. Das entspricht “,array_power.sum()/1000, ” kWh.” )
SumProd= array_power.sum()/1000
Personenanzahl= 1
if Personenanzahl== 1:
    Verbrauch= 1400
elif Personenanzahl== 2:
    Verbrauch=2500
elif Personenanzahl== 3:
    Verbrauch= 3600
elif Personenanzahl==4:
    Verbrauch=4000
else: Verbrauch= 4500
Zwischensum= SumProd-Verbrauch
if Zwischensum>0:
    Verkauf= Zwischensum*0.13
    print(“Bei ihrem Verbrauch erhalten sie “, Verkauf, “€ Gewinn.“)
if  Zwischensum<0:
    Kosten= Zwischensum*0.3496
    print(“Bei ihrem Verbrauch müssen sie “, Kosten, “zahlen.“)