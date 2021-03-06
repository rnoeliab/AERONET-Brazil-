#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:17:38 2020

@author: noelia
"""

###############################################################################
###  despues de usar el maiac_aod_local y aeronet.py ya tendremos los datos  ##
###   guardados en excel. Ahora nos toca hacer una seleccion de datos para   ##
###            un intervalo de tiempo y espacio del 2014 al 2019             ##    
###############################################################################

import os
import pandas as pd
import numpy as np

INPUT_AERONET ="/data/noelia/in-situ/aeronet/AOD/"
INPUT_MAIAC = "/data/noelia/imagen_data/modis/results/maiac_local/"
OUTPUT = "/data/noelia/imagen_data/modis/results/aero_maiac/"

listdir_aero = os.listdir(INPUT_AERONET)
listdir_maiac = os.listdir(INPUT_MAIAC)
listdir_aero =sorted(listdir_aero, key=str.lower)
listdir_maiac =sorted(listdir_maiac, key=str.lower)

for m in listdir_aero:
    for n in listdir_maiac:  
        if m[0:4] in n:       ### selecciona el año  
            if m[5:-8] in n:
                print(m, n)
                aer = pd.read_csv(INPUT_AERONET+m)
                mod = pd.read_csv(INPUT_MAIAC+n)
                mod["year"] = mod["year"].astype(int).astype(str)
                mod["month"] = mod["month"].astype(int).astype(str)
                mod["day"] = mod["day"].astype(int).astype(str)
                mod["hour"] = mod["hour"].astype(int).astype(str)
                mod["min"] = mod["min"].astype(int).astype(str)
                mod["sec"] = mod["sec"].astype(int).astype(str)
                for i in range(len(mod)):
                    mod["day"][i] = mod["day"][i].zfill(2)
                    mod["month"][i] = mod["month"][i].zfill(2)
                    mod["hour"][i] = mod["hour"][i].zfill(2)
                    mod["min"][i] = mod["min"][i].zfill(2)
                    mod["sec"][i] = mod["sec"][i].zfill(2)
                modis = mod.sort_values(by=['month','day'], ascending=True)
                modis = modis.reset_index()
                modis = modis.drop(['index'], axis=1)

                data = pd.DataFrame(modis["IP"])
                for j in range(len(modis)):
                    data.loc[j, "latitud"] = modis["latitud"][j]
                    data.loc[j, "longitud"] = modis["longitud"][j]
                    data.loc[j, "distancia"] = modis["distancia"][j]                    
                    data.loc[j, "count 3x3"] = modis["count 3x3"][j]                    
                    data.loc[j,"Time_mod"] = modis["year"][j] + "-" + modis["month"][j] + "-" + modis["day"][j]
                    data.loc[j,"hr_mod"] = modis["hour"][j] + ":"+modis["min"][j]+":"+modis["sec"][j]

                    data.loc[j, "AOD modis"] = modis["AOD"][j]
                    data.loc[j, "AOD 3x3 mean"] = modis["AOD 3x3 mean"][j]
                    data.loc[j, "AOD_std"] = modis["AOD_std"][j]
                    data.loc[j, "AOD_median"] = modis["AOD_median"][j]              
            
                    date_aer = []
                    minu_30_aer = []
                    minu_15_aer = []
                    for k in range(len(aer)):
                        ####  agrupando por dia
                        if (modis["year"][j]+"-"+modis["month"][j]+"-"+modis["day"][j] == aer["Date(dd:mm:yyyy)"][k][6:10]+"-"+aer["Date(dd:mm:yyyy)"][k][3:5]+"-"+aer["Date(dd:mm:yyyy)"][k][0:2]):                                               
                            print("mismo dia:", modis["day"][j] + "-" + modis["month"][j] + "-" + modis["year"][j])
                            ### agrupando por hora
                            cal = (float(modis["hour"][j])*60+float(modis["min"][j])) - (float(aer["Time(hh:mm:ss)"][k][0:2])*60+float(aer["Time(hh:mm:ss)"][k][3:5]))
                            if -60 <= cal and cal <=60:
                                print('menor a +-60 min')
                                date_aer.append(aer["AOD_550nm-AOD"][k])
                                data.loc[j,"time_+-60_min_aero"] = aer["Time(hh:mm:ss)"][k]
                            prom = np.nanmean(date_aer)
                            data.loc[j, "prom_60_min_AOD_aero"] = prom
                            #### agrupando por 30 minutos
                            if -30<=cal and cal<=30:
                                print('menor a +-30 min')
                                minu_30_aer.append(aer["AOD_550nm-AOD"][k])
                                data.loc[j,"time_+-30_min_aero"] = aer["Time(hh:mm:ss)"][k]
                            prom_30_minu = np.nanmean(minu_30_aer)
                            data.loc[j, "prom_30_min_AOD_aero"] = prom_30_minu
                            #### agrupando por 15 minutos
                            if -15<=cal and cal<=15:
                                print('menor a +-15 min')
                                minu_15_aer.append(aer["AOD_550nm-AOD"][k])
                                data.loc[j,"time_+-15_min_aero"] = aer["Time(hh:mm:ss)"][k]
                            prom_15_minu = np.nanmean(minu_15_aer)
                            data.loc[j, "prom_15_min_AOD_aero"] = prom_15_minu
                data['AOD modis'][data['AOD modis']<0.0] = np.nan
                data['AOD 3x3 mean'][data['AOD 3x3 mean']<0.0] = np.nan
#                aa["Date(dd:mm:yyyy)"] = aa["Date(dd:mm:yyyy)"].replace({':':'-'}, regex=True)
                data.to_csv(OUTPUT+n[0:-4] + "_AERONET.csv", index=None)           
            else:
                pass                                
        else:
            pass
