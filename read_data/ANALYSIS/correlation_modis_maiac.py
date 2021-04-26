#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:03:34 2020

@author: noelia
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from matplotlib import path
import matplotlib
from sklearn.metrics import mean_squared_error

INPUT_AERONET_MODIS = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_maiac/"

lis_modis = os.listdir(INPUT_AERONET_MODIS)
lis_modis =sorted(lis_modis, key=str.lower)
lis_maiac = os.listdir(INPUT_AERONET_MAIAC)
lis_maiac =sorted(lis_maiac, key=str.lower)

OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod_statis/estadistica/figures/correlation/"

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
name = ["prom_60_min_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
distancia = [3000.0,15000.0,25000.0,50000.0]
marker = ["*","v","s"]
colour = ["blue","red","green"]
diss = ['3km','15km','25km','50km']

def MB(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    mb = np.nanmean(diff)
    return mb

def ME(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    me = np.nanmean(diff)
    return me

####################### TODO EL PERIODO 2014 - 2019 ###########################
############################# MODIS ###########################################
def modis_cor_all(OUTPUT,INPUT_AERONET_MODIS,data,city,resol,listdir,prod,prod_name):
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
    #################################  TERRA  #################################
    fig, axs = plt.subplots(3, 4,figsize=(29,17),sharex=True,sharey=True)
    for ax in axs.flat:
        ax.set(xlabel='AERONET AOD', ylabel= str(prod_name)+'-'+str(resol)+' Terra AOD')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    SMALL_SIZE = 28
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for e,dd in enumerate(['D1','D2','D3','D4']):
        dt = terra[terra.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
            X = t_subset[str(name[w])].reset_index(drop=True)
            Y = t_subset["AOD modis"].reset_index(drop=True)
            if (len(t_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                rmse = mean_squared_error(X,Y, squared=False)
                bias = MB(X,Y)
                err = ME(X,Y)
                x1=np.linspace(0,1.2,500)
                y1=slope*x1+intercept
                if str(resol) == '3K':
                    y_err = 0.05 + 0.20*x1
                else:
                    y_err = 0.05 + 0.15*x1
                y_min = x1-y_err
                y_max = x1 + y_err
                p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                poly = p1 + p2
                q = [(X[i], Y[i]) for i in range(X.shape[0])]
                p = path.Path(poly)
                count = sum(p.contains_points(q))
                porcentaje = round((count/len(X))*100,2)
                textstr = '\n'.join((
                    r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                    r'$n=%.0f$' % (len(X),),
                    r'$R=%.2f$' % (r_value, ),
                    r'$RMSE=%.2f$' % (rmse, ),
                    r'$MB=%.2f$' % (bias, ),
                    r'$ME=%.2f$' % (err, ),
                    r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                axs[w,e].scatter(X,Y, marker = marker[w],c=colour[w])
                axs[w,e].plot(x1,x1,'-',color='black')
                axs[w,e].plot(x1,y1,'-',color='m')
                axs[w,e].plot(x1,x1-y_err,'--',color='black')
                axs[w,e].plot(x1,x1+y_err,'--',color='black')
                axs[w,e].axis([0,1.2,0,1.2])
                for axis in ['top','bottom','left','right']:
                    axs[w,e].spines[axis].set_linewidth(3.0)
                axs[w,e].set_xticks(np.linspace(0,1.2,4))
                axs[w,e].set_yticks(np.linspace(0,1.2,4))
                props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                axs[w,e].text(0.02, 1.15, textstr, fontsize=21,
                        verticalalignment='top', bbox=props)
                axs[w,e].text(0.9,0.05,('d < '+str(diss[e])+'\n'+
                                        't < \xB1 '+str(name[w][5:7])+' min'),
                              fontsize=21,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
    plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_terra.png',bbox_inches='tight')
    plt.show()

    ################################ AQUA #####################################
    fig, axs = plt.subplots(3, 4,figsize=(29,17),sharex=True,sharey=True)
    for ax in axs.flat:
        ax.set(xlabel='AERONET AOD', ylabel=str(prod_name)+'-'+str(resol)+' Aqua AOD')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    SMALL_SIZE = 28
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for e,dd in enumerate(['D1','D2','D3','D4']):
        da = aqua[aqua.loc[:,str(dd)] == str(dd)]
        for w in range(3):
            a_subset = da.dropna(subset=['AOD modis',str(name[w])])
            X = a_subset[str(name[w])].reset_index(drop=True)
            Y = a_subset["AOD modis"].reset_index(drop=True)
            if (len(a_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                rmse = mean_squared_error(X,Y, squared=False)
                bias = MB(X,Y)
                err = ME(X,Y)
                x1=np.linspace(0,1.2,500)
                y1=slope*x1+intercept
                if str(resol) == '3K':
                    y_err = 0.05 + 0.20*x1
                else:
                    y_err = 0.05 + 0.15*x1
                y_min = x1-y_err
                y_max = x1 + y_err
                p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                poly = p1 + p2
                q = [(X[i], Y[i]) for i in range(X.shape[0])]
                p = path.Path(poly)
                count = sum(p.contains_points(q))
                porcentaje = round((count/len(X))*100,2)
                textstr = '\n'.join((
                    r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                    r'$n=%.0f$' % (len(X),),
                    r'$R=%.2f$' % (r_value, ),
                    r'$RMSE=%.2f$' % (rmse, ),
                    r'$MB=%.2f$' % (bias, ),
                    r'$ME=%.2f$' % (err, ),
                    r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                axs[w,e].scatter(X,Y, marker = marker[w],c=colour[w])
                axs[w,e].plot(x1,x1,'-',color='black')
                axs[w,e].plot(x1,y1,'-',color='m')
                axs[w,e].plot(x1,x1-y_err,'--',color='black')
                axs[w,e].plot(x1,x1+y_err,'--',color='black')
                axs[w,e].axis([0,1.2,0,1.2])
                for axis in ['top','bottom','left','right']:
                    axs[w,e].spines[axis].set_linewidth(3.0)
                axs[w,e].set_xticks(np.linspace(0,1.2,4))
                axs[w,e].set_yticks(np.linspace(0,1.2,4))
                props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                axs[w,e].text(0.02, 1.15, textstr, fontsize=21,
                        verticalalignment='top', bbox=props)
                axs[w,e].text(0.9,0.05,('d < '+str(diss[e])+'\n'+
                                       't < \xB1 '+str(name[w][5:7])+' min'),
                              fontsize=21,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
    plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_aqua.png',bbox_inches='tight')
    plt.show()

product = ['DT_AOD','DB_AOD','DT_DB_AOD','DT_AOD']
prod_name = ['DT','DB','DT-DB','DT']
resol = ['3K','L2','L2','L2']
for city in cities:
    data = pd.DataFrame()
    for r,p,pro_name in zip(resol,product,prod_name):
        modis_cor_all(OUTPUT,INPUT_AERONET_MODIS,data,city,r,lis_modis,p,pro_name)

############################### POR TEMPORADA #################################
sumer = ['Dec','Jan','Feb']
fall = ['Mar','Apr','May']
winter = ['Jun','Jul','Aug']
spring = ['Sep','Oct','Nov']
############################# MODIS ###########################################
def modis_temporada(OUTPUT,INPUT_AERONET_MODIS,data,city,resol,listdir,prod,prod_name):
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
    #################################  TERRA  #################################
    for temp in ['DJF','MAM','JJA','SON']:
        fig, axs = plt.subplots(3, 4,figsize=(29,17),sharex=True,sharey=True)
        for ax in axs.flat:
            ax.set(xlabel='AERONET AOD', ylabel= str(prod_name)+'-'+str(resol)+' Terra AOD')
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        SMALL_SIZE = 28
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        for e,dd in enumerate(['D1','D2','D3','D4']):
            dt = terra.loc[(terra.loc[:,'temporada'] == str(temp))&(terra.loc[:,str(dd)] == str(dd))]
            for w in range(3):
                t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
                X = t_subset[str(name[w])].reset_index(drop=True)
                Y = t_subset["AOD modis"].reset_index(drop=True)
                if (len(t_subset) == 0):
                    pass
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    rmse = mean_squared_error(X,Y, squared=False)
                    bias = MB(X,Y)
                    err = ME(X,Y)
                    x1=np.linspace(0,1.2,500)
                    y1=slope*x1+intercept
                    if str(resol) == '3K':
                        y_err = 0.05 + 0.20*x1
                    else:
                        y_err = 0.05 + 0.15*x1
                    y_min = x1-y_err
                    y_max = x1 + y_err
                    p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                    p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                    poly = p1 + p2
                    q = [(X[i], Y[i]) for i in range(X.shape[0])]
                    p = path.Path(poly)
                    count = sum(p.contains_points(q))
                    porcentaje = round((count/len(X))*100,2)
                    textstr = '\n'.join((
                        r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                        r'$n=%.0f$' % (len(X),),
                        r'$R=%.2f$' % (r_value, ),
                        r'$RMSE=%.2f$' % (rmse, ),
                        r'$MB=%.2f$' % (bias, ),
                        r'$ME=%.2f$' % (err, ),
                        r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                    axs[w,e].scatter(X,Y, marker = marker[w],c=colour[w])
                    axs[w,e].plot(x1,x1,'-',color='black')
                    axs[w,e].plot(x1,y1,'-',color='m')
                    axs[w,e].plot(x1,x1-y_err,'--',color='black')
                    axs[w,e].plot(x1,x1+y_err,'--',color='black')
                    axs[w,e].axis([0,1.2,0,1.2])
                    for axis in ['top','bottom','left','right']:
                        axs[w,e].spines[axis].set_linewidth(3.0)
                    axs[w,e].set_xticks(np.linspace(0,1.2,4))
                    axs[w,e].set_yticks(np.linspace(0,1.2,4))
                    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                    axs[w,e].text(0.02, 1.15, textstr, fontsize=21,
                        verticalalignment='top', bbox=props)
                    axs[w,e].text(0.9,0.05,('d < '+str(diss[e])+'\n'+
                                           't < \xB1 '+str(name[w][5:7])+' min'),
                                  fontsize=21,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
        plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_'+str(temp)+'_terra.png',bbox_inches='tight')
        plt.show()

    ##################################  AQUA  #################################
        fig, axs = plt.subplots(3, 4,figsize=(29,17),sharex=True,sharey=True)
        for ax in axs.flat:
            ax.set(xlabel='AERONET AOD', ylabel= str(prod_name)+'-'+str(resol)+' Aqua AOD')
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        SMALL_SIZE = 28
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        for e,dd in enumerate(['D1','D2','D3','D4']):
            da = aqua.loc[(aqua.loc[:,'temporada'] == str(temp))&(aqua.loc[:,str(dd)] == str(dd))]
            for w in range(3):
                t_subset = da.dropna(subset=['AOD modis',str(name[w])])
                X = t_subset[str(name[w])].reset_index(drop=True)
                Y = t_subset["AOD modis"].reset_index(drop=True)
                if (len(t_subset) == 0):
                    pass
                else:                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                    rmse = mean_squared_error(X,Y, squared=False)
                    bias = MB(X,Y)
                    err = ME(X,Y)
                    x1=np.linspace(0,1.2,500)
                    y1=slope*x1+intercept
                    if str(resol) == '3K':
                        y_err = 0.05 + 0.20*x1
                    else:
                        y_err = 0.05 + 0.15*x1
                    y_min = x1-y_err
                    y_max = x1 + y_err
                    p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                    p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                    poly = p1 + p2
                    q = [(X[i], Y[i]) for i in range(X.shape[0])]
                    p = path.Path(poly)
                    count = sum(p.contains_points(q))
                    porcentaje = round((count/len(X))*100,2)
                    textstr = '\n'.join((
                        r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                        r'$n=%.0f$' % (len(X),),
                        r'$R=%.2f$' % (r_value, ),
                        r'$RMSE=%.2f$' % (rmse, ),
                        r'$MB=%.2f$' % (bias, ),
                        r'$ME=%.2f$' % (err, ),
                        r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                    axs[w,e].scatter(X,Y, marker = marker[w],c=colour[w])
                    axs[w,e].plot(x1,x1,'-',color='black')
                    axs[w,e].plot(x1,y1,'-',color='m')
                    axs[w,e].plot(x1,x1-y_err,'--',color='black')
                    axs[w,e].plot(x1,x1+y_err,'--',color='black')
                    axs[w,e].axis([0,1.2,0,1.2])
                    for axis in ['top','bottom','left','right']:
                        axs[w,e].spines[axis].set_linewidth(3.0)
                    axs[w,e].set_xticks(np.linspace(0,1.2,4))
                    axs[w,e].set_yticks(np.linspace(0,1.2,4))
                    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                    axs[w,e].text(0.02, 1.15, textstr, fontsize=21,
                        verticalalignment='top', bbox=props)
                    axs[w,e].text(0.9,0.05,('d < '+str(diss[e])+'\n'+
                                           't < \xB1 '+str(name[w][5:7])+' min'),
                                  fontsize=21,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
        plt.savefig(OUTPUT +str(city)+'_'+str(resol)+'_'+str(prod)+'_'+str(temp)+'_aqua.png',bbox_inches='tight')
        plt.show()

prod_name = ['DT','DB','DT-DB','DT']
product = ['DT_AOD','DB_AOD','DT_DB_AOD','DT_AOD']
resol = ['3K','L2','L2','L2']
for city in cities:
    data = pd.DataFrame()
    for r,p,pro_name in zip(resol,product,prod_name):
        modis_temporada(OUTPUT,INPUT_AERONET_MODIS,data,city,r,lis_modis,p,pro_name)

################################ MAIAC ########################################
def maiac_all(OUTPUT,INPUT_AERONET_MAIAC,data,city,listdir,prod):
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
    #################################  TERRA  #################################
    fig, axs = plt.subplots(1,3,figsize=(15,6),sharey=True)
    for ax in axs.flat:
        ax.set(xlabel='AERONET AOD', ylabel=str(prod)+' - 1km Terra AOD')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    SMALL_SIZE = 20
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for dd in ['D1','D2','D3','D4']:
        dt = terra[terra.loc[:,str(dd)] == str(dd)]
    for w in range(3):
        t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
        X = t_subset[str(name[w])].reset_index(drop=True)
        Y = t_subset["AOD modis"].reset_index(drop=True)
        if (len(t_subset) == 0):
            pass
        else:
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            rmse = mean_squared_error(X,Y, squared=False)
            bias = MB(X,Y)
            err = ME(X,Y)
            x1=np.linspace(0,1.2,500)
            y1=slope*x1+intercept
            y_err = 0.05 + 0.05*x1
            y_min = x1-y_err
            y_max = x1 + y_err
            p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
            p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
            poly = p1 + p2
            q = [(X[i], Y[i]) for i in range(X.shape[0])]
            p = path.Path(poly)
            count = sum(p.contains_points(q))
            porcentaje = round((count/len(X))*100,2)
            textstr = '\n'.join((
                r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                r'$n=%.0f$' % (len(X),),
                r'$R=%.2f$' % (r_value, ),
                r'$RMSE=%.2f$' % (rmse, ),
                r'$MB=%.2f$' % (bias, ),
                r'$ME=%.2f$' % (err, ),
                r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
            axs[w].scatter(X,Y, marker = marker[w],c=colour[w])
            axs[w].plot(x1,x1,'-',color='black')
            axs[w].plot(x1,y1,'-',color='m')
            axs[w].plot(x1,x1-y_err,'--',color='black')
            axs[w].plot(x1,x1+y_err,'--',color='black')
            axs[w].axis([0,1.2,0,1.2])
            for axis in ['top','bottom','left','right']:
                axs[w].spines[axis].set_linewidth(3.0)
            axs[w].set_xticks(np.linspace(0,1.2,4))
            axs[w].set_yticks(np.linspace(0,1.2,4))
            props = dict(boxstyle='round', facecolor='white', alpha=0.7)
            axs[w].text(0.02, 1.15, textstr, fontsize=15,
                    verticalalignment='top', bbox=props)
            axs[w].text(0.9,0.05,('d < 3km '+'\n'+
                                   't < \xB1 '+str(name[w][5:7])+' min'),
                        fontsize=15,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
    plt.tight_layout()
    plt.savefig(OUTPUT +str(city)+'_MAIAC_terra.png',bbox_inches='tight')
    plt.show()

    ################################ AQUA #####################################
    fig, axs = plt.subplots(1,3,figsize=(15,6),sharey=True)
    for ax in axs.flat:
        ax.set(xlabel='AERONET AOD', ylabel= str(prod)+' - 1km Aqua AOD')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    SMALL_SIZE = 20
    matplotlib.rc('font', size=SMALL_SIZE)
    matplotlib.rc('axes', titlesize=SMALL_SIZE)
    for dd in ['D1','D2','D3','D4']:
        da = aqua[aqua.loc[:,str(dd)] == str(dd)]
    for w in range(3):
        a_subset = da.dropna(subset=['AOD modis',str(name[w])])
        X = a_subset[str(name[w])].reset_index(drop=True)
        Y = a_subset["AOD modis"].reset_index(drop=True)
        if (len(a_subset) == 0):
            pass
        else:                    
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            rmse = mean_squared_error(X,Y, squared=False)
            bias = MB(X,Y)
            err = ME(X,Y)
            x1=np.linspace(0,1.2,500)
            y1=slope*x1+intercept
            y_err = 0.05 + 0.05*x1
            y_min = x1-y_err
            y_max = x1 + y_err
            p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
            p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
            poly = p1 + p2
            q = [(X[i], Y[i]) for i in range(X.shape[0])]
            p = path.Path(poly)
            count = sum(p.contains_points(q))
            porcentaje = round((count/len(X))*100,2)
            textstr = '\n'.join((
                r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                r'$n=%.0f$' % (len(X),),
                r'$R=%.2f$' % (r_value, ),
                r'$RMSE=%.2f$' % (rmse, ),
                r'$MB=%.2f$' % (bias, ),
                r'$ME=%.2f$' % (err, ),
                r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
            axs[w].scatter(X,Y, marker = marker[w],c=colour[w])
            axs[w].plot(x1,x1,'-',color='black')
            axs[w].plot(x1,y1,'-',color='m')
            axs[w].plot(x1,x1-y_err,'--',color='black')
            axs[w].plot(x1,x1+y_err,'--',color='black')
            axs[w].axis([0,1.2,0,1.2])
            for axis in ['top','bottom','left','right']:
                axs[w].spines[axis].set_linewidth(3.0)
            axs[w].set_xticks(np.linspace(0,1.2,4))
            axs[w].set_yticks(np.linspace(0,1.2,4))
            props = dict(boxstyle='round', facecolor='white', alpha=0.7)
            axs[w].text(0.02, 1.15, textstr, fontsize=15,
                    verticalalignment='top', bbox=props)
            axs[w].text(0.9,0.05,('d < 3km '+'\n'+
                                   't < \xB1 '+str(name[w][5:7])+' min'),
                        fontsize=15,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
    plt.tight_layout()
    plt.savefig(OUTPUT +str(city)+'_MAIAC_aqua.png',bbox_inches='tight')
    plt.show()

for city in cities:
    data = pd.DataFrame()
    maiac_all(OUTPUT,INPUT_AERONET_MAIAC,data,city,lis_maiac,'MAIAC')

############################## POR TEMPORADA ##################################
def maiac_temporada(OUTPUT,INPUT_AERONET_MAIAC,data,city,listdir,prod):
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
    #################################  TERRA  #################################
    for temp in ['DJF','MAM','JJA','SON']:
        fig, axs = plt.subplots(1,3,figsize=(15,6),sharey=True)
        for ax in axs.flat:
            ax.set(xlabel='AERONET AOD', ylabel= str(prod)+' - 1km Terra AOD')
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        SMALL_SIZE = 20
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        for e,dd in enumerate(['D1','D2','D3','D4']):
            dt = terra.loc[(terra.loc[:,'temporada'] == str(temp))&(terra.loc[:,str(dd)] == str(dd))]
        for w in range(3):
            t_subset = dt.dropna(subset=['AOD modis',str(name[w])])
            X = t_subset[str(name[w])].reset_index(drop=True)
            Y = t_subset["AOD modis"].reset_index(drop=True)
            if (len(t_subset) == 0):
                pass
            else:
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                rmse = mean_squared_error(X,Y, squared=False)
                bias = MB(X,Y)
                err = ME(X,Y)
                x1=np.linspace(0,1.2,500)
                y1=slope*x1+intercept
                y_err = 0.05 + 0.05*x1
                y_min = x1-y_err
                y_max = x1 + y_err
                p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                poly = p1 + p2
                q = [(X[i], Y[i]) for i in range(X.shape[0])]
                p = path.Path(poly)
                count = sum(p.contains_points(q))
                porcentaje = round((count/len(X))*100,2)
                textstr = '\n'.join((
                    r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                    r'$n=%.0f$' % (len(X),),
                    r'$R=%.2f$' % (r_value, ),
                    r'$RMSE=%.2f$' % (rmse, ),
                    r'$MB=%.2f$' % (bias, ),
                    r'$ME=%.2f$' % (err, ),
                    r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                axs[w].scatter(X,Y, marker = marker[w],c=colour[w])
                axs[w].plot(x1,x1,'-',color='black')
                axs[w].plot(x1,y1,'-',color='m')
                axs[w].plot(x1,x1-y_err,'--',color='black')
                axs[w].plot(x1,x1+y_err,'--',color='black')
                axs[w].axis([0,1.2,0,1.2])
                for axis in ['top','bottom','left','right']:
                    axs[w].spines[axis].set_linewidth(3.0)
                axs[w].set_xticks(np.linspace(0,1.2,4))
                axs[w].set_yticks(np.linspace(0,1.2,4))
                props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                axs[w].text(0.02, 1.15, textstr, fontsize=15,
                            verticalalignment='top', bbox=props)
                axs[w].text(0.9,0.05,('d < 3km '+'\n'+
                                       't < \xB1 '+str(name[w][5:7])+' min'),
                            fontsize=15,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
        plt.savefig(OUTPUT +str(city)+'_'+str(temp)+'_MAIAC_terra.png',bbox_inches='tight')
        plt.show()

    ##################################  AQUA  #################################
        fig, axs = plt.subplots(1,3,figsize=(15,6),sharey=True)
        for ax in axs.flat:
            ax.set(xlabel='AERONET AOD', ylabel= str(prod)+' - 1km Aqua AOD')
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        SMALL_SIZE = 20
        matplotlib.rc('font', size=SMALL_SIZE)
        matplotlib.rc('axes', titlesize=SMALL_SIZE)
        for e,dd in enumerate(['D1','D2','D3','D4']):
            da = aqua.loc[(aqua.loc[:,'temporada'] == str(temp))&(aqua.loc[:,str(dd)] == str(dd))]
        for w in range(3):
            t_subset = da.dropna(subset=['AOD modis',str(name[w])])
            X = t_subset[str(name[w])].reset_index(drop=True)
            Y = t_subset["AOD modis"].reset_index(drop=True)
            if (len(t_subset) == 0):
                pass
            else:
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                rmse = mean_squared_error(X,Y, squared=False)
                bias = MB(X,Y)
                err = ME(X,Y)
                x1=np.linspace(0,1.2,500)
                y1=slope*x1+intercept
                y_err = 0.05 + 0.05*x1
                y_min = x1-y_err
                y_max = x1 + y_err
                p1 =[[x1[i],y_min[i]] for i in range(len(x1))]
                p2 =[[x1[(len(x1)-1)-i],y_max[(len(x1)-1)-i]] for i in range(len(x1))]
                poly = p1 + p2
                q = [(X[i], Y[i]) for i in range(X.shape[0])]
                p = path.Path(poly)
                count = sum(p.contains_points(q))
                porcentaje = round((count/len(X))*100,2)
                textstr = '\n'.join((
                    r'$y=%.2f$' % (slope, )+'*x + ' +  "%.3f"%intercept,
                    r'$n=%.0f$' % (len(X),),
                    r'$R=%.2f$' % (r_value, ),
                    r'$RMSE=%.2f$' % (rmse, ),
                    r'$MB=%.2f$' % (bias, ),
                    r'$ME=%.2f$' % (err, ),
                    r'$within$'+' '+'$EE =%.2f$' % (porcentaje,)))
                axs[w].scatter(X,Y, marker = marker[w],c=colour[w])
                axs[w].plot(x1,x1,'-',color='black')
                axs[w].plot(x1,y1,'-',color='m')
                axs[w].plot(x1,x1-y_err,'--',color='black')
                axs[w].plot(x1,x1+y_err,'--',color='black')
                axs[w].axis([0,1.2,0,1.2])
                for axis in ['top','bottom','left','right']:
                    axs[w].spines[axis].set_linewidth(3.0)
                axs[w].set_xticks(np.linspace(0,1.2,4))
                axs[w].set_yticks(np.linspace(0,1.2,4))
                props = dict(boxstyle='round', facecolor='white', alpha=0.7)
                axs[w].text(0.02, 1.15, textstr, fontsize=15,
                            verticalalignment='top', bbox=props)
                axs[w].text(0.9,0.05,('d < 3km '+'\n'+
                                       't < \xB1 '+str(name[w][5:7])+' min'),
                            fontsize=15,ha='center',bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.7})
        plt.savefig(OUTPUT +str(city)+'_'+str(temp)+'_MAIAC_aqua.png',bbox_inches='tight')
        plt.show()

for city in cities:
    data = pd.DataFrame()
    maiac_temporada(OUTPUT,INPUT_AERONET_MAIAC,data,city,lis_maiac,'MAIAC')
