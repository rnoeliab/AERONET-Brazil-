#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:14:49 2020

@author: noelia
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.lines as mlines
import seaborn as sns

INPUT_AERONET_MODIS = "/imagen_data/modis/results/aero_mod/"
OUTPUT = "/imagen_data/modis/results/aero_mod_statis/"
listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)

name = ["prom_60_min_AOD_aero","prom_30_min_AOD_aero","prom_15_min_AOD_aero"]
marker = ["*","v","s"]
colour = ["black","red","blue"]
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']
producto = ['DT_DB_AOD_L2_MODIS','DT_AOD_3K_MODIS','DT_AOD_L2_MODIS','DB_AOD_L2_MODIS']

dat_1 = pd.DataFrame()
dat_2 = pd.DataFrame()
dat_3 = pd.DataFrame()
dat_4 = pd.DataFrame()
for s in range(len(station)):
    for n in listdir:
        if 'DT_DB_AOD_L2_MODIS_'+str(station[s]) in n:
            a = pd.read_csv(INPUT_AERONET_MODIS+n)
            a['Product'] = 'DT_DB_AOD_L2_MODIS'
            a['Station'] = station[s]
            dat_1 = pd.concat([dat_1,a])         
        elif 'DT_AOD_3K_MODIS_'+str(station[s]) in n:
            a = pd.read_csv(INPUT_AERONET_MODIS+n)
            a['Product'] = 'DT_AOD_3K_MODIS'
            a['Station'] = station[s]
            dat_2 = pd.concat([dat_2,a])         
        elif 'DT_AOD_L2_MODIS_'+str(station[s]) in n:
            a = pd.read_csv(INPUT_AERONET_MODIS+n)
            a['Product'] = 'DT_AOD_L2_MODIS'
            a['Station'] = station[s]
            dat_3 = pd.concat([dat_3,a])         
        elif 'DB_AOD_L2_MODIS_'+str(station[s]) in n:
            a = pd.read_csv(INPUT_AERONET_MODIS+n)
            a['Product'] = 'DB_AOD_L2_MODIS'
            a['Station'] = station[s]
            dat_4 = pd.concat([dat_4,a])         
dato_total = pd.concat([dat_1, dat_2, dat_3, dat_4], axis=0)
dato_total = dato_total.reset_index(drop=True)

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True,figsize=(30,25)) 
rect = fig.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_ylabel("AOD values - MODIS", fontsize=35, labelpad=55)
ax0.set_xlabel("AOD values - AERONET", fontsize=35,labelpad=55)
for i in range(4):
    for j in range(4):
        dato = dato_total[(dato_total['Station'] == station[i]) & (dato_total['Product'] == producto[j])]
        dato['AOD modis'][dato['AOD modis'] < 0 ] = np.nan
        corre = []
        for w in range(3):
            dato[str(name[w])][dato[str(name[w])] < 0 ] = np.nan
            df1_subset = dato.dropna(subset=["AOD modis",str(name[w])])
            X = df1_subset[str(name[w])]
            Y = df1_subset["AOD modis"]    
            if (len(df1_subset) == 0):
                pass
            else:                    
                slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                l = axes[i, j].scatter(dato[str(name[w])],dato["AOD modis"], marker=str(marker[w]), c=str(colour[w]),linewidth=1, s=3)             
                axes[i, j].plot(np.unique(X), np.poly1d(np.polyfit(X, Y, 1))(np.unique(X)), color='black',linewidth=1)
                df1 = pd.DataFrame({ 'observado': df1_subset[str(name[w])].values, 'modelado': df1_subset["AOD modis"].values})
                corre.append(df1.corr(method='pearson').values[0,1])
        textstr = '\n'.join((
            r'$ R_{60}=%.2f$' % (corre[0], ),
            r'$ R_{30}=%.2f$' % (corre[1], ),
            r'$ R_{15}=%.2f$' % (corre[2], ),
            r'$n=%.0f$' % (len(df1_subset), )))            
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        axes[i, j].text(0.0,1.0, textstr, fontsize=20, verticalalignment='top', bbox=props)
        axes[i,j].set_ylim((-0.05,1.1))
        axes[i,j].tick_params(axis="x", labelsize=25)
        axes[i,j].set_xlim((-0.05,1.1))
        axes[i,j].set_xticks(np.arange(0,1.2,0.2))
        axes[i,j].tick_params(axis="y", labelsize=25)
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    axes[i, 3].text(1.2,0.5, str(producto[i][0:-6].replace("_","-")), fontsize=30, verticalalignment='top', bbox=props)
    axes[0,i].set_title(str(station[i].replace("_"," ")),fontsize=25)    

black_line = mlines.Line2D([], [], color='black', marker='*', markersize=6, label=str(name[0][5::]))
red_line = mlines.Line2D([], [], color='red', marker='v', markersize=6, label=str(name[1][5::]))
blue_line = mlines.Line2D([], [], color='blue', marker='s', markersize=6, label=str(name[2][5::]))
ax0.legend(handles=[black_line,red_line,blue_line],ncol=3,bbox_to_anchor=(0.9, 1.08), fontsize=25)
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(OUTPUT +'correlation_total.png',dpi=100, bbox_inches='tight')
plt.show()

pal = {'MODIS': 'red', 'AERONET': 'blue'}
boxprops = {'edgecolor': 'k', 'linewidth': 2}
lineprops = {'color': 'k', 'linewidth': 2}
kwargs = {'palette': pal, 'hue_order': ['AERONET', 'MODIS'],'sym':'w'}
boxplot_kwargs = dict({'boxprops': boxprops, 'medianprops': lineprops,
                        'whiskerprops': lineprops, 'capprops': lineprops,
                        'width': 0.75},**kwargs)

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True,figsize=(30,20)) 
rect = fig.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_ylabel("AOD values", fontsize=35, labelpad=55)
ax0.set_xlabel("Time (between AERONET and MODIS)", fontsize=35,labelpad=55)
for i in range(4):
    for j in range(4):
        dato = dato_total[(dato_total['Station'] == station[i]) & (dato_total['Product'] == producto[j])]
        dato['AOD_mod'][dato['AOD_mod'] < 0 ] = np.nan
        data_x = []
        for w in range(3):
            dato[str(name[w])][dato[str(name[w])] < 0 ] = np.nan
            df1_subset = dato.dropna(subset=["AOD_mod",str(name[w])])
            X = df1_subset[str(name[w])]
            Y = df1_subset["AOD_mod"]    
            if (len(df1_subset) == 0):
                pass
            else:
                data_x.append([X,Y])
        df1=pd.DataFrame(data_x[0]).T.assign(Trial="60 min")
        df1.columns = ['AERONET','MODIS','Trial'] 
        df2=pd.DataFrame(data_x[1]).T.assign(Trial="30 min")
        df2.columns = ['AERONET','MODIS','Trial']
        df3=pd.DataFrame(data_x[2]).T.assign(Trial="15 min")
        df3.columns = ['AERONET','MODIS','Trial']
        data = pd.concat([df1, df2, df3], ignore_index=True)    
        mdf = pd.melt(data, id_vars=['Trial'], var_name=['Data'])      # MELT
        sns.boxplot(x="Trial", y="value", hue="Data", data=mdf, ax=axes[i,j],**boxplot_kwargs)
        axes[i,j].tick_params(axis="x", labelsize=25)
        axes[i,j].set_yticks(np.arange(0,2.0,0.5))
        axes[i,j].set_ylim((-0.05,2.0))
        axes[i,j].set_ylabel("")
        axes[i,j].set_xlabel("")
        axes[i,j].tick_params(axis="y", labelsize=25)
        handles, labels = axes[i,j].get_legend_handles_labels()
        lgd = axes[i,j].legend(handles[0:2], labels[0:2],
                loc='upper left',
                fontsize=20,
                handletextpad=0.5)
        lgd.legendHandles[0]._sizes = [40]
        lgd.legendHandles[1]._sizes = [40]
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    axes[i, 3].text(2.8,0.5, str(producto[i][0:-6].replace("_","-")), fontsize=30, verticalalignment='top', bbox=props)
    axes[0,i].set_title(str(station[i].replace("_"," ")),fontsize=25)    
plt.subplots_adjust(wspace=0, hspace=0)    
plt.savefig(OUTPUT +'errors_total.png',dpi=100, bbox_inches='tight')
plt.show()

import statistics_basic as stat

aa = np.arange(len(name))

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True,figsize=(30,20)) 
rect = fig.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_ylabel("AOD values", fontsize=35, labelpad=95)
ax0.set_xlabel("Time (between AERONET and MODIS)", fontsize=35,labelpad=55)
for i in range(4):
    for j in range(4):
        dato = dato_total[(dato_total['Station'] == station[i]) & (dato_total['Product'] == producto[j])]
        dato['AOD_mod'][dato['AOD_mod'] < 0 ] = np.nan
        mb = []
        for w in range(3):
            dato[str(name[w])][dato[str(name[w])] < 0 ] = np.nan
            df1_subset = dato.dropna(subset=["AOD_mod",str(name[w])])
            X = df1_subset[str(name[w])]
            Y = df1_subset["AOD_mod"]    
            if (len(df1_subset) == 0):
                pass
            else:    
                mb.append(stat.MB(X,Y))
        axes[i,j].bar(name, mb, width=0.2, color='black')
        axes[i,j].set_ylim((-0.05,0.01))
        axes[i,j].set_xlim((-0.5,2.5))
        axes[i,j].tick_params(axis="x", labelsize=25)
        axes[i,j].tick_params(axis="y", labelsize=25)
        axes[i,j].set_xticks(aa)
        axes[i,j].set_xticklabels(["60 min","30 min","15 min"])
#        axes[i,j].grid()
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    axes[i, 3].text(2.7,-0.02, str(producto[i][0:-6].replace("_","-")), fontsize=30, verticalalignment='top', bbox=props)
    axes[0,i].set_title(str(station[i].replace("_"," ")),fontsize=25)    
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(OUTPUT +'mb_total.png',dpi=100, bbox_inches='tight')
plt.show()       

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True,figsize=(30,20)) 
rect = fig.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_ylabel("AOD values", fontsize=35, labelpad=95)
ax0.set_xlabel("Time (between AERONET and MODIS)", fontsize=35,labelpad=55)
for i in range(4):
    for j in range(4):
        dato = dato_total[(dato_total['Station'] == station[i]) & (dato_total['Product'] == producto[j])]
        dato['AOD_mod'][dato['AOD_mod'] < 0 ] = np.nan
        mb = []
        for w in range(3):
            dato[str(name[w])][dato[str(name[w])] < 0 ] = np.nan
            df1_subset = dato.dropna(subset=["AOD_mod",str(name[w])])
            X = df1_subset[str(name[w])]
            Y = df1_subset["AOD_mod"]    
            if (len(df1_subset) == 0):
                pass
            else:    
                mb.append(stat.RMSE(X,Y))
        axes[i,j].bar(name, mb, width=0.2, color='black')
        axes[i,j].set_ylim((0,0.2))
        axes[i,j].set_xlim((-0.5,2.5))
        axes[i,j].tick_params(axis="x", labelsize=25)
        axes[i,j].tick_params(axis="y", labelsize=25)
        axes[i,j].set_xticks(aa)
        axes[i,j].set_yticks(np.arange(0,0.2,0.05))
        axes[i,j].set_xticklabels(["60 min","30 min","15 min"])
#        axes[i,j].grid()
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    axes[i, 3].text(2.7,0.10, str(producto[i][0:-6].replace("_","-")), fontsize=30, verticalalignment='top', bbox=props)
    axes[0,i].set_title(str(station[i].replace("_"," ")),fontsize=25)    
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(OUTPUT +'rmse_total.png',dpi=100, bbox_inches='tight')
plt.show()  

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True,figsize=(30,20)) 
rect = fig.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_ylabel("AOD values", fontsize=35, labelpad=65)
ax0.set_xlabel("Time (between AERONET and MODIS)", fontsize=35,labelpad=55)
for i in range(4):
    for j in range(4):
        dato = dato_total[(dato_total['Station'] == station[i]) & (dato_total['Product'] == producto[j])]
        dato['AOD_mod'][dato['AOD_mod'] < 0 ] = np.nan
        mb = []
        for w in range(3):
            dato[str(name[w])][dato[str(name[w])] < 0 ] = np.nan
            df1_subset = dato.dropna(subset=["AOD_mod",str(name[w])])
            X = df1_subset[str(name[w])]
            Y = df1_subset["AOD_mod"]    
            if (len(df1_subset) == 0):
                pass
            else:    
                mb.append(stat.ioa(X,Y))
        axes[i,j].bar(name, mb, width=0.2, color='black')
        axes[i,j].set_ylim((0.,1.))
        axes[i,j].set_xlim((-0.5,2.5))
        axes[i,j].tick_params(axis="x", labelsize=25)
        axes[i,j].tick_params(axis="y", labelsize=25)
        axes[i,j].set_xticks(aa)
        axes[i,j].set_yticks(np.arange(0,1.,0.2))        
        axes[i,j].set_xticklabels(["60 min","30 min","15 min"])
#        axes[i,j].grid()
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    axes[i, 3].text(2.7,0.5, str(producto[i][0:-6].replace("_","-")), fontsize=30, verticalalignment='top', bbox=props)
    axes[0,i].set_title(str(station[i].replace("_"," ")),fontsize=25)    
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(OUTPUT +'ioa_total.png',dpi=100, bbox_inches='tight')
plt.show()  

