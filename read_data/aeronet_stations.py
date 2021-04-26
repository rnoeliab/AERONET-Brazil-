#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:54:03 2021

@author: noelia
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np
from netCDF4 import Dataset
from wrf import getvar
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import adjustText as aT

path_wrf = '/media/noelia/TOSHIBA EXT/doctorado/usp/modelo/WRF_model/wrf_model_wps/2_dominio/'
output = '/media/noelia/TOSHIBA EXT/doctorado/usp/modelo/figures/plot_cetesb_wrf/'
################################## DOMINIO 1 ##################################
ncfile = Dataset(path_wrf+"wrfinput_d01")
hgt = getvar(ncfile, "HGT")
data = hgt.values

lat = getvar(ncfile, "XLAT").values
lat_inver = lat[::-1]
lon = getvar(ncfile, "XLONG").values
################################## DOMINIO 2 ##################################
ncfile2 = Dataset(path_wrf+"wrfinput_d02")
hgt2 = getvar(ncfile2, "HGT")
data2 = hgt2.values

lat2 = getvar(ncfile2, "XLAT").values
lat2_inver = lat2[::-1]
lon2 = getvar(ncfile2, "XLONG").values

###################### posicion de las estaciones ###########################
sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']


levels = MaxNLocator(nbins=12).tick_values(0.0, hgt.values.max()/1000)
cmap = cm.get_cmap("terrain",lut=25)
cmap.set_bad("w")
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)


fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(111)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(3.0)
m = Basemap(projection='cyl', resolution='h', llcrnrlat=lat.min(), urcrnrlat=lat.max(),
            llcrnrlon=lon.min(), urcrnrlon=-30)
m.drawmapboundary(fill_color='#7777ff')
m.fillcontinents(color='#ddaa66', lake_color='#7777ff', zorder=0)
m.drawcoastlines(linewidth=1.5)
m.drawstates(linewidth=1.5)    
m.drawparallels(np.arange(-90., 120., 1),fontsize=22)
m.drawmeridians(np.arange(-180., 181., 1),fontsize=22) 
m.readshapefile('/media/noelia/TOSHIBA EXT/doctorado/usp/shapefile/RM_Sao_Paulo/transformed','sp')
x1,y1 = m(lon, lat)
trend1 = m.pcolormesh(x1,y1, data/1000, cmap=cmap, norm = norm)

count = 0
texts1 = []
for latt,long,name in zip(sta_lat,sta_lon,station):
    count = count + 1
    xx, yy = m(long,latt)
    plt.plot(xx, yy, 'om', markeredgecolor='black',markersize=10,label= str(count)+" -> "+str(name))
    texts1.append(plt.text(xx, yy, str(count), fontsize=10,color='k',
                           bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.9}))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.10, hspace=0.15)
aT.adjust_text(texts1,force_points=1.1, force_text=1.1, 
               expand_points=(2,2),expand_text=(2,2), 
               arrowprops=dict(arrowstyle="->", color='black', lw=1.1))

axins = zoomed_inset_axes(ax, 2.35, loc=7)
axins.set_xlim(-49, -43)
axins.set_ylim(-25, -21)
# plt.xticks(visible=False)
# plt.yticks(visible=False)
m2 = Basemap(projection='cyl', resolution='h', llcrnrlat=lat2.min(), urcrnrlat=lat2.max(),
            llcrnrlon=lon2.min(), urcrnrlon=lon2.max(),ax=axins)
m2.drawmapboundary(fill_color='#7777ff')
m2.fillcontinents(color='#ddaa66', lake_color='#7777ff', zorder=0)
m2.drawcoastlines(linewidth=1.5)
m2.drawstates(linewidth=1.5)    
m2.drawparallels(np.arange(-90., 120., 1), labels=[0, 1, 0, 0],linewidth=1.5,xoffset=0.1,fontsize=22)
m2.drawmeridians(np.arange(-180., 181., 1), labels=[0, 0, 0, 1],linewidth=1.5,yoffset=0.12,fontsize=22) 
m2.readshapefile('/media/noelia/TOSHIBA EXT/doctorado/usp/shapefile/RM_Sao_Paulo/transformed','sp')
x2,y2 = m2(lon2, lat2)
trend2 = m2.pcolormesh(x2,y2, data2/1000, cmap=cmap, norm = norm)

count = 0
texts1 = []
for latt,long,name in zip(sta_lat,sta_lon,station):
    count = count + 1
    xx, yy = m(long,latt)
    plt.plot(xx, yy, 'om', markeredgecolor='black',markersize=15,label= str(count)+" -> "+str(name))
    texts1.append(plt.text(xx, yy, str(count), fontsize=15,color='k',
                           bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.9}))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.2)
aT.adjust_text(texts1,force_points=1.1, force_text=1.1, 
               expand_points=(4,4),expand_text=(4,4), 
               arrowprops=dict(arrowstyle="->", color='black', lw=2.2))
cbar = m.colorbar(trend1, location='bottom', ax=ax, pad="9%", ticks=levels)
cbar.set_label('Height (km)', labelpad=30, fontsize=30)
cbar.ax.tick_params(labelsize=30) 
l=ax.legend(handletextpad=0.1,loc=3,prop={'size': 14})
l.set_title("Aeronet Stations", prop = {'size':17,'weight':'bold'})
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", lw=3, ec="r")

fig.savefig(output+'area_study.png',bbox_inches='tight')
plt.show()
