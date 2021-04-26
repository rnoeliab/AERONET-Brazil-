#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 20:42:06 2020

@author: noelia
"""

###############################################################################
# Este script esta hecho para calcular la correlacion entre los datos MODIS y #
# AERONET para tres productos DT, DB y MAIAC con tres resoluciones diferentes #
# 10km, 3km y 1km para todo el periodo y dividido en temporadas.              #
###############################################################################

import os
import numpy as np
import pandas as pd
import datetime
from scipy import stats

INPUT_AERONET_MODIS = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_maiac/"
lis_modis = os.listdir(INPUT_AERONET_MODIS)
lis_modis =sorted(lis_modis, key=str.lower)
lis_maiac = os.listdir(INPUT_AERONET_MAIAC)
lis_maiac =sorted(lis_maiac, key=str.lower)

OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod_statis/estadistica/"

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
name = ["prom_60_min_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
distancia = [3000.0,15000.0,25000.0,50000.0]
####################### TODO EL PERIODO 2014 - 2019 ###########################
############################# MODIS ###########################################
def modis_all(INPUT_AERONET_MODIS,data,city,resol,listdir,prod):
    for n in range(len(listdir)):
        names = listdir[n][0:5]+str(prod)+'_'+str(resol)+'_MODIS'+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MODIS+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            df["prom_60_min_AOD_aero"][df["prom_60_min_AOD_aero"] < 0 ] = np.nan
            df["prom_30_min_AOD_aero"][df["prom_30_min_AOD_aero"] < 0 ] = np.nan
            df["prom_15_min_AOD_aero"][df["prom_15_min_AOD_aero"] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[0:5] for d in data['IP']]
    terra = data[data['satelite'] == 'MOD04'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'MYD04'].reset_index(drop=True)
    ############################### Distancia #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    ###################### calculo de la correlacion ########################
    num_t = []
    corre_terra = []
    for dd in ['D1','D2','D3','D4']:
        dt = terra[terra.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
            X = t_subset[str(name[w])]
            Y = t_subset["AOD modis"]
            num_t.append(len(t_subset))
            if (len(t_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                corre_terra.append(r_value)
    num_a = []
    corre_aqua = []
    for dd in ['D1','D2','D3','D4']:
        da = aqua[aqua.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            a_subset = da.dropna(subset=['AOD modis',str(name[w])])
            X = a_subset[str(name[w])]
            Y = a_subset["AOD modis"]
            num_a.append(len(a_subset))
            if (len(a_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                corre_aqua.append(r_value)
#    return dt,da
    return corre_terra,corre_aqua,num_t,num_a

count = 0
data_corre = pd.DataFrame({'station':[]})
product = ['DT_AOD','DB_AOD','DT_DB_AOD','DT_AOD']
resol = ['3K','L2','L2','L2']
for city in cities:
    data = pd.DataFrame()
    for r,p in zip(resol,product):
        cor_t,cor_a,t_n,a_n = modis_all(INPUT_AERONET_MODIS,data,city,r,lis_modis,p)
        suma = 0
        for dd in ['D1','D2','D3','D4']:
            data_corre.loc[count,'station'] = city
            data_corre.loc[count,'resolution'] = r
            data_corre.loc[count,'producto'] = p
            data_corre.loc[count,'distancia'] = dd
            for w in range(3):
                data_corre.loc[count,'Terra_'+str(name[w][5:7])] = cor_t[suma]
                data_corre.loc[count,'count Terra_'+str(name[w][5:7])] = t_n[suma]
                data_corre.loc[count,'Aqua_'+str(name[w][5:7])] = cor_a[suma]
                data_corre.loc[count,'Count Aqua_'+str(name[w][5:7])] = a_n[suma]
                suma = suma + 1
            count = count + 1
data_corre.to_csv(OUTPUT+"tabla_correlacion_MODIS_all_dist.csv", index=False)
        
################################ MAIAC ########################################
def maiac_all(INPUT_AERONET_MAIAC,data,city,listdir,prod):
    for n in range(len(listdir)):
        names = listdir[n][0:13]+str(prod)+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MAIAC+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            df["prom_60_min_AOD_aero"][df["prom_60_min_AOD_aero"] < 0 ] = np.nan
            df["prom_30_min_AOD_aero"][df["prom_30_min_AOD_aero"] < 0 ] = np.nan
            df["prom_15_min_AOD_aero"][df["prom_15_min_AOD_aero"] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[-1::] for d in data['IP']]
    terra = data[data['satelite'] == 'T'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'A'].reset_index(drop=True)
    ############################### Distancia #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    ######################## calculo de la correlacion ########################
    num_t = []
    corre_terra = []
    for dd in ['D1','D2','D3','D4']:
        dt = terra[terra.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
            X = t_subset[str(name[w])]
            Y = t_subset["AOD modis"]
            num_t.append(len(t_subset))
            if (len(t_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                corre_terra.append(r_value)
    num_a = []
    corre_aqua = []
    for dd in ['D1','D2','D3','D4']:
        da = aqua[aqua.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            a_subset = da.dropna(subset=['AOD modis',str(name[w])])
            X = a_subset[str(name[w])]
            Y = a_subset["AOD modis"]
            num_a.append(len(a_subset))
            if (len(a_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                corre_aqua.append(r_value)
    return corre_terra,corre_aqua,num_t,num_a


count = 0
data_corre = pd.DataFrame({'station':[]})
for city in cities:
    data = pd.DataFrame()
    cor_t,cor_a,t_n,a_n = maiac_all(INPUT_AERONET_MAIAC,data,city,lis_maiac,'MAIAC')
    suma = 0
    for dd in ['D1','D2','D3','D4']:
        data_corre.loc[count,'station'] = city
        data_corre.loc[count,'producto'] = 'MAIAC'
        data_corre.loc[count,'distancia'] = dd
        for w in range(3):
            data_corre.loc[count,'Terra_'+str(name[w][5:7])] = cor_t[w]
            data_corre.loc[count,'count Terra_'+str(name[w][5:7])] = t_n[w]
            data_corre.loc[count,'Aqua_'+str(name[w][5:7])] = cor_a[w]
            data_corre.loc[count,'Count Aqua_'+str(name[w][5:7])] = a_n[w]
            suma = suma + 1
        count = count + 1
data_corre.to_csv(OUTPUT+"tabla_correlacion_MAIAC_all_dist.csv", index=False)

############################### POR TEMPORADA #################################
sumer = ['Dec','Jan','Feb']
fall = ['Mar','Apr','May']
winter = ['Jun','Jul','Aug']
spring = ['Sep','Oct','Nov']
############################# MODIS ###########################################
def modis_temporada(INPUT_AERONET_MODIS,data,city,resol,listdir,prod):
    for n in range(len(listdir)):
        names = listdir[n][0:5]+str(prod)+'_'+str(resol)+'_MODIS'+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MODIS+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            df["prom_60_min_AOD_aero"][df["prom_60_min_AOD_aero"] < 0 ] = np.nan
            df["prom_30_min_AOD_aero"][df["prom_30_min_AOD_aero"] < 0 ] = np.nan
            df["prom_15_min_AOD_aero"][df["prom_15_min_AOD_aero"] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[0:5] for d in data['IP']]
    terra = data[data['satelite'] == 'MOD04'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'MYD04'].reset_index(drop=True)
    ######################### SEPARAR POR TEMPORADA ###########################
    for s,f,w,sp in zip(sumer,fall,winter,spring):
        terra.loc[terra.loc[:,'month']==str(s),'temporada'] = 'DJF'
        terra.loc[terra.loc[:,'month']==str(f),'temporada'] = 'MAM'
        terra.loc[terra.loc[:,'month']==str(w),'temporada'] = 'JJA'
        terra.loc[terra.loc[:,'month']==str(sp),'temporada'] = 'SON'

    for s,f,w,sp in zip(sumer,fall,winter,spring):
        aqua.loc[aqua.loc[:,'month']==str(s),'temporada'] = 'DJF'
        aqua.loc[aqua.loc[:,'month']==str(f),'temporada'] = 'MAM'
        aqua.loc[aqua.loc[:,'month']==str(w),'temporada'] = 'JJA'
        aqua.loc[aqua.loc[:,'month']==str(sp),'temporada'] = 'SON'
    ############################### Distancia #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    ####################### calculo de la correlacion #########################
    num_t = []
    corre_terra = []
    for dd in ['D1','D2','D3','D4']:
        for temp in ['DJF','MAM','JJA','SON']:
            for w in range(3):
                t_subset = terra.loc[(terra.loc[:,'temporada'] == str(temp))&(terra.loc[:,str(dd)] == str(dd))].dropna(subset=['AOD modis',str(name[w])])
                X = t_subset[str(name[w])]
                Y = t_subset["AOD modis"]
                num_t.append(len(t_subset))
                if (len(t_subset) == 0):
                    corre_terra.append('nan')
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    corre_terra.append(r_value)
    num_a = []
    corre_aqua = []
    for dd in ['D1','D2','D3','D4']:
        for temp in ['DJF','MAM','JJA','SON']:
            for w in range(3):
                a_subset = aqua.loc[(aqua.loc[:,'temporada'] == str(temp))&(aqua.loc[:,str(dd)] == str(dd))].dropna(subset=['AOD modis',str(name[w])])
                X = a_subset[str(name[w])]
                Y = a_subset["AOD modis"]
                num_a.append(len(a_subset))
                if (len(a_subset) == 0):
                    corre_aqua.append('nan')
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    corre_aqua.append(r_value)
    return corre_terra,corre_aqua,num_t,num_a


count = 0
data_corre = pd.DataFrame({'station':[]})
product = ['DT_AOD','DB_AOD','DT_DB_AOD','DT_AOD']
resol = ['3K','L2','L2','L2']
for city in cities:
    data = pd.DataFrame()
    for r,p in zip(resol,product):
        cor_t,cor_a,t_n,a_n = modis_temporada(INPUT_AERONET_MODIS,data,city,r,lis_modis,p)
        suma = 0
        for dd in ['D1','D2','D3','D4']:
            for temp in ['DJF','MAM','JJA','SON']:
                for w in range(3):
                    data_corre.loc[count,'station'] = city
                    data_corre.loc[count,'resolution'] = r
                    data_corre.loc[count,'producto'] = p
                    data_corre.loc[count,'temporada'] = temp
                    data_corre.loc[count,'distancia'] = dd
                    data_corre.loc[count,'Terra_'+str(name[w][5:7])] = cor_t[suma]
                    data_corre.loc[count,'count Terra_'+str(name[w][5:7])] = t_n[suma]
                    data_corre.loc[count,'Aqua_'+str(name[w][5:7])] = cor_a[suma]
                    data_corre.loc[count,'Count Aqua_'+str(name[w][5:7])] = a_n[suma]
                    suma = suma + 1
                count = count + 1
data_corre.to_csv(OUTPUT+"tabla_correlacion_MODIS_temp_dist.csv", index=False)

################################ MAIAC ########################################
def maiac_temporada(INPUT_AERONET_MAIAC,data,city,listdir,prod):
    for n in range(len(listdir)):
        names = listdir[n][0:13]+str(prod)+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MAIAC+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            df["prom_60_min_AOD_aero"][df["prom_60_min_AOD_aero"] < 0 ] = np.nan
            df["prom_30_min_AOD_aero"][df["prom_30_min_AOD_aero"] < 0 ] = np.nan
            df["prom_15_min_AOD_aero"][df["prom_15_min_AOD_aero"] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[-1::] for d in data['IP']]
    terra = data[data['satelite'] == 'T'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'A'].reset_index(drop=True)
    ######################### SEPARAR POR TEMPORADA ###########################
    for s,f,w,sp in zip(sumer,fall,winter,spring):
        terra.loc[terra.loc[:,'month']==str(s),'temporada'] = 'DJF'
        terra.loc[terra.loc[:,'month']==str(f),'temporada'] = 'MAM'
        terra.loc[terra.loc[:,'month']==str(w),'temporada'] = 'JJA'
        terra.loc[terra.loc[:,'month']==str(sp),'temporada'] = 'SON'

    for s,f,w,sp in zip(sumer,fall,winter,spring):
        aqua.loc[aqua.loc[:,'month']==str(s),'temporada'] = 'DJF'
        aqua.loc[aqua.loc[:,'month']==str(f),'temporada'] = 'MAM'
        aqua.loc[aqua.loc[:,'month']==str(w),'temporada'] = 'JJA'
        aqua.loc[aqua.loc[:,'month']==str(sp),'temporada'] = 'SON'
    ############################### Distancia #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    ####################### calculo de la correlacion #########################
    num_t = []
    corre_terra = []
    for dd in ['D1','D2','D3','D4']:
        for temp in ['DJF','MAM','JJA','SON']:
            for w in range(3):
                t_subset = terra.loc[(terra.loc[:,'temporada'] == str(temp))&(terra.loc[:,str(dd)] == str(dd))].dropna(subset=['AOD modis',str(name[w])])
                X = t_subset[str(name[w])]
                Y = t_subset["AOD modis"]
                num_t.append(len(t_subset))
                if (len(t_subset) == 0):
                    corre_terra.append('nan')
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    corre_terra.append(r_value)
    num_a = []
    corre_aqua = []
    for dd in ['D1','D2','D3','D4']:
        for temp in ['DJF','MAM','JJA','SON']:
            for w in range(3):
                a_subset = aqua.loc[(aqua.loc[:,'temporada'] == str(temp))&(aqua.loc[:,str(dd)] == str(dd))].dropna(subset=['AOD modis',str(name[w])])
                X = a_subset[str(name[w])]
                Y = a_subset["AOD modis"]
                num_a.append(len(a_subset))
                if (len(a_subset) == 0):
                    corre_aqua.append('nan')
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    corre_aqua.append(r_value)
    return corre_terra,corre_aqua,num_t,num_a

count = 0
data_corre = pd.DataFrame({'station':[]})
for city in cities:
    data = pd.DataFrame()
    cor_t,cor_a,t_n,a_n = maiac_temporada(INPUT_AERONET_MAIAC,data,city,lis_maiac,'MAIAC')
    suma = 0
    for dd in ['D1','D2','D3','D4']:
        for n,temp in enumerate(['DJF','MAM','JJA','SON']):
            for w in range(3):
                data_corre.loc[count,'station'] = city
                data_corre.loc[count,'producto'] = 'MAIAC'
                data_corre.loc[count,'temporada'] = temp
                data_corre.loc[count,'distancia'] = dd
                data_corre.loc[count,'Terra_'+str(name[w][5:7])] = cor_t[suma]
                data_corre.loc[count,'count Terra_'+str(name[w][5:7])] = t_n[suma]
                data_corre.loc[count,'Aqua_'+str(name[w][5:7])] = cor_a[suma]
                data_corre.loc[count,'Count Aqua_'+str(name[w][5:7])] = a_n[suma]
                suma = suma + 1
            count = count + 1
data_corre.to_csv(OUTPUT+"tabla_correlacion_MAIAC_temp_dist.csv", index=False)


