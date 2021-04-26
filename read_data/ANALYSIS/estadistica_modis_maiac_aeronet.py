#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:49:00 2020

@author: noelia
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def MB(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    mb = np.nanmean(diff)
    return mb

def NMB(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    nmb = (np.nansum(diff)/np.nansum(data_obs))*100
    return nmb

def ME(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    me = np.nanmean(diff)
    return me

def NME(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    nme = (np.nansum(diff)/np.nansum(data_obs))*100
    return nme

def RMSE(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = np.power((data_model - data_obs), 2)
    rmse = np.sqrt(np.nanmean(diff))
    return rmse

def ioa(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    obs_mean = np.nanmean(data_obs)
    diff = np.power((data_model - data_obs), 2)
    a = np.nansum(diff)
    b = np.power((abs(data_model-obs_mean)+abs(data_obs-obs_mean)),2)
    c = np.nansum(b)
    ioa = 1 - (a/c)
    return ioa

def pearson(data_obs,data_model):
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    model_mean = np.nanmean(data_model)
    obs_mean = np.nanmean(data_obs)
    rest_obs = data_obs - obs_mean
    rest_model = data_model - model_mean 
    a = np.nansum(rest_model*rest_obs) 
    b =(np.nansum(np.power(rest_model,2)))*(np.nansum(np.power(rest_obs,2)))
    r = a/(np.sqrt(b))
    return r

INPUT_AERONET_MODIS = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_maiac/"
listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)
listdir1 = os.listdir(INPUT_AERONET_MAIAC)
listdir1 =sorted(listdir1, key=str.lower)

OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod_statis/estadistica/"

cities = ["Sao_Paulo","SP-EACH","Itajuba","Cachoeira_Paulista"]
name1 = ["prom_60_min_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
marker = ["*","v","s"]
colour = ["black","red","blue"]

statis = pd.DataFrame({'IP':[]})

for i,n in enumerate(range(len(listdir))):
    print(i,listdir[n])
    df = pd.read_csv(INPUT_AERONET_MODIS+listdir[n])
    statis.loc[i,'IP']=listdir[n][0:-12]
    a = df.loc[df['count 3x3']>=5.0]
    for j in range(len(name1)):
        a['AOD modis'][a['AOD modis'] < 0 ] = np.nan
        a[str(name1[j])][a[str(name1[j])] < 0 ] = np.nan
        data_obs = np.array(a[str(name1[j])])
        data_model = np.array(a['AOD modis'])
        statis.loc[i,'MB_'+str(name1[j][5:7])] = MB(data_obs,data_model)
        statis.loc[i,'NMB_'+str(name1[j][5:7])] = NMB(data_obs,data_model)
        statis.loc[i,'ME_'+str(name1[j][5:7])] = ME(data_obs,data_model)
        statis.loc[i,'NME_'+str(name1[j][5:7])] = NME(data_obs,data_model)
        statis.loc[i,'RMSE_'+str(name1[j][5:7])] = RMSE(data_obs,data_model)
        statis.loc[i,'IOA_'+str(name1[j][5:7])] = ioa(data_obs,data_model)
        statis.loc[i,'PEARSON_'+str(name1[j][5:7])] = pearson(data_obs,data_model)
statis.to_csv(OUTPUT+"estatistica_MODIS.csv", index=False)
###################################  PLOT #####################################
x_date = list(statis['IP'])
bar_width = 0.6
colors = ["green","red","blue"]
fig = plt.figure(figsize=(30,15)) 
ax = fig.add_subplot(111)
dat = statis[["IP","MB_15","MB_30","MB_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axhline(0, color='k', linewidth=0.9)
ax.axis([-1,len(statis), -0.35,0.35])
ax.set_xticks(statis['IP'].index)
ax.set_xticklabels(x_date,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("BIAS", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
# for rect in ax.patches:
#     # Find where everything is located
#     height = rect.get_height()
#     width = rect.get_width()
#     x = rect.get_x()
#     y = rect.get_y()
    
#     label_text = f'{height:.2f}'  # f'{height:.2f}' to format decimal values
    
#     # ax.text(x, y, text)
#     label_x = x + width / 2
#     label_y = y + height / 2

#     # plot only when height is greater than specified value
#     ax.text(label_x, label_y, label_text, ha='center', va='center', fontsize=8,rotation=90)
    
plt.tight_layout()
plt.savefig(OUTPUT +'figures/bias_modis.png')
plt.show()


fig = plt.figure(figsize=(30,15)) 
ax = fig.add_subplot(111)
dat = statis[["IP","RMSE_15","RMSE_30","RMSE_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis), 0.,1.0])
ax.set_xticks(statis['IP'].index)
ax.set_xticklabels(x_date,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("RMSE", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/rmse_modis.png')
plt.show()


fig = plt.figure(figsize=(30,15)) 
ax = fig.add_subplot(111)
dat = statis[["IP","IOA_15","IOA_30","IOA_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis), -0.1,3.0])
ax.set_xticks(statis['IP'].index)
ax.set_xticklabels(x_date,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("IOA", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/ioa_modis.png')
plt.show()

fig = plt.figure(figsize=(30,15)) 
ax = fig.add_subplot(111)
dat = statis[["IP","PEARSON_15","PEARSON_30","PEARSON_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis), -0.1,2.0])
ax.set_xticks(statis['IP'].index)
ax.set_xticklabels(x_date,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("PEARSON", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/pearson_modis.png')
plt.show()

##############################    MAIAC   #####################################
statis1 = pd.DataFrame({'IP':[]})
for i,m in enumerate(range(len(listdir1))):
    df1 = pd.read_csv(INPUT_AERONET_MAIAC+listdir1[m])
    statis1.loc[i,'IP']=listdir1[m][0:-12]
    a = df1.loc[df1['count 3x3']>=5.0]
    for j in range(len(name1)):
        a['AOD modis'][a['AOD modis'] < 0 ] = np.nan
        a[str(name1[j])][a[str(name1[j])] < 0 ] = np.nan
        data_obs = np.array(a[str(name1[j])])
        data_model = np.array(a['AOD modis'])
        statis1.loc[i,'MB_'+str(name1[j][5:7])] = MB(data_obs,data_model)
        statis1.loc[i,'NMB_'+str(name1[j][5:7])] = NMB(data_obs,data_model)
        statis1.loc[i,'ME_'+str(name1[j][5:7])] = ME(data_obs,data_model)
        statis1.loc[i,'NME_'+str(name1[j][5:7])] = NME(data_obs,data_model)
        statis1.loc[i,'RMSE_'+str(name1[j][5:7])] = RMSE(data_obs,data_model)
        statis1.loc[i,'IOA_'+str(name1[j][5:7])] = ioa(data_obs,data_model)
        statis1.loc[i,'PEARSON_'+str(name1[j][5:7])] = pearson(data_obs,data_model)
statis1.to_csv(OUTPUT+"estatistica_MAIAC.csv", index=False)
###################################  PLOT #####################################
x_date1 = list(statis1['IP'])
bar_width = 0.6
colors = ["green","red","blue"]
fig = plt.figure(figsize=(25,12)) 
ax = fig.add_subplot(111)
dat = statis1[["IP","MB_15","MB_30","MB_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axhline(0, color='k', linewidth=0.9)
ax.axis([-1,len(statis1), -0.35,0.35])
ax.set_xticks(statis1['IP'].index)
ax.set_xticklabels(x_date1,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("BIAS", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/bias_maiac.png')
plt.show()

fig = plt.figure(figsize=(25,12)) 
ax = fig.add_subplot(111)
dat = statis1[["IP","RMSE_15","RMSE_30","RMSE_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis1), 0.,0.5])
ax.set_xticks(statis1['IP'].index)
ax.set_xticklabels(x_date1,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("RMSE", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/rmse_maiac.png')
plt.show()

fig = plt.figure(figsize=(25,12)) 
ax = fig.add_subplot(111)
dat = statis1[["IP","IOA_15","IOA_30","IOA_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis1), -0.1,4.0])
ax.set_xticks(statis1['IP'].index)
ax.set_xticklabels(x_date1,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("IOA", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/ioa_maiac.png')
plt.show()

fig = plt.figure(figsize=(25,12)) 
ax = fig.add_subplot(111)
dat = statis1[["IP","PEARSON_15","PEARSON_30","PEARSON_60"]]
dat.plot(kind="bar",stacked=True,color=colors,ax=ax,legend=False)
plt.legend([num for num in reversed(name1)],loc=0, prop={'size': 25},framealpha=1.0)
ax.axis([-1,len(statis1), -0.1,4.0])
ax.set_xticks(statis1['IP'].index)
ax.set_xticklabels(x_date1,rotation=90)
plt.xlabel('PRODUTO', size = 30)
plt.xticks(size = 20)
plt.yticks(size = 25)
plt.ylabel("PEARSON", size = 25)
ax.xaxis.grid(linestyle='--',color='k')
plt.tight_layout()
plt.savefig(OUTPUT +'figures/pearson_maiac.png')
plt.show()

