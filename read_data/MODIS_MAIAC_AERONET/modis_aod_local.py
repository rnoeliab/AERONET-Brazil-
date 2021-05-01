#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 12:20:39 2018

@author: noelia
"""
###############################################################################
#####   This algorithm is used to find the closest pixel of the stations     ##
####  AERONET in the state of Sao Paulo. The data is exported and saved      ##
####      in an excel for an analysis for several years 2014 - 2020          ##
#####        after using this algorithm, use modis_aeronet.py                ## 
###############################################################################

import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import os
import time
import calendar
from datetime import datetime

#open several data
INPUT_PATH = '../imagen_data/modis/DATA/'
listdir = os.listdir(INPUT_PATH)
OUT_PATH = '../imagen_data/modis/results/mod_local/'

#sp = -23.561 ;  -46.735
#each = -23.482 ; -46.500 
#itajuba = -22.413 ; -45.452
#cachoeira = -22.689 ; -45.006 

sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

#var_name = 'AOD_550_Dark_Target_Deep_Blue_Combined'   ## (1)
#var_name = 'Optical_Depth_Land_And_Ocean'              ## (2)   
#var_name = 'Deep_Blue_Aerosol_Optical_Depth_550_Land'  ## (3)

for user_lat,user_lon,name_station in zip(sta_lat,sta_lon,station):
    for k in range(len(listdir)):    #### 3K  and 10K
        if listdir[k] == "3K":
            var_name = 'Optical_Depth_Land_And_Ocean'
            name = "DT_AOD"
            input_modis = INPUT_PATH+listdir[k]+"/"
            for ano in range(2014,2021,1):
                input_modis = INPUT_PATH+str(listdir[k])+"/"+str(ano)+"/"
                print(input_modis)
                list_mod = os.listdir(input_modis) 
                dim=len(list_mod)
                order=sorted(list_mod, key=str.lower)
                mylist=[]
                listdirr = []
                time_serie = pd.DataFrame({'IP':[]})
                for i in range(len(order)):
                    if i == (len(order)-1):
                        break;      
                    else:
                        if order[i][0:17] == order[i + 1][0:17]:
                            listdirr.append(order[i])          
                            if i == (len(order)-2):
                                listdirr.append(order[len(order)-1])
                                mylist.append(listdirr)               
                        else:
                            listdirr.append(order[i])
                            mylist.append(listdirr)
                            listdirr = []
    
                count=0
                for n in range(len(mylist)):
                    for FILE_NAME in mylist[n]:
                        FILE_NAME=FILE_NAME.strip()                                       
                        hdf = SD(input_modis+FILE_NAME, SDC.READ)
                        #get latitude and longitude
                        lat=hdf.select('Latitude')
                        latitude=lat[:]
                        min_lat=latitude.min()
                        max_lat=latitude.max()
                        lon=hdf.select('Longitude')
                        longitude=lon[:]
                        min_lon=longitude.min()
                        max_lon=longitude.max()
                        scan_time=hdf.select('Scan_Start_Time')                
                        scan_time=scan_time[:]
                    
                        # Read dataset.
                        sds_obj = hdf.select(var_name)
                        
                        #get scale factor and fill value for data field
                        attributes=sds_obj.attributes()
                        scale_factor=attributes['scale_factor']
                        fillvalue=attributes['_FillValue']
                        
                        #get SDS data
                        data= sds_obj.get()
                        
                        #mostrar o range de lat e lon encontado no archivo
                        print("latitud minima: ",min_lat,"latitud maxima:",max_lat,'grados'+'\n'+
                              "longitud minima:",min_lon, "longitud maxima", max_lon,'grados') 
                        
                        time_serie.loc[count,'IP']=FILE_NAME[:-4]
                        
                        ##Calculando os pontos mais pertos do ponto local
                        R=6371000  ## Raio da terra em metros
                        lat1=np.radians(user_lat)
                        lat2=np.radians(latitude)
                        delta_lat=np.radians(latitude-user_lat)
                        delta_lon=np.radians(longitude-user_lon)
                        a=(np.sin(delta_lat/2))*(np.sin(delta_lat/2))+(np.cos(lat1))*(np.cos(lat2))*(np.sin(delta_lon/2))*(np.sin(delta_lon/2))
                        c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
                        d=R*c                          
                        ## obter os pontos x,y do ponto local ingresado
                        x,y=np.unravel_index(d.argmin(),d.shape)  # vertical, horizontal
                        print('el pixel mas cerca del punto ingresado es: Latitud:', latitude[x,y], 'longitud:', longitude[x,y])
                        if scan_time[x,y] == 0.0:
                            scan_time[x,y] = scan_time.max()
                        time_serie.loc[count,'scan_time'] = scan_time[x,y]
#                                temp=time.gmtime(scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC')))   ### hora utc
                        temp=scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC'))   ### timestamps utc
                        time_serie.loc[count,'year'] = datetime.fromtimestamp(temp).strftime('%Y')
                        time_serie.loc[count,'month'] = datetime.fromtimestamp(temp).strftime('%m')
                        time_serie.loc[count,'day'] = datetime.fromtimestamp(temp).strftime('%d')
                        time_serie.loc[count,'hour'] = datetime.fromtimestamp(temp).strftime('%H')
                        time_serie.loc[count,'min'] = datetime.fromtimestamp(temp).strftime('%M')
                        time_serie.loc[count,'sec'] = datetime.fromtimestamp(temp).strftime('%S')
                        time_serie.loc[count,'distancia'] = d[x,y]
                        time_serie.loc[count,'latitud'] = latitude[x,y]
                        time_serie.loc[count,'longitud'] = longitude[x,y]                
                        time_serie.loc[count,'AOD'] = round(data[x,y]*scale_factor,3)
                        if data[x,y]==fillvalue:
                            print('el valor de', name, 'para este pixel es', fillvalue,"""(o sea no tiene valor)""")
                            time_serie.loc[count,'AOD'] = np.nan
                        else:
                            print('el valor de', name, 'para este pixel es', round(data[x,y]*scale_factor,3))
                            time_serie.loc[count,'AOD'] = round(data[x,y]*scale_factor,3)
                        ## calculo do promedio, mediana, desvio standar do ponto alredor da grilla 3x3 do pongo local.
                        if x < 1:
                            x+=1
                        if x > data.shape[0]-2:
                            x-=2
                        if y < 1:
                            y+=1
                        if y > data.shape[1]-2:
                            y-=2
                        three_by_three=data[x-1:x+2,y-1:y+2]
                        three_by_three=three_by_three.astype(float)
                        three_by_three[three_by_three==float(fillvalue)]=np.nan
                        nnan=np.count_nonzero(~np.isnan(three_by_three))
                        time_serie.loc[count,'count 3x3'] = nnan
                        if nnan==0:
                            print('Nao tem pixeles validos numa grilla centrada de 3x3 em a localicacao dada')
                            time_serie.loc[count,'AOD 3x3 mean'] = np.nan
                            count=count+1
                        else:
                            three_by_three=three_by_three*scale_factor
                            three_by_three_average=np.nanmean(three_by_three)
                            three_by_three_std=np.nanstd(three_by_three)
                            three_by_three_median=np.nanmedian(three_by_three)
                            if nnan==1:
                                npixels='is'
                                mpixels='pixel'
                            else:
                                npixels='are'
                                mpixels='pixels'
                            # print('there',npixels, nnan, 'válido', mpixels, 'numa grilla centrada de 3x3 em a localicacao dada')
                            # print('O valor promedio nesta grilla é:', round(three_by_three_average,3),'O valor medio nesta grilla é:', round(three_by_three_median,3), 'A desviacao estandar nesta grilla é:', round(three_by_three_std,3))
                            time_serie.loc[count,'AOD 3x3 mean'] = three_by_three_average
                            time_serie.loc[count,'AOD_std'] = three_by_three_std
                            time_serie.loc[count,'AOD_median'] = three_by_three_median
                            count=count+1
                time_serie.to_csv(OUT_PATH+FILE_NAME[10:14]+"_"+name+"_"+FILE_NAME[6:8]+"_MODIS_"+str(name_station)+".csv", index=False)

        elif listdir[k] == "10K":
            var_name =['Optical_Depth_Land_And_Ocean','AOD_550_Dark_Target_Deep_Blue_Combined','Deep_Blue_Aerosol_Optical_Depth_550_Land']
            input_modis = INPUT_PATH+listdir[k]+"/"
            for ano in range(2014,2021,1):
                input_modis = INPUT_PATH+str(listdir[k])+"/"+str(ano)+"/"
                print(input_modis)
                list_mod = os.listdir(input_modis) 
                dim=len(list_mod)
                order=sorted(list_mod, key=str.lower)
                mylist=[]
                listdirr = []
                time_serie = pd.DataFrame({'IP':[]})
                for i in range(len(order)):
                    if i == (len(order)-1):
                        break;      
                    else:
                        if order[i][0:17] == order[i + 1][0:17]:
                            listdirr.append(order[i])          
                            if i == (len(order)-2):
                                listdirr.append(order[len(order)-1])
                                mylist.append(listdirr)               
                        else:
                            listdirr.append(order[i])
                            mylist.append(listdirr)
                            listdirr = []
    
                for r in range(len(var_name)):
                    if var_name[r] == 'AOD_550_Dark_Target_Deep_Blue_Combined':
                        name = "DT_DB_AOD"
                    elif var_name[r] == 'Deep_Blue_Aerosol_Optical_Depth_550_Land':
                        name = "DB_AOD"    
                    else:
                        name = "DT_AOD"                    
        
                    count=0
                    for n in range(len(mylist)):
                        for FILE_NAME in mylist[n]:
                            FILE_NAME=FILE_NAME.strip()
                            hdf = SD(input_modis+FILE_NAME, SDC.READ)
                            #get latitude and longitude
                            lat=hdf.select('Latitude')
                            latitude=lat[:]
                            min_lat=latitude.min()
                            max_lat=latitude.max()
                            lon=hdf.select('Longitude')
                            longitude=lon[:]
                            min_lon=longitude.min()
                            max_lon=longitude.max()
                            scan_time=hdf.select('Scan_Start_Time')                
                            scan_time=scan_time[:]
                        
                            # Read dataset.
                            sds_obj = hdf.select(var_name[r])
                            
                            #get scale factor and fill value for data field
                            attributes=sds_obj.attributes()
                            scale_factor=attributes['scale_factor']
                            fillvalue=attributes['_FillValue']
                            
                            #get SDS data
                            data= sds_obj.get()
                            
                            #mostrar o range de lat e lon encontado no archivo
                            print("latitud minima: ",min_lat,"latitud maxima:",max_lat,'grados'+'\n'+
                                  "longitud minima:",min_lon, "longitud maxima", max_lon,'grados') 
                            time_serie.loc[count,'IP']=FILE_NAME[:-4]
                            
                            ##Calculando os pontos mais pertos do ponto local
                            R=6371000  ## Raio da terra em metros
                            lat1=np.radians(user_lat)
                            lat2=np.radians(latitude)
                            delta_lat=np.radians(latitude-user_lat)
                            delta_lon=np.radians(longitude-user_lon)
                            a=(np.sin(delta_lat/2))*(np.sin(delta_lat/2))+(np.cos(lat1))*(np.cos(lat2))*(np.sin(delta_lon/2))*(np.sin(delta_lon/2))
                            c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
                            d=R*c
                           
                            ## obter os pontos x,y do ponto local ingresado
                            x,y=np.unravel_index(d.argmin(),d.shape)
                            print('el pixel mas cerca del punto ingresado es: Latitud:', latitude[x,y], 'longitud:', longitude[x,y])
                            if scan_time[x,y] == 0.0:
                                scan_time[x,y] = scan_time.max()
                            time_serie.loc[count,'scan_time'] = scan_time[x,y]
    #                                temp=time.gmtime(scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC')))   ### hora utc
                            temp=scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC'))   ### timestamps utc
                            time_serie.loc[count,'year'] = datetime.fromtimestamp(temp).strftime('%Y')
                            time_serie.loc[count,'month'] = datetime.fromtimestamp(temp).strftime('%m')
                            time_serie.loc[count,'day'] = datetime.fromtimestamp(temp).strftime('%d')
                            time_serie.loc[count,'hour'] = datetime.fromtimestamp(temp).strftime('%H')
                            time_serie.loc[count,'min'] = datetime.fromtimestamp(temp).strftime('%M')
                            time_serie.loc[count,'sec'] = datetime.fromtimestamp(temp).strftime('%S')
                            time_serie.loc[count,'distancia'] = d[x,y]
                            time_serie.loc[count,'latitud'] = latitude[x,y]
                            time_serie.loc[count,'longitud'] = longitude[x,y]                
                            time_serie.loc[count,'AOD'] = round(data[x,y]*scale_factor,3)
                            if data[x,y]==fillvalue:
                                print('el valor de', name, 'para este pixel es', fillvalue,"""(o sea no tiene valor)""")
                                time_serie.loc[count,'AOD'] = np.nan
                            else:
                                print('el valor de', name, 'para este pixel es', round(data[x,y]*scale_factor,3))
                                time_serie.loc[count,'AOD'] = round(data[x,y]*scale_factor,3)
                            ## calculo do promedio, mediana, desvio standar do ponto alredor da grilla 3x3 do pongo local.
                            if x < 1:
                                x+=1
                            if x > data.shape[0]-2:
                                x-=2
                            if y < 1:
                                y+=1
                            if y > data.shape[1]-2:
                                y-=2
                            three_by_three=data[x-1:x+2,y-1:y+2]
                            three_by_three=three_by_three.astype(float)
                            three_by_three[three_by_three==float(fillvalue)]=np.nan
                            nnan=np.count_nonzero(~np.isnan(three_by_three))
                            time_serie.loc[count,'count 3x3'] = nnan
                            if nnan==0:
                                print('Nao tem pixeles validos numa grilla centrada de 3x3 em a localicacao dada')
                                time_serie.loc[count,'AOD 3x3 mean'] = np.nan
                                count=count+1
                            else:
                                three_by_three=three_by_three*scale_factor
                                three_by_three_average=np.nanmean(three_by_three)
                                three_by_three_std=np.nanstd(three_by_three)
                                three_by_three_median=np.nanmedian(three_by_three)
                                if nnan==1:
                                    npixels='is'
                                    mpixels='pixel'
                                else:
                                    npixels='are'
                                    mpixels='pixels'
                                # print('there',npixels, nnan, 'válido', mpixels, 'numa grilla centrada de 3x3 em a localicacao dada')
                                # print('O valor promedio nesta grilla é:', round(three_by_three_average,3),'O valor medio nesta grilla é:', round(three_by_three_median,3), 'A desviacao estandar nesta grilla é:', round(three_by_three_std,3))
                                time_serie.loc[count,'AOD 3x3 mean'] = three_by_three_average
                                time_serie.loc[count,'AOD_std'] = three_by_three_std
                                time_serie.loc[count,'AOD_median'] = three_by_three_median
                                count=count+1
                                
                    time_serie.to_csv(OUT_PATH+FILE_NAME[10:14]+"_"+name+"_"+FILE_NAME[6:8]+"_MODIS_"+str(name_station)+".csv", index=False)
        else:
            pass
        
