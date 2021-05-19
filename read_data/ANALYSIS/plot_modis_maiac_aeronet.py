#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 19:16:21 2019

@author: noelia
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

INPUT_AERONET_MODIS = "/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/imagen_data/modis/results/aero_maiac/"

listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)
listdir1 = os.listdir(INPUT_AERONET_MAIAC)
listdir1 =sorted(listdir1, key=str.lower)
OUTPUT = "/imagen_data/modis/results/plot_Aero_550/"

months = list(pd.date_range(start='01-01-2017',end='31-12-2017',freq='M').strftime('%b'))

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
distancia = [3000.0,15000.0,25000.0,50000.0]
diss = ['3km','15km','25km','50km']
producto = ['DB-L2','DT-3K','DT-L2','DT-DB-L2']
colors = ['dimgray','black','black','darkgray']
markers = ['s','v','d','s']
lmonths = [0,2,4,6,7,9,11]
smonths = [3,5,8,10]
months_idx = list()
idx = -15
for jj in range(len(months)):
    if jj in lmonths:
        idx+=31
        months_idx.append(idx)
    elif jj in smonths:
        idx+=30
        months_idx.append(idx)
    elif jj == 1:
        idx+=28
        months_idx.append(idx)

for i in range(len(listdir1)):
    print(str(listdir1[i]))
    ano = list(filter(lambda a: str(listdir1[i][8:12]) in a,listdir))
    stn = list(filter(lambda a: str(listdir1[i][19:-4]) in a,ano))
    print(stn)
    ################################# MAIAC ###################################
    data1= pd.read_csv(INPUT_AERONET_MAIAC+listdir1[i])
    data1['AOD modis'][data1['AOD modis'] < 0 ] = np.nan
    data1["prom_60_min_AOD_aero"][data1["prom_60_min_AOD_aero"] < 0 ] = np.nan
    data1["prom_30_min_AOD_aero"][data1["prom_30_min_AOD_aero"] < 0 ] = np.nan
    data1["prom_15_min_AOD_aero"][data1["prom_15_min_AOD_aero"] < 0 ] = np.nan
    data1['satelite'] = [d[-1::] for d in data1['IP']]
    terra1 = data1[data1['satelite'] == 'T'].reset_index(drop=True)
    aqua1 = data1[data1['satelite'] == 'A'].reset_index(drop=True)
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra1.loc[terra1.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua1.loc[aqua1.loc[:,'distancia']<=dist,str(dd)] = dd
    #################################  TERRA  #################################
    fig, axs = plt.subplots(1, 1,figsize=(29,17),sharex=True,sharey=True)
    
    plt.xlabel('TIME ('+str(listdir1[i][8:12])+')')
    fig.text(0.06, 0.5, 'MODIS - Terra AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    dt = terra1
    axs.scatter(dt['Time_mod'],dt["AOD modis"],c = "m", marker = "*", s=270,label='MAIAC')
    axs.scatter(dt['Time_mod'],dt["prom_60_min_AOD_aero"],c = "blue", marker = "o", s=100,label= '\xB1 60 min AERO')
    axs.scatter(dt['Time_mod'],dt["prom_30_min_AOD_aero"],c = "red", marker = "o", s=100,label='\xB1 30 min AERO')
    axs.scatter(dt['Time_mod'],dt["prom_15_min_AOD_aero"],c = "green", marker = "o", s=100,label='\xB1 15 min AERO')
    axs.axis([-1,370,0,1.0])
    axs.set_xticks(months_idx)
    axs.set_xticklabels(months)
    axs.text(340,0.7,'D = '+str(round(dt["distancia"][0],2)),size=45,ha='center')
    axs.text(340,0.6,'n = '+str(len(dt["AOD modis"][~np.isnan(dt["AOD modis"])])),size=45,ha='center')
    for axis in ['top','bottom','left','right']:
        axs.spines[axis].set_linewidth(3.0)
    l=plt.legend(loc=0, prop={'size': 40},bbox_to_anchor=(1.3, 0.7))
    l.set_title(str(listdir1[i][19:-12]).replace('_',' '), prop = {'size':40,'weight':'bold'})
    plt.savefig(OUTPUT +'/terra/'+listdir1[i][:-4]+'.png',bbox_inches='tight')
    print (OUTPUT +listdir1[i])
    plt.show()

    #################################  AQUA  ##################################
    fig, axs = plt.subplots(1, 1,figsize=(29,17),sharex=True,sharey=True)
    plt.xlabel('TIME ('+str(listdir1[i][8:12])+')')
    fig.text(0.06, 0.5, 'MODIS - Aqua AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    da = aqua1
    axs.scatter(da['Time_mod'],da["AOD modis"],c = "m", marker = "*", s=270,label='MAIAC')
    axs.scatter(da['Time_mod'],da["prom_60_min_AOD_aero"],c = "blue", marker = "o", s=100,label= '\xB1 60 min AERO')
    axs.scatter(da['Time_mod'],da["prom_30_min_AOD_aero"],c = "red", marker = "o", s=100,label='\xB1 30 min AERO')
    axs.scatter(da['Time_mod'],da["prom_15_min_AOD_aero"],c = "green", marker = "o", s=100,label='\xB1 15 min AERO')
    axs.axis([-1,370,0,1.0])
    axs.set_xticks(months_idx)
    axs.set_xticklabels(months)
    axs.text(340,0.7,'D = '+str(round(da["distancia"][0],2)),size=45,ha='center')
    axs.text(340,0.6,'n = '+str(len(da["AOD modis"][~np.isnan(da["AOD modis"])])),size=45,ha='center')
    for axis in ['top','bottom','left','right']:
        axs.spines[axis].set_linewidth(3.0)
    l=plt.legend(loc=0, prop={'size': 40},bbox_to_anchor=(1.3, 0.7))
    l.set_title(str(listdir1[i][19:-12]).replace('_',' '), prop = {'size':40,'weight':'bold'})
    plt.savefig(OUTPUT +'/aqua/'+listdir1[i][:-4]+'.png',bbox_inches='tight')
    print (OUTPUT +listdir1[i])
    plt.show()

    ################################# MODIS ###################################
    fig, axs = plt.subplots(4, 1,figsize=(29,22),sharex=True,sharey=True)
    plt.xlabel('TIME ('+str(listdir1[i][8:12])+')')
    fig.text(0.06, 0.5, 'MODIS - Terra AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    num = []
    for e,dd in enumerate(['D1','D2','D3','D4']):
        for j in range(len(stn)):
            data= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            data['AOD modis'][data['AOD modis'] < 0 ] = np.nan
            data['satelite'] = [d[0:5] for d in data['IP']]
            terra = data[data['satelite'] == 'MOD04'].reset_index(drop=True)
            for dist,ddd in zip(distancia,['D1','D2','D3','D4']):
                terra.loc[terra.loc[:,'distancia']<=dist,str(ddd)] = ddd
    #################################  TERRA  #################################
            dt = terra[terra.loc[:,str(dd)] == str(dd)]
            num.append(len(dt[str(dd)][~dt[str(dd)].isnull()]))
            axs[e].scatter(dt['Time_mod'],dt["AOD modis"],c = colors[j], marker = "*", s=270,label=str(producto[j]))
        axs[e].scatter(dt['Time_mod'],dt["prom_60_min_AOD_aero"],c = "blue", marker = "o", s=150,label= '\xB1 60 min AERO')
        axs[e].scatter(dt['Time_mod'],dt["prom_30_min_AOD_aero"],c = "red", marker = "o", s=150,label='\xB1 30 min AERO')
        axs[e].scatter(dt['Time_mod'],dt["prom_15_min_AOD_aero"],c = "green", marker = "o", s=150,label='\xB1 15 min AERO')
        axs[e].axis([-1,370,0,1.0])
        axs[e].set_xticks(months_idx)
        axs[e].set_xticklabels(months)
        axs[e].text(340,0.8,'d < '+str(diss[e]),size=35,ha='center')
        axs[e].text(340,0.65,'L2: (n = '+str(num[e*len(stn)])+")",size=35,ha='center')
        axs[e].text(340,0.45,'3K: (n = '+str(num[e*len(stn)+1])+")",size=35,ha='center')
        for axis in ['top','bottom','left','right']:
            axs[e].spines[axis].set_linewidth(3.0)
    l=plt.legend(loc=0, prop={'size': 40},bbox_to_anchor=(1.3, 2.7))
    l.set_title(str(listdir1[i][19:-12]).replace('_',' '), prop = {'size':40,'weight':'bold'})
    plt.savefig(OUTPUT +'/terra/'+'MOD04_'+listdir1[i][8:13]+listdir1[i][19:-4]+'.png',bbox_inches='tight')
    print (OUTPUT +listdir1[i])
    plt.show()

    fig, axs = plt.subplots(4, 1,figsize=(29,22),sharex=True,sharey=True)
    plt.xlabel('TIME ('+str(listdir1[i][8:12])+')')
    fig.text(0.06, 0.5, 'MODIS - Aqua AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    num = []
    for e,dd in enumerate(['D1','D2','D3','D4']):
        for j in range(len(stn)):
            data= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            data['AOD modis'][data['AOD modis'] < 0 ] = np.nan
            data['satelite'] = [d[0:5] for d in data['IP']]
            aqua = data[data['satelite'] == 'MYD04'].reset_index(drop=True)
            for dist,ddd in zip(distancia,['D1','D2','D3','D4']):
                aqua.loc[aqua.loc[:,'distancia']<=dist,str(ddd)] = ddd
    #################################  AQUA  ##################################
            da = aqua[aqua.loc[:,str(dd)] == str(dd)]           
            num.append(len(da[str(dd)][~da[str(dd)].isnull()]))
            axs[e].scatter(da['Time_mod'],da["AOD modis"],c = colors[j], marker = "*", s=270,label=str(producto[j]))
        axs[e].scatter(da['Time_mod'],da["prom_60_min_AOD_aero"],c = "blue", marker = "o", s=100,label= '\xB1 60 min AERO')
        axs[e].scatter(da['Time_mod'],da["prom_30_min_AOD_aero"],c = "red", marker = "o", s=100,label='\xB1 30 min AERO')
        axs[e].scatter(da['Time_mod'],da["prom_15_min_AOD_aero"],c = "green", marker = "o", s=100,label='\xB1 15 min AERO')
        axs[e].axis([-1,370,0,1.0])
        axs[e].set_xticks(months_idx)
        axs[e].set_xticklabels(months)
        axs[e].text(340,0.8,'d < '+str(diss[e]),size=35,ha='center')
        axs[e].text(340,0.65,'L2: (n = '+str(num[e*len(stn)])+")",size=35,ha='center')
        axs[e].text(340,0.45,'3K: (n = '+str(num[e*len(stn)+1])+")",size=35,ha='center')
        for axis in ['top','bottom','left','right']:
            axs[e].spines[axis].set_linewidth(3.0)
    l=plt.legend(loc=0, prop={'size': 40},bbox_to_anchor=(1.3, 2.7))
    l.set_title(str(listdir1[i][19:-12]).replace('_',' '), prop = {'size':40,'weight':'bold'})
    plt.savefig(OUTPUT +'/aqua/'+'MYD04_'+listdir1[i][8:13]+listdir1[i][19:-4]+'.png',bbox_inches='tight')
    print (OUTPUT +listdir1[i])
    plt.show()


