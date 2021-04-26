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
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import adjustText as aT

INPUT_AERONET_MODIS = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_mod/"
INPUT_AERONET_MAIAC = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/aero_maiac/"
listdir = os.listdir(INPUT_AERONET_MODIS)
listdir =sorted(listdir, key=str.lower)
listdir1 = os.listdir(INPUT_AERONET_MAIAC)
listdir1 =sorted(listdir1, key=str.lower)

OUTPUT = "/media/noelia/TOSHIBA EXT/doctorado/usp/imagen_data/modis/results/plot_Aero_550/distancia/"

sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

producto = ['L2','3K']
colors = ['r','m','b','g']
marker = ['*','+','s','v']
alpha = [0.8,0.6,0.4,0.2]
distancia = [3000.0,15000.0,25000.0,50000.0]
######################################### MODIS TOTAL ##########################
for i in np.arange(2014,2020,1):
    ano = list(filter(lambda a: str(i) in a,listdir))
    fig = plt.figure(figsize=(20,18))
    ax=plt.axes()
    m = Basemap(projection='cyl', resolution='h',llcrnrlat=-25.0, urcrnrlat=-22.0,
                llcrnrlon=-48.0, urcrnrlon=-44.0)
    m.drawcoastlines(linewidth=1.5)
    m.drawstates(linewidth=1.5)    
    m.drawparallels(np.arange(-90., 120., 1), labels=[1, 0, 0, 0],fontsize=23)
    m.drawmeridians(np.arange(-180., 181., 1), labels=[0, 0, 0, 1],fontsize=23) 
    m.readshapefile('/media/noelia/TOSHIBA EXT/doctorado/usp/shapefile/RM_Sao_Paulo/transformed','sp')     
    for name,lons,lats in zip(station,sta_lon,sta_lat):
        stn = list(filter(lambda a: str(name) in a,ano))
        if len(stn) != 0:   ### stn[0] = L2  & stn[1] = 3K
            pl2 = pd.read_csv(INPUT_AERONET_MODIS+stn[0])
            p3k = pd.read_csv(INPUT_AERONET_MODIS+stn[0])            
            for n,d in enumerate(distancia):
                b = pl2[pl2["distancia"] < d]
                x,y = m(b['longitud'],b['latitud'])
                plt.plot(x,y,marker[n]+colors[n],alpha=alpha[n],markersize=8,label=str(producto[0]))
        x0,y0 = m(lons, lats)
        plt.plot(x0,y0,'black',marker='o',markersize=10,label=str(name).replace('_',' '))







            plt.legend(bbox_to_anchor=(1., 0, 0.1,0.8),loc=0, prop={'size': 20})
            ax.set_title(str(i)+" MODIS " + str(name).replace('_',' ') + " AERONET", fontsize=26)
#            fig.savefig(OUTPUT+str(i)+"_"+str(name)+'_MODIS.png',bbox_inches='tight')
            plt.show()

def calc_new_coord(lat1, lon1, rad, dist):
    """
    Calculate coordinate pair given starting point, radial and distance
    Method from: http://www.geomidpoint.com/destination/calculation.html
    Note: the variable 'flat' below represents the earth's polar flattening 
    used in various ellipsoid models. For the commonly used WGS-84, 
    let flat = 298.257223563
    """
    flat = 298.257223563
    a = 2 * 6378137.00
    b = 2 * 6356752.3142

    # Calculate the destination point using Vincenty's formula
    f = 1 / flat
    sb = np.sin(rad)
    cb = np.cos(rad)
    tu1 = (1 - f) * np.tan(lat1)
    cu1 = 1 / np.sqrt((1 + tu1*tu1))
    su1 = tu1 * cu1
    s2 = np.arctan2(tu1, cb)
    sa = cu1 * sb
    csa = 1 - sa * sa
    us = csa * (a * a - b * b) / (b * b)
    A = 1 + us / 16384 * (4096 + us * (-768 + us * (320 - 175 * us)))
    B = us / 1024 * (256 + us * (-128 + us * (74 - 47 * us)))
    s1 = dist / (b * A)
    s1p = 2 * np.pi

    while (abs(s1 - s1p) > 1e-12):
        cs1m = np.cos(2 * s2 + s1)
        ss1 = np.sin(s1)
        cs1 = np.cos(s1)
        ds1 = B * ss1 * (cs1m + B / 4 * (cs1 * (- 1 + 2 * cs1m * cs1m) - B / 6 * \
            cs1m * (- 3 + 4 * ss1 * ss1) * (-3 + 4 * cs1m * cs1m)))
        s1p = s1
        s1 = dist / (b * A) + ds1

    t = su1 * ss1 - cu1 * cs1 * cb
    lat2 = np.arctan2(su1 * cs1 + cu1 * ss1 * cb, (1 - f) * np.sqrt(sa * sa + t * t))
    l2 = np.arctan2(ss1 * sb, cu1 * cs1 - su1 * ss1 * cb)
    c = f / 16 * csa * (4 + f * (4 - 3 * csa))
    l = l2 - (1 - c) * f * sa * (s1 + c * ss1 * (cs1m + c * cs1 * (-1 + 2 * cs1m * cs1m)))
    d = np.arctan2(sa, -t)
    finaltc = d + 2 * np.pi
    backtc = d + np.pi
    lon2 = lon1 + l

    return (np.rad2deg(lat2), np.rad2deg(lon2))


def shaded_great_circle(m, lat_0, lon_0, dist=100, alpha=0.2, col='k',sizze='2.0',distan='5km'):  # dist specified in nautical miles
    dist = dist * 1852  # Convert distance to nautical miles
    theta_arr = np.linspace(0, np.deg2rad(360), 100)
    lat_0 = np.deg2rad(lat_0)
    lon_0 = np.deg2rad(lon_0)

    coords_new = []

    for theta in theta_arr:
        coords_new.append(calc_new_coord(lat_0, lon_0, theta, dist))

    lat = [item[0] for item in coords_new]
    lon = [item[1] for item in coords_new]

    x, y = m(lon, lat)
    m.plot(x, y, col,linewidth = sizze,label=distan)

for i in np.arange(2014,2021,1):
    ano = list(filter(lambda a: str(i) in a,listdir))
    fig = plt.figure(figsize=(25,15))
    name,lons,lats = station[0],sta_lon[0],sta_lat[0]
    stn = list(filter(lambda a: str(name) in a,ano))
    if len(stn) != 0:
        ax = fig.add_subplot(221)
        m = Basemap(projection='cyl', resolution='h',llcrnrlat=-24.0, urcrnrlat=-23.0,
                    llcrnrlon=-47.5, urcrnrlon=-45.5,ax =ax)
        m.drawcoastlines(linewidth=1.5)
        m.drawstates(linewidth=1.5)    
        m.drawparallels(np.arange(-90., 120., 0.2), labels=[1, 0, 0, 0],fontsize=25)
        m.drawmeridians(np.arange(-180., 181., 0.5), labels=[0, 0, 0, 1],fontsize=25) 
        m.readshapefile('/data/noelia/shapefile/RM_Sao_Paulo/transformed','sp')
        for j in range(len(stn)):
            df= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            x,y = m(df['longitud'],df['latitud'])
            plt.plot(x,y,'*'+colors[j],alpha=0.5,markersize=11,label=str(producto[j]))
        x0,y0 = m(lons, lats)
        plt.plot(x0,y0,'black',marker='o',markersize=5)
        # Draw great circle
        ### 1 meter = 0.000539957
        shaded_great_circle(m, y0, x0,0.000539957*5000, col='k-',sizze=3.0,distan='5km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*10000, col='k--',sizze=3.0,distan='10km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*15000, col='red',sizze=5.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ax.set_title(str(i)+" MODIS " + str(name).replace('_',' ') + " AERONET", fontsize=25)
    name,lons,lats = station[1],sta_lon[1],sta_lat[1]
    stn = list(filter(lambda a: str(name) in a,ano))
    if len(stn) != 0:
        ax = fig.add_subplot(222)
        m = Basemap(projection='cyl', resolution='h',llcrnrlat=-23.0, urcrnrlat=-22.0,
            llcrnrlon=-46.0, urcrnrlon=-44.0,ax =ax)
        m.drawcoastlines(linewidth=1.5)
        m.drawstates(linewidth=1.5)    
        m.drawparallels(np.arange(-90., 120., 0.2), labels=[1, 0, 0, 0],fontsize=25)
        m.drawmeridians(np.arange(-180., 181., 0.5), labels=[0, 0, 0, 1],fontsize=25) 
        m.readshapefile('/data/noelia/shapefile/RM_Sao_Paulo/transformed','sp')
        for j in range(len(stn)):
            df= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            x,y = m(df['longitud'],df['latitud'])
            plt.plot(x,y,'*'+colors[j],alpha=0.5,markersize=11,label=str(producto[j]))
        x0,y0 = m(lons, lats)
        plt.plot(x0,y0,'black',marker='o',markersize=5)
        # Draw great circle
        ### 1 meter = 0.000539957
        shaded_great_circle(m, y0, x0,0.000539957*5000, col='k-',sizze=3.0,distan='5km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*10000, col='k--',sizze=3.0,distan='10km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*15000, col='red',sizze=5.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ax.set_title(str(i)+" MODIS " + str(name).replace('_',' ') + " AERONET", fontsize=25)
    name,lons,lats = station[2],sta_lon[2],sta_lat[2]
    stn = list(filter(lambda a: str(name) in a,ano))
    if len(stn) != 0:
        ax = fig.add_subplot(223)
        m = Basemap(projection='cyl', resolution='h',llcrnrlat=-24.0, urcrnrlat=-23.0,
                    llcrnrlon=-47.5, urcrnrlon=-45.5,ax =ax)
        m.drawcoastlines(linewidth=1.5)
        m.drawstates(linewidth=1.5)    
        m.drawparallels(np.arange(-90., 120., 0.2), labels=[1, 0, 0, 0],fontsize=25)
        m.drawmeridians(np.arange(-180., 181., 0.5), labels=[0, 0, 0, 1],fontsize=25) 
        m.readshapefile('/data/noelia/shapefile/RM_Sao_Paulo/transformed','sp')
        for j in range(len(stn)):
            df= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            x,y = m(df['longitud'],df['latitud'])
            plt.plot(x,y,'*'+colors[j],alpha=0.5,markersize=11,label=str(producto[j]))
        x0,y0 = m(lons, lats)
        plt.plot(x0,y0,'black',marker='o',markersize=5)
        # Draw great circle
        ### 1 meter = 0.000539957
        shaded_great_circle(m, y0, x0,0.000539957*5000, col='k-',sizze=3.0,distan='5km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*10000, col='k--',sizze=3.0,distan='10km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*15000, col='red',sizze=5.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ax.set_title(str(i)+" MODIS " + str(name).replace('_',' ') + " AERONET", fontsize=25)
    name,lons,lats = station[3],sta_lon[3],sta_lat[3]
    stn = list(filter(lambda a: str(name) in a,ano))
    if len(stn) != 0:
        ax = fig.add_subplot(224)
        m = Basemap(projection='cyl', resolution='h',llcrnrlat=-23.0, urcrnrlat=-22.0,
                    llcrnrlon=-46.0, urcrnrlon=-44.0,ax =ax)
        m.drawcoastlines(linewidth=1.5)
        m.drawstates(linewidth=1.5)    
        m.drawparallels(np.arange(-90., 120., 0.2), labels=[1, 0, 0, 0],fontsize=25)
        m.drawmeridians(np.arange(-180., 181., 0.5), labels=[0, 0, 0, 1],fontsize=25) 
        m.readshapefile('/data/noelia/shapefile/RM_Sao_Paulo/transformed','sp')
        for j in range(len(stn)):
            df= pd.read_csv(INPUT_AERONET_MODIS+stn[j])
            x,y = m(df['longitud'],df['latitud'])
            plt.plot(x,y,'*'+colors[j],alpha=0.5,markersize=11,label=str(producto[j]))
        x0,y0 = m(lons, lats)
        plt.plot(x0,y0,'black',marker='o',markersize=5)
        # Draw great circle
        ### 1 meter = 0.000539957
        shaded_great_circle(m, y0, x0,0.000539957*5000, col='k-',sizze=3.0,distan='5km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*10000, col='k--',sizze=3.0,distan='10km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        shaded_great_circle(m, y0, x0,0.000539957*15000, col='red',sizze=5.0,distan='15km')  # Distance specified in nautical miles, i.e. 100 nmi in this case
        ax.set_title(str(i)+" MODIS " + str(name).replace('_',' ') + " AERONET", fontsize=25)
    plt.legend(title="Legend",bbox_to_anchor=(1., 0.1, 0.1,1.0), prop={'size': 20},title_fontsize=30)
    fig.savefig(OUTPUT+str(i)+'_MODIS_rmsp.png',bbox_inches='tight')
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
m.readshapefile('/media/noelia/TOSHIBA EXT/doctorado/usp/shapefile/RM_Sao_Paulo/transformed','sp')
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
fig.savefig(OUTPUT+'2014_2019_AERONET_MAIAC.png',bbox_inches='tight')
plt.show()
