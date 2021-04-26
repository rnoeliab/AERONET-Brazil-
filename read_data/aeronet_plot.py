#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:48:05 2019

@author: noelia
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


INPUT ="/media/noelia/TOSHIBA EXT/doctorado/usp/in-situ/aeronet/AOD/"
listdir = os.listdir(INPUT)
listdir=sorted(listdir, key=str.lower)
OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/in-situ/aeronet/figures/"

color = ['black','blue','red','orange']
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']
data = pd.DataFrame()
for i in range(len(listdir)):
    print(listdir[i][5:-8])
    aa = pd.read_csv(INPUT+listdir[i])
    aa["Date(dd:mm:yyyy)"] = aa["Date(dd:mm:yyyy)"].replace({':':'-'}, regex=True)
    aa.columns = ['Date','Time','AOD (550nm)']
    aa['Station'] = listdir[i][5:-8] 
    aa['AOD (550nm)'][aa['AOD (550nm)'] < 0] = np.nan
    data = pd.concat([data,aa])
data = data.reset_index(drop=True)
for n,j in enumerate(data["Date"]):
    data['Date'][n] = j[6:10]+'-'+j[3:5]+'-'+j[0:2]
data.Date = pd.to_datetime(data["Date"]).dt.strftime("%Y-%m-%d")
df = data.sort_values(by=['Station','Date'])
df.set_index('Date',inplace=True)

################################# Plotando ####################################
fig1 = plt.figure(figsize=(30,25)) 
rect = fig1.patch
rect.set_facecolor('lightgoldenrodyellow')
ax0 = fig1.add_subplot(111, frame_on=False)
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_title("AERONET Stations over SPMR from 2014 - 2020",size=30)
ax0.set_ylabel("AOD", fontsize=35, labelpad=45)
for s in range(len(station)):   
    ax = fig1.add_subplot(4,1,s+1)
    dim = df.loc[df["Station"] == station[s]]
    days = []
    for d in range(len(dim)//350):
#        print(df.index[d*300])
        days.append(dim.index[d*350])
    df.loc[df["Station"] == station[s]].plot(c = color[s], marker = "*", linewidth = 1.0, ax = ax, legend=False)
    ax.axis([0,len(dim), 0,1.5])
    ax.set_xticks(np.linspace(0,len(dim),len(dim)//350+1))
    ax.set_xticklabels(days, rotation=63)
    plt.xticks(size = 25)
    plt.yticks(size = 25)
    red_patch = mpatches.Patch(color=color[s], label= str(station[s]))
    plt.legend(handles=[red_patch], loc = 'upper right', prop={'size': 35})
plt.xlabel("Time (days)", size = 35)
plt.tight_layout()
plt.savefig(OUTPUT +'stations.jpg')
plt.show()
