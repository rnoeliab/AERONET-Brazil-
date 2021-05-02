#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 17:31:30 2020

@author: noelia
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import adjustText as aT
import create_coord_circular as ccc
import matplotlib.lines as mlines


INPUT_AERONET_MODIS = "../modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "../modis/results/aero_maiac/"
listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)
listdir1 = os.listdir(INPUT_AERONET_MAIAC)
listdir1 =sorted(listdir1, key=str.lower)

OUTPUT = "../modis/results/plot_Aero_550/distancia/"

sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

producto = ['L2','3K']
colors = ['b','y','r']
marker = ['*','+','s']
alpha = [0.8,0.6,0.2]
distancia = [3000.0,15000.0,25000.0]
######################################### MODIS TOTAL ##########################
for i in np.arange(2014,2020,1):
    ano = list(filter(lambda a: str(i) in a,listdir))
    fig = plt.figure(figsize=(20, 18))
    ax = fig.add_subplot(111)
    m = Basemap(projection='cyl', resolution='h',llcrnrlat=-24.5, urcrnrlat=-22.0,
                llcrnrlon=-47.5, urcrnrlon=-44.5)
    m.drawcoastlines(linewidth=1.5)
    m.drawstates(linewidth=1.5)    
    m.drawparallels(np.arange(-90., 120., 1), labels=[1, 0, 0, 0],fontsize=25)
    m.drawmeridians(np.arange(-180., 181., 1), labels=[0, 0, 0, 1],fontsize=25) 
    m.readshapefile('../shapefile/RM_Sao_Paulo/transformed','sp',default_encoding='iso-8859-15',color='darkred',linewidth=1.5)     
    count = 0
    texts1 = []
    for name,lons,lats in zip(station,sta_lon,sta_lat):
        stn = list(filter(lambda a: str(name) in a,ano))
        if len(stn) != 0:   ### stn[0] = L2  & stn[1] = 3K
            pl2 = pd.read_csv(INPUT_AERONET_MODIS+stn[0])
            for n,d in enumerate(distancia[::-1]):
                b = pl2[pl2["distancia"] < d]
                x,y = m(b['longitud'],b['latitud'])
                plt.plot(x,y,marker[n]+colors[n],alpha=alpha[n],markersize=8,label=str(d))

        count = count + 1
        xx, yy = m(lons,lats)
        # Draw great circle
        ### 1 meter = 0.000539957
        ccc.shaded_great_circle(m, yy, xx,0.000539957*3000, col='k-',sizze=3.0,distan='3km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ccc.shaded_great_circle(m, yy, xx,0.000539957*15000, col='k--',sizze=3.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ccc.shaded_great_circle(m, yy, xx,0.000539957*25000, col='k',sizze=5.0,distan='25km')  # Distance specified in nautical miles, i.e. 100 nmi in this case

        plt.plot(xx, yy, 'og', markeredgecolor='black',markersize=10,label= str(count)+" -> "+str(name))
        texts1.append(plt.text(xx, yy, str(count), fontsize=15,color='k',
                               bbox={'facecolor':'orange', 'edgecolor':'none', 'alpha':0.9}))

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.15)
        aT.adjust_text(texts1,force_points=2.2, force_text=2.2, 
                       expand_points=(2,2),expand_text=(2,2), 
                       arrowprops=dict(arrowstyle="->", color='black', lw=2.2))
    #create legend
    p1 = mlines.Line2D([0],[0], color='r', marker='s', linestyle = 'None', markersize=10, label='< 3km')
    p2 = mlines.Line2D([0],[0], color='y', marker='+', linestyle = 'None', markersize=10, label='< 15km')
    p3 = mlines.Line2D([0],[0], color='b', marker='*', linestyle = 'None', markersize=10, label='< 25km')
    leg1 = ax.legend(handles=[p1,p2,p3],handletextpad=0.3,loc=2,prop={'size': 20},framealpha=1.0,facecolor="beige")
    leg1.set_title("MODIS data"+"\n"+
                   "Distance (m)", prop = {'size':23,'weight':'bold'})

    #create legend
    l1 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="1 -> "+str(station[0].replace("_"," ")))
    l2 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="2 -> "+str(station[1]))
    l3 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="3 -> "+str(station[2]))
    l4 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="4 -> "+str(station[3].replace("_"," ")))
    leg2 = ax.legend(handles=[l1,l2,l3,l4],handletextpad=0.3,loc=4,prop={'size': 20},framealpha=1.0,facecolor="beige")
    leg2.set_title("Aeronet Stations", prop = {'size':23,'weight':'bold'})
    ax.add_artist(leg1)

    ax.set_title("Distance between MODIS algorithm and the AERONET stations"+"\n"+
                 str(i)+ " - " + str(producto[0]), fontsize=32)
    fig.savefig(OUTPUT+str(i)+'_AERONET_'+str(producto[0])+'.png',bbox_inches='tight')
    plt.show()

    fig = plt.figure(figsize=(20, 18))
    ax = fig.add_subplot(111)
    m = Basemap(projection='cyl', resolution='h',llcrnrlat=-24.5, urcrnrlat=-22.0,
                llcrnrlon=-47.5, urcrnrlon=-44.5)
    m.drawcoastlines(linewidth=1.5)
    m.drawstates(linewidth=1.5)    
    m.drawparallels(np.arange(-90., 120., 1), labels=[1, 0, 0, 0],fontsize=25)
    m.drawmeridians(np.arange(-180., 181., 1), labels=[0, 0, 0, 1],fontsize=25) 
    m.readshapefile('../shapefile/RM_Sao_Paulo/transformed','sp',default_encoding='iso-8859-15',color='darkred',linewidth=1.5)     
    count = 0
    texts1 = []
    for name,lons,lats in zip(station,sta_lon,sta_lat):
        stn = list(filter(lambda a: str(name) in a,ano))
        if len(stn) != 0:   ### stn[0] = L2  & stn[1] = 3K
            p3k = pd.read_csv(INPUT_AERONET_MODIS+stn[1])            
            for n,d in enumerate(distancia[::-1]):
                b = p3k[p3k["distancia"] < d]
                x,y = m(b['longitud'],b['latitud'])
                plt.plot(x,y,marker[n]+colors[n],alpha=alpha[n],markersize=8,label=str(d))

        count = count + 1
        xx, yy = m(lons,lats)
        # Draw great circle
        ### 1 meter = 0.000539957
        ccc.shaded_great_circle(m, yy, xx,0.000539957*3000, col='k-',sizze=3.0,distan='3km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ccc.shaded_great_circle(m, yy, xx,0.000539957*15000, col='k--',sizze=3.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ccc.shaded_great_circle(m, yy, xx,0.000539957*25000, col='k',sizze=5.0,distan='25km')  # Distance specified in nautical miles, i.e. 100 nmi in this case

        plt.plot(xx, yy, 'og', markeredgecolor='black',markersize=10,label= str(count)+" -> "+str(name))
        texts1.append(plt.text(xx, yy, str(count), fontsize=15,color='k',
                               bbox={'facecolor':'orange', 'edgecolor':'none', 'alpha':0.9}))

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.15)
        aT.adjust_text(texts1,force_points=2.2, force_text=2.2, 
                       expand_points=(2,2),expand_text=(2,2), 
                       arrowprops=dict(arrowstyle="->", color='black', lw=2.2))
    #create legend
    p1 = mlines.Line2D([0],[0], color='r', marker='s', linestyle = 'None', markersize=10, label='< 3km')
    p2 = mlines.Line2D([0],[0], color='y', marker='+', linestyle = 'None', markersize=10, label='< 15km')
    p3 = mlines.Line2D([0],[0], color='b', marker='*', linestyle = 'None', markersize=10, label='< 25km')
    leg1 = ax.legend(handles=[p1,p2,p3],handletextpad=0.3,loc=2,prop={'size': 20},framealpha=1.0,facecolor="beige")
    leg1.set_title("MODIS data"+"\n"+
                   "Distance (m)", prop = {'size':23,'weight':'bold'})

    #create legend
    l1 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="1 -> "+str(station[0].replace("_"," ")))
    l2 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="2 -> "+str(station[1]))
    l3 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="3 -> "+str(station[2]))
    l4 = mlines.Line2D([0],[0],marker='o', color='g', linestyle = 'None', markeredgecolor='black',markersize=10, label="4 -> "+str(station[3].replace("_"," ")))
    leg2 = ax.legend(handles=[l1,l2,l3,l4],handletextpad=0.3,loc=4,prop={'size': 20},framealpha=1.0,facecolor="beige")
    leg2.set_title("Aeronet Stations", prop = {'size':23,'weight':'bold'})
    ax.add_artist(leg1)

    ax.set_title("Distance between MODIS algorithm and the AERONET stations"+"\n"+
                 str(i)+ " - " + str(producto[1]), fontsize=32)
    fig.savefig(OUTPUT+str(i)+'_AERONET_'+str(producto[1])+'.png',bbox_inches='tight')
    plt.show()


########################### MAIAC #####################################
station_by_ano = list(filter(lambda a: str(2016) in a,listdir1))
lats = []; lons = []; dist = []
for name,lon,lat in zip(station,sta_lon,sta_lat):
    stn = list(filter(lambda a: str(name) in a,station_by_ano))
    df= pd.read_csv(INPUT_AERONET_MAIAC+stn[0])
    lons.append(df['longitud'][0])
    lats.append(df['latitud'][0])
    dist.append(round(df["distancia"][0],2))
    
fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(111)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(3.0)
m = Basemap(projection='cyl', resolution='h',llcrnrlat=-25.0, urcrnrlat=-22.0,
            llcrnrlon=-48.0, urcrnrlon=-44.0)
m.drawmapboundary(fill_color=None)
m.fillcontinents(color='#ddaa66', lake_color='#7777ff', zorder=0)
m.drawcoastlines(linewidth=1.5)
m.drawstates(linewidth=1.5)    
m.drawparallels(np.arange(-90., 120., 1), labels=[0, 1, 0, 0],fontsize=24)
m.drawmeridians(np.arange(-180., 181., 1), labels=[0, 0, 0, 1],fontsize=24) 
m.readshapefile('../shapefile/RM_Sao_Paulo/transformed','sp')
x,y = m(lons,lats)
plt.plot(x,y,'*m',markersize=25,label='MAIAC')
count = 0
texts1 = []
for latt,long,name,dists in zip(sta_lat,sta_lon,station,dist):
    count = count + 1
    xx, yy = m(long,latt)
    plt.plot(xx, yy, 'og', markeredgecolor='black',markersize=10,label= str(count)+" -> "+str(name)+" (d = "+str(dists)+" m)")
    texts1.append(plt.text(xx, yy, str(count), fontsize=15,color='k',
                           bbox={'facecolor':'orange', 'edgecolor':'none', 'alpha':0.9}))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.15)
aT.adjust_text(texts1,force_points=2.2, force_text=2.2, 
               expand_points=(4,4),expand_text=(4,4), 
               arrowprops=dict(arrowstyle="->", color='black', lw=2.2))
l=ax.legend(handletextpad=0.3,loc=3,prop={'size': 17},framealpha=1.0,facecolor="beige")
l.set_title("Aeronet Stations", prop = {'size':20,'weight':'bold'})

ax.set_title("Distance between the nearest pixel from"+"\n"
             +"MAIAC algorithm and the AERONET stations ", fontsize=32)
