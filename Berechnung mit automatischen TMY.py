#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 20:43:43 2023

@author: Lea
"""

import pvlib

from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import matplotlib as plt
import pandas as pd


# hier ist eine Funktion erforderlich die die Adresse entgegennimmt und entsprechende Werte für 
# den Längen- und Breitengrad ausgibt und in den Variablen lat und long speichert

lat= 51.478
long=7.223

location = Location(lat, long, tz="Europe/Berlin", altitude=100, name="BochumHBF")
# der Name muss aus dem Input der Adresse generiert werden
#altitude=100 #Höhe der PV Anlage übder dem Meeresspiegel - Wie kommt man an die Zahl wenn man nur Adresse hat?
# timezone (tz ist fix = es wird nur Deutschland betrachet)

#hier muss das entsprechende System festgelegt werden
#erst Datenbasis auswählen
sandia_modules= pvlib.pvsystem.retrieve_sam("SandiaMod")
cec_inverters= pvlib.pvsystem.retrieve_sam("CECInverter")
#dann spezifisches System und Inverter festlegen
module=sandia_modules["Canadian_Solar_CS5P_220M___2009_"]
inverter=cec_inverters["ABB__PVI_3_0_OUTD_S_US__208V_"]

# Was passiert wenn die Sonne auf die PV Anlage scheint? Aufheizen der Anlage hat Auswirkungen auf die Anlage
temperature_parameters=TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]


InpTilt=input("Bitte Dachneigung angeben")
InpTilt=int(InpTilt)
InpAz=input("Bitte Himmelsrichtung der Ausrichtung angeben")
InpAz=int(InpAz)

system= PVSystem (surface_tilt=InpTilt, surface_azimuth=InpAz, module_parameters=module, 
                  inverter_parameters=inverter, temperature_model_parameters=temperature_parameters,
                  modules_per_string=7, strings_per_inverter=2)


modelchain= ModelChain(system, location)

# hier müssen entsprechende Wetterdaten für die Bestimmte Location extrahiert werden
# AUTOMATISCH TMY FÜR EINE BESTIMMTE LOCATION ERHALTEN

tmydata= pvlib.iotools.get_pvgis_tmy(latitude=51.478, longitude=7.223, 
                                 outputformat='json', usehorizon=True, userhorizon=None, 
                                 startyear=None, endyear=None, map_variables=True, 
                                url='https://re.jrc.ec.europa.eu/api/', timeout=30)

# da nur die erste Position des Tuples der Datensatz ist den man braucht, diesen Teil in tmy speichern
tmy = pd.DataFrame(tmydata[0])

tmy.index=pd.date_range(start="2021-01-01 00:00", end="2021-12-31 23:00", freq="h") 
# unbennenen des Index mit einem ausgedachten Referenzjahr 2021

tmy = tmy.drop('relative_humidity', axis=1)
tmy = tmy.drop('IR(h)', axis=1)
tmy = tmy.drop('wind_direction', axis=1)
tmy = tmy.drop('pressure', axis=1)

tmy.index=pd.to_datetime(tmy.index)



modelchain.run_model(tmy)
#modelchain.results.ac.plot(figsize=(16,9))
#plt.show()
print(modelchain.results.ac.sum() ) #ist das die richitge Summe?? Welche Einheit etc??

modelchain.results.ac.resample("M").sum().plot(figsize=(16,9))
plt.show()







