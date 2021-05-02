#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 06:37:09 2020

@author: noelia
"""

################################################################################### 
##### Este algoritmo sirve para encontrar el pixel mas cercano de las estaciones ##
####  AERONET en el estado de Sao Paulo. Se exporta los datos en un excel        ## 
####  en la direccion "/dados/noelia/results/maiac_local/"                       ##
####   un analisis para varios años 2014 - 2020   
#####     despues de usar este algoritmo, utilizar el modis_aeronet.py           ##  
###################################################################################

import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import os
from datetime import datetime
import glob
import re
import pyproj
import time
import calendar


USE_GDAL = False

#open several data
INPUT_PATH = '/data/noelia/imagen_data/modis/DATA/SP/DADOS MAIAC/'
listdir = os.listdir(INPUT_PATH)
OUT_PATH = '/data/noelia/imagen_data/modis/results/maiac_local/'


sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

def jdtodatestd (jdate):
    fmt = '%Y%j%H%M'
    datestd = datetime.strptime(jdate, fmt)
    timee = datestd.strftime("%Y-%m-%d %H:%M:%S")    ### utc
    time_tuple = time.strptime(timee, "%Y-%m-%d %H:%M:%S")
    t = calendar.timegm(time_tuple)
    aa = time.localtime(t)
    time_local = time.strftime('%Y-%m-%d %H:%M:%S', aa)    ### local
    return(time_local)


def calibrate(h5):
    # Read global attribute.
    attrs = hdf.attributes(full=0)
    times = attrs['Orbit_time_stamp'].replace(' ',',').replace(',,',',').split(',')
    fattrs = hdf.attributes(full=1)
    ga = fattrs["StructMetadata.0"]
    gridmeta = ga[0]
    # Construct the grid.  The needed information is in a global attribute
    # called 'StructMetadata.0'.  Use regular expressions to tease out the
    # extents of the grid. 
    ul_regex = re.compile(r'''UpperLeftPointMtrs=\(
                              (?P<upper_left_x>[+-]?\d+\.\d+)
                              ,
                              (?P<upper_left_y>[+-]?\d+\.\d+)
                              \)''', re.VERBOSE)
    match = ul_regex.search(gridmeta)
    x0 = np.float(match.group('upper_left_x')) 
    y0 = np.float(match.group('upper_left_y')) 

    lr_regex = re.compile(r'''LowerRightMtrs=\(
                              (?P<lower_right_x>[+-]?\d+\.\d+)
                              ,
                              (?P<lower_right_y>[+-]?\d+\.\d+)
                              \)''', re.VERBOSE)
    match = lr_regex.search(gridmeta)
    x1 = np.float(match.group('lower_right_x')) 
    y1 = np.float(match.group('lower_right_y')) 
    nh, ny, nx = data.shape
    xinc = (x1 - x0) / nx
    yinc = (y1 - y0) / ny

    x = np.linspace(x0, x0 + xinc*nx, nx)
    y = np.linspace(y0, y0 + yinc*ny, ny)
    xv, yv = np.meshgrid(x, y)

    return xv,yv,times

for user_lat,user_lon,name_station in zip(sta_lat,sta_lon,station):
    for k in range(len(listdir)):
        path = INPUT_PATH+listdir[k]+'/'
        mai_path = sorted(glob.glob(path+'*.hdf'))
        time_serie = pd.DataFrame({'IP':[]})
        count = 0
        for FILE_NAME in mai_path:
            FILE_NAME=FILE_NAME.strip()
            print(FILE_NAME)
            hdf = SD(FILE_NAME, SDC.READ)
            datasets_dic = hdf.datasets()
            dat=hdf.select('Optical_Depth_055')
            attr = dat.attributes()
            FillValue = attr['_FillValue']
            scale_factor = attr['scale_factor']
            valid_range = attr['valid_range']
            add_offset = attr['add_offset']
            unit = attr['unit']
            long_name = attr['long_name']
            data = dat[:]
            
            xv,yv,times = calibrate(dat)
            
            # In basemap, the sinusoidal projection is global, so we won't use it.
            # Instead we'll convert the grid back to lat/lons.
            sinu = pyproj.Proj("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")
            wgs84 = pyproj.Proj("+init=EPSG:4326") 
            lon, lat= pyproj.transform(sinu, wgs84, xv, yv)
            min_lat=lat.min()
            max_lat=lat.max()
            min_lon=lon.min()
            max_lon=lon.max()
            print(min_lat,max_lat,min_lon,max_lon)
            #mostrar o range de lat e lon encontado no archivo
            # print("latitud minima: ",min_lat,"latitud maxima:",max_lat,'grados'+'\n'+
            #       "longitud minima:",min_lon, "longitud maxima", max_lon,'grados')
            ##Calculando os pontos mais pertos do ponto local
            R=6371000  ## Raio da terra em metros
            lat1=np.radians(user_lat)
            lat2=np.radians(lat)
            delta_lat=np.radians(lat-user_lat)
            delta_lon=np.radians(lon-user_lon)
            a=(np.sin(delta_lat/2))*(np.sin(delta_lat/2))+(np.cos(lat1))*(np.cos(lat2))*(np.sin(delta_lon/2))*(np.sin(delta_lon/2))
            c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
            d=R*c                          
            ## obter os pontos x,y do ponto local ingresado
            x,y=np.unravel_index(d.argmin(),d.shape)  # vertical, horizontal
#            print('el pixel mas cerca del punto ingresado es: Latitud:', lat[x,y], 'longitud:', lon[x,y])
            print(x,y)
            date = [jdtodatestd(times[i][0:-1]) for i in range(data.shape[0])]
            sensor = [(times[i][-1::]) for i in range(data.shape[0])]
            for n in range(data.shape[0]):
                time_serie.loc[count,'IP']=FILE_NAME[-45:-4]+sensor[n]
                time_serie.loc[count,'Time']=date[n]
                time_serie.loc[count,'year'] = date[n][0:4]
                time_serie.loc[count,'month'] = date[n][5:7]
                time_serie.loc[count,'day'] = date[n][8:10]
                time_serie.loc[count,'hour'] = date[n][11:13]
                time_serie.loc[count,'min'] = date[n][14:16]
                time_serie.loc[count,'sec'] = date[n][17:19]
                time_serie.loc[count,'distancia'] = d[x,y]
                time_serie.loc[count,'latitud'] = lat[x,y]
                time_serie.loc[count,'longitud'] = lon[x,y]                
                time_serie.loc[count,'AOD'] = round(data[n,x,y]*scale_factor + add_offset,3)
                if data[n,x,y]==FillValue:
#                    print('el valor de para este pixel es', FillValue,"""(o sea no tiene valor)""")
                    time_serie.loc[count,'AOD'] = np.nan
                else:
#                    print('el valor de para este pixel es', round(data[n,x,y]*scale_factor + add_offset,3))
                    time_serie.loc[count,'AOD'] = round(data[n,x,y]*scale_factor + add_offset,3)
                ## calculo do promedio, mediana, desvio standar do ponto alredor da grilla 3x3 do pongo local.
                if x < 1:
                    x+=1
                if x > data.shape[1]-2:
                    x-=2
                if y < 1:
                    y+=1
                if y > data.shape[2]-2:
                    y-=2
                three_by_three=data[n,x-1:x+2,y-1:y+2]
                three_by_three=three_by_three.astype(float)
                three_by_three[three_by_three==float(FillValue)]=np.nan
                nnan=np.count_nonzero(~np.isnan(three_by_three))
                time_serie.loc[count,'count 3x3'] = nnan
                if nnan==0:
#                    print('Nao tem pixeles validos numa grilla centrada de 3x3 em a localicacao dada')
                    time_serie.loc[count,'AOD 3x3 mean'] = np.nan
                    count=count+1
                else:
                    three_by_three=three_by_three*scale_factor + add_offset
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
        time_serie.to_csv(OUT_PATH+FILE_NAME[-45:-38]+'_'+str(listdir[k])+"_MAIAC_"+str(name_station)+".csv", index=False)
