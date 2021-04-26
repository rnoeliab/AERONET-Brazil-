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

INPUT_AERONET_MODIS = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod/"

listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)

OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/plot_Aero_550/modis/"

months = list(pd.date_range(start='01-01-2017',end='31-12-2017',freq='M').strftime('%b'))

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

for i in range(len(listdir)):
    print(listdir[i])
    data= pd.read_csv(INPUT_AERONET_MODIS+listdir[i])
    data['AOD modis'][data['AOD modis'] < 0 ] = np.nan
    data["prom_60_min_AOD_aero"][data["prom_60_min_AOD_aero"] < 0 ] = np.nan
    data["prom_30_min_AOD_aero"][data["prom_30_min_AOD_aero"] < 0 ] = np.nan
    data["prom_15_min_AOD_aero"][data["prom_15_min_AOD_aero"] < 0 ] = np.nan

    fig = plt.figure(figsize=(21,8)) 
    ax = fig.add_subplot(111)
    ax.plot(data['Time_mod'],data["AOD modis"],color = "black", marker = "v", linewidth = 1.5,label='MODIS')
#        ax1 = ax.twinx()
    ax.plot(data['Time_mod'],data["prom_60_min_AOD_aero"],color = "blue", marker = "*",label= '\xB1 60 min AERO')
    ax.plot(data['Time_mod'],data["prom_30_min_AOD_aero"],color = "red", marker = "s",label='\xB1 30 min AERO')
    ax.plot(data['Time_mod'],data["prom_15_min_AOD_aero"],color = "green", marker = "o",label='\xB1 15 min AERO')
    ax.axis([-1,370, -0.05,1.2])
    ax.set_xticks(months_idx)
    ax.set_xticklabels(months)
    plt.title(str(listdir[i][5:-4].replace('_','-')), size = 30)
    plt.xlabel(str(listdir[i][0:4]), size = 30)
    plt.legend(loc=0, prop={'size': 25})
    plt.xticks(size = 25)
    plt.yticks(size = 25)
    plt.ylabel("AOD", size = 25)
    plt.tight_layout()
    plt.savefig(OUTPUT +listdir[i][:-4]+'.png')
    print (OUTPUT +listdir[i])
    plt.show()

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
for i in np.arange(2014,2021,1):
    ano = list(filter(lambda a: str(i) in a,listdir))
    for c in cities:
        stn = list(filter(lambda a: str(c) in a,ano))
        if len(stn) != 0:
            fig = plt.figure(figsize=(21,8))
            ax = fig.add_subplot(111)
            for j in range(len(stn)):
                data= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
                data['AOD modis'][data['AOD modis'] < 0 ] = np.nan
                ax.plot(data['Time_mod'],data["AOD modis"],color = colors[j], marker = markers[j], linewidth = 1.5,label=producto[j])
            ax.axis([-1,370, -0.05,1.2])
            ax.set_xticks(months_idx)
            ax.set_xticklabels(months)
            plt.title("MODIS-"+str(c)+"-AERONET", size = 30)
            plt.xlabel(str(i), size = 30)
            plt.xticks(size = 25)
            plt.yticks(size = 25)
            plt.ylabel("AOD", size = 30)
            plt.tight_layout()
            plt.legend(loc=0, prop={'size': 20})
            plt.savefig(OUTPUT +str(i)+"_MODIS_"+str(c)+'_AERONET.png')
            print (OUTPUT+str(i)+"_MODIS_"+str(c)+'_AERONET.png')
            plt.show()





