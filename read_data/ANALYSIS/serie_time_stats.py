#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:05:35 2020

@author: noelia
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

INPUT_AERONET_MODIS = "/data/noelia/imagen_data/modis/results/aero_mod/"
OUTPUT = "/data/noelia/imagen_data/modis/results/aero_mod_statis/"
listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
name = ["prom_hr_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
name1 = ["prom_60_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
marker = ["*","v","s"]
colour = ["black","red","blue"]

def select_plot(INPUT_AERONET_MODIS,OUTPUT,data,city,resol,listdir,prod):
    for n in range(len(listdir)):
        name = listdir[n][0:5]+str(prod)+'_'+str(resol)+'_MODIS'+'_'+str(city)+'_AERONET.csv'
        if str(name) in listdir[n]:
            print(listdir[n]) 
            df = pd.read_csv(INPUT_AERONET_MODIS+listdir[n])
            df['station'] = str(city)
            df['AOD_mod'][df['AOD_mod'] < 0 ] = np.nan
            df["prom_60_min_AOD_aero"][df["prom_60_min_AOD_aero"] < 0 ] = np.nan
            df["prom_30_min_AOD_aero"][df["prom_30_min_AOD_aero"] < 0 ] = np.nan
            df["prom_15_min_AOD_aero"][df["prom_15_min_AOD_aero"] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    dat_month = pd.DataFrame(data['month'].unique(),columns=['month'])
    dat_month['AOD_mod'] = [np.nanmean(data[data['month']== str(d)]['AOD_mod']) for d in dat_month['month']]
    dat_month['prom_60_min_AOD_aero'] = [np.nanmean(data[data['month']== str(d)]['prom_60_min_AOD_aero']) for d in dat_month['month']]
    dat_month['prom_30_min_AOD_aero'] = [np.nanmean(data[data['month']== str(d)]['prom_30_min_AOD_aero']) for d in dat_month['month']]
    dat_month['prom_15_min_AOD_aero'] = [np.nanmean(data[data['month']== str(d)]['prom_15_min_AOD_aero']) for d in dat_month['month']]

    fig = plt.figure(figsize=(21,8)) 
    ax = fig.add_subplot(111)
    data.plot(x='year',y='AOD_mod',color = "black", marker = "v", linewidth = 1.5, ax = ax,label='MODIS')
    data.plot(x='year',y='prom_60_min_AOD_aero',color = "blue", marker = "*", linewidth = 1.5, ax = ax,label='mean 60 min AERONET')
    data.plot(x='year',y='prom_30_min_AOD_aero',color = "red", marker = "s", linewidth = 1.5, ax = ax,label='mean 30 min AERONET')
    data.plot(x='year',y='prom_15_min_AOD_aero',color = "green", marker = "o", linewidth = 1.0, ax = ax,label='mean 15 min AERONET')
    ax.set_ylim((0,2.5))
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=25)
    plt.title("Resolution: " + str(resol)+ ", Algorithm: " + str(prod[0:-4]) + ", Station: " + str(city.replace('_',' ')), size = 30)
    plt.xlabel("Time (hourly)", size = 30)
    plt.legend(loc=0, prop={'size': 16})
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.ylabel("AOD Values", size = 30)
    plt.tight_layout()
    plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'.png')
    plt.show()  
    
    fig = plt.figure(figsize=(21,8)) 
    ax = fig.add_subplot(111)
    data.plot(x='month',y='AOD_mod',color = "black", marker = "v", linewidth = 1.5, ax = ax,label='MODIS')
    data.plot(x='month',y='prom_60_min_AOD_aero',color = "blue", marker = "*", linewidth = 1.5, ax = ax,label='mean 60 min AERONET')
    data.plot(x='month',y='prom_30_min_AOD_aero',color = "red", marker = "s", linewidth = 1.5, ax = ax,label='mean 30 min AERONET')
    data.plot(x='month',y='prom_15_min_AOD_aero',color = "green", marker = "o", linewidth = 1.0, ax = ax,label='mean 15 min AERONET')
    ax.set_ylim((0,2.5))
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=25)
    plt.title("Resolution: " + str(resol)+ ", Algorithm: " + str(prod[0:-4]) + ", Station: " + str(city.replace('_',' ')), size = 30)
    plt.xlabel("Time (monthly)", size = 30)
    plt.legend(loc=0, prop={'size': 16})
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.ylabel("AOD Values", size = 30)
    plt.tight_layout()
    plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_all_month.png')
    plt.show()     
 
    fig = plt.figure(figsize=(21,8)) 
    ax = fig.add_subplot(111)
    dat_month.plot(x='month',y='AOD_mod',color = "black", marker = "v", linewidth = 1.5, ax = ax,label='MODIS')
    dat_month.plot(x='month',y='prom_60_min_AOD_aero',color = "blue", marker = "*", linewidth = 1.5, ax = ax,label='mean 60 min AERONET')
    dat_month.plot(x='month',y='prom_30_min_AOD_aero',color = "red", marker = "s", linewidth = 1.5, ax = ax,label='mean 30 min AERONET')
    dat_month.plot(x='month',y='prom_15_min_AOD_aero',color = "green", marker = "o", linewidth = 1.0, ax = ax,label='mean 15 min AERONET')
    ax.set_ylim((0,0.5))
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=25)
    plt.title("Resolution: " + str(resol)+ ", Algorithm: " + str(prod[0:-4]) + ", Station: " + str(city.replace('_',' ')), size = 30)
    plt.xlabel("Time (monthly)", size = 30)
    plt.legend(loc=0, prop={'size': 16})
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.ylabel("AOD Values", size = 30)
    plt.tight_layout()
    plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_month.png')
    plt.show()      
     
for city in cities:
    data = pd.DataFrame()    
    select_plot(INPUT_AERONET_MODIS,OUTPUT,data,city,'3K',listdir,'DT_AOD')
    select_plot(INPUT_AERONET_MODIS,OUTPUT,data,city,'L2',listdir,'DB_AOD')
    select_plot(INPUT_AERONET_MODIS,OUTPUT,data,city,'L2',listdir,'DT_DB_AOD')
    select_plot(INPUT_AERONET_MODIS,OUTPUT,data,city,'L2',listdir,'DT_AOD')

