#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:37:03 2020

@author: noelia
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime


INPUT_AERONET_MODIS = "/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/imagen_data/modis/results/aero_maiac/"
lis_modis = os.listdir(INPUT_AERONET_MODIS)
lis_modis =sorted(lis_modis, key=str.lower)
lis_maiac = os.listdir(INPUT_AERONET_MAIAC)
lis_maiac =sorted(lis_maiac, key=str.lower)
OUTPUT = "/imagen_data/modis/results/plot_Aero_550/"

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
name = ["prom_60_min_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
distancia = [3000.0,15000.0,25000.0,50000.0]
diss = ['3km','15km','25km','50km']
marker = ["*","v","s"]
colour = ["blue","red","green"]

####################### all period (2014 - 2019) ###########################
############################# MODIS ###########################################
def modis_cor_all(OUTPUT,INPUT_AERONET_MODIS,data,city,resol,listdir,prod,prod_name):
    for n in range(len(listdir)):
        names = listdir[n][0:5]+str(prod)+'_'+str(resol)+'_MODIS'+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MODIS+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[0:5] for d in data['IP']]
    terra = data[data['satelite'] == 'MOD04'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'MYD04'].reset_index(drop=True)
    ############################### Distance #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    fig, axs = plt.subplots(4, 1,figsize=(29,25),sharex=True,sharey=True)
    plt.xlabel('TIME')
    fig.text(0.06, 0.5, 'MODIS - Terra AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for e,dd in enumerate(['D1','D2','D3','D4']):
        dt = terra[terra.loc[:,str(dd)] == str(dd)].reset_index(drop=True)
        t_subset = dt[~np.isnan(dt['AOD modis'])]
        if (len(t_subset) == 0):
            pass
        else:
            slope, intercept, r_value, p_value, std_err = np.polyfit(range(len(t_subset)),t_subset['AOD modis'],1,full=True)
            axs[e].plot(dt['Time_mod'],dt["AOD modis"],color = "black", marker = "*", markersize=15,linewidth = 3.5,label=str(prod_name))
            axs[e].plot([slope[0]*i + slope[1] for i in range(len(list(sorted(set(dt['year']))))*365)],color='red',linewidth = 3.5)
            axs[e].set_ylim(0,1.2)
            axs[e].set_xticks(np.arange(0,6*365,365))
            axs[e].set_xticklabels(list(sorted(set(dt['year']))))
            axs[e].annotate('d < '+str(diss[e]), xy=(1, 0.94), xycoords='axes fraction', fontsize=35,
                    xytext=(-5, 5), textcoords='offset points',ha='right', va='top')
    plt.legend(loc=0, prop={'size': 45},bbox_to_anchor=(1.2, 2.7),title=str(city).replace('_',' '))
    plt.savefig(OUTPUT +'/terra/tendencia_'+str(city)+'_'+str(prod)+'.png',bbox_inches='tight')
    plt.show()

    #################################  AQUA  ##################################
    fig, axs = plt.subplots(4, 1,figsize=(29,25),sharex=True,sharey=True)
    plt.xlabel('TIME')
    fig.text(0.06, 0.5, 'MODIS - Aqua AOD', ha='center', va='center', rotation='vertical')
    SMALL_SIZE = 45
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for e,dd in enumerate(['D1','D2','D3','D4']):
        da = aqua[aqua.loc[:,str(dd)] == str(dd)].reset_index(drop=True)
        t_subset = da[~np.isnan(da['AOD modis'])]
        if (len(t_subset) == 0):
            pass
        else:
            slope, intercept, r_value, p_value, std_err = np.polyfit(range(len(t_subset)),t_subset['AOD modis'],1,full=True)
            axs[e].plot(dt['Time_mod'],dt["AOD modis"],color = "black", marker = "*", markersize=15,linewidth = 3.5,label=str(prod_name))
            axs[e].plot([slope[0]*i + slope[1] for i in range(len(list(sorted(set(dt['year']))))*365)],color='red',linewidth = 3.5)
            axs[e].set_ylim(0,1.2)
            axs[e].set_xticks(np.arange(0,6*365,365))
            axs[e].set_xticklabels(list(sorted(set(dt['year']))))
            axs[e].annotate('d < '+str(diss[e]), xy=(1, 0.94), xycoords='axes fraction', fontsize=35,
                    xytext=(-5, 5), textcoords='offset points',ha='right', va='top')
    plt.legend(loc=0, prop={'size': 45},bbox_to_anchor=(1.2, 2.7),title=str(city).replace('_',' '))
    plt.savefig(OUTPUT +'/aqua/tendencia_'+str(city)+'_'+str(prod)+'.png',bbox_inches='tight')
    plt.show()


product = ['DT_AOD','DB_AOD','DT_DB_AOD','DT_AOD']
prod_name = ['DT','DB','DT-DB','DT']
resol = ['3K','L2','L2','L2']
for city in cities:
    data = pd.DataFrame()
    for r,p,pro_name in zip(resol,product,prod_name):
        modis_cor_all(OUTPUT,INPUT_AERONET_MODIS,data,city,r,lis_modis,p,pro_name)

################################ MAIAC ########################################
def maiac_all(OUTPUT,INPUT_AERONET_MAIAC,data,city,listdir,prod):
    for n in range(len(listdir)):
        names = listdir[n][0:13]+str(prod)+'_'+str(city)+'_AERONET.csv'
        if str(names) in listdir[n]:
            df = pd.read_csv(INPUT_AERONET_MAIAC+listdir[n])
            df['station'] = str(city)
            df['AOD modis'][df['AOD modis'] < 0 ] = np.nan
            data = pd.concat([data,df])
    data['year'] = [d[0:4] for d in data['Time_mod']]
    data['month'] = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b") for d in data.Time_mod]
    data['satelite'] = [d[-1::] for d in data['IP']]
    terra = data[data['satelite'] == 'T'].reset_index(drop=True)
    aqua = data[data['satelite'] == 'A'].reset_index(drop=True)
    ############################### Distance #################################
    for dist,dd in zip(distancia,['D1','D2','D3','D4']):
        terra.loc[terra.loc[:,'distancia']<=dist,str(dd)] = dd
        aqua.loc[aqua.loc[:,'distancia']<=dist,str(dd)] = dd
    #################################  TERRA  #################################
    for e,dd in enumerate(['D1','D2','D3','D4']):
        dt = terra[terra.loc[:,str(dd)] == str(dd)].reset_index(drop=True)
    t_subset = dt[~np.isnan(dt['AOD modis'])]
    if (len(t_subset) == 0):
        pass
    else:
        slope, intercept, r_value, p_value, std_err = np.polyfit(range(len(t_subset)),t_subset['AOD modis'],1,full=True)
        fig, axs = plt.subplots(1, 1,figsize=(29,17),sharex=True,sharey=True)
        plt.xlabel('TIME')
        fig.text(0.06, 0.5, 'MODIS - Terra AOD', ha='center', va='center', rotation='vertical')
        SMALL_SIZE = 45
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        axs.plot(dt['Time_mod'],dt["AOD modis"],color = "black", marker = "*", markersize=15,linewidth = 3.5,label=str('MAIAC'))
        axs.plot([slope[0]*i + slope[1] for i in range(6*365)],color='red',linewidth = 3.5)
        axs.set_ylim(0,1.0)
        axs.set_xticks(np.arange(0,6*365,365))
        axs.set_xticklabels(list(sorted(set(dt['year']))))
        axs.annotate('d < 3km', xy=(1, 0.94), xycoords='axes fraction', fontsize=40,
                xytext=(-5, 5), textcoords='offset points',ha='right', va='top')
    plt.legend(loc=0, prop={'size': 45},bbox_to_anchor=(0.3,1),title=str(city).replace('_',' '))
    plt.savefig(OUTPUT +'/terra/tendencia_'+str(city)+'_'+str(prod)+'.png',bbox_inches='tight')
    plt.show()
    
    ################################ AQUA #####################################
    for e,dd in enumerate(['D1','D2','D3','D4']):
        da = aqua.reset_index(drop=True)
    t_subset = da[~np.isnan(da['AOD modis'])]
    if (len(t_subset) == 0):
        pass
    else:
        slope, intercept, r_value, p_value, std_err = np.polyfit(range(len(t_subset)),t_subset['AOD modis'],1,full=True)
        fig, axs = plt.subplots(1, 1,figsize=(29,17),sharex=True,sharey=True)
        plt.xlabel('TIME')
        fig.text(0.06, 0.5, 'MODIS - Aqua AOD', ha='center', va='center', rotation='vertical')
        SMALL_SIZE = 45
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        axs.plot(dt['Time_mod'],dt["AOD modis"],color = "black", marker = "*", markersize=15,linewidth = 3.5,label=str('MAIAC'))
        axs.plot([slope[0]*i + slope[1] for i in range(6*365)],color='red',linewidth = 3.5)
        axs.set_ylim(0,1.0)
        axs.set_xticks(np.arange(0,6*365,365))
        axs.set_xticklabels(list(sorted(set(dt['year']))))
        axs.annotate('d < 3km', xy=(1, 0.94), xycoords='axes fraction', fontsize=40,
                xytext=(-5, 5), textcoords='offset points',ha='right', va='top')
    plt.legend(loc=0, prop={'size': 45},bbox_to_anchor=(0.3, 1),title=str(city).replace('_',' '))
    plt.savefig(OUTPUT +'/aqua/tendencia_'+str(city)+'_'+str(prod)+'.png',bbox_inches='tight')
    plt.show()

for city in ['Sao_Paulo']:
    data = pd.DataFrame()
    maiac_all(OUTPUT,INPUT_AERONET_MAIAC,data,city,lis_maiac,'MAIAC')

