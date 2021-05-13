# AERONET-Brazil-

![Alt text](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/figures/area_study.png)

## Comparison between AERONET and MODIS sensor

* Here we are going to compare the in-situ data from several AERONET stations (point data) with the satellite data (in this case Terra and Aqua). 
* Therefore we are going to carry out some steps: 
### First, extract and read the AERONET data 
* In the folder [data_aeronet](https://github.com/rnoeliab/AERONET-Brazil-/tree/main/data_aeronet), I am providing the AOD data for four AERONET stations in the northeast of Sao Paulo.
* In the folder [read_data/AERONET](https://github.com/rnoeliab/AERONET-Brazil-/tree/main/read_data/AERONET) there are three scripts to read the AERONET data, plot the time series and display the stations in the domain. 
    - The [read_aeronet.py](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/read_data/AERONET/read_aeronet.py) script will read the data downloaded from the [AERONOET](https://aeronet.gsfc.nasa.gov/cgi-bin/draw_map_display_aod_v3) website. In it, the AOD values for seven wavelengths will be considered and the AOD values for 550 nm will be calculated. That data will be saved and created with a different name "year_station_AOD.csv". 

![Alt text](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/figures/stations.jpg)

### Second, extract and read the SATELLITE data 
* For this step, we are going to remember a bit how to obtain the MODIS data explained in the repository [Satellite-WRF-Model](https://github.com/rnoeliab/Satellite-WRF-Model). At the end of the download, we will use the script [modis_aod_local.py](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/read_data/MODIS_MAIAC_AERONET/modis_aod_local.py) to extract the AOD values for a specific point.

* Importing the libraries, for that it is necessary to install all the libraries that python needs to run the script. 
```
 conda install -c conda-forge pyhdf 
 conda install -c conda-forge pyproj 
 conda install -c trentonoliphant datetime 
 ```
 ```python
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import os
from datetime import datetime
import glob
import re
import pyproj
import time
import calendar
```
 
* Extracting the AOD values for a certain position, only select a product of the MODIS sensor:
```
POINTS:
sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

PRODUCTS of MODIS sensor:
#var_name = 'AOD_550_Dark_Target_Deep_Blue_Combined'   ## (1)
#var_name = 'Optical_Depth_Land_And_Ocean'              ## (2)   
#var_name = 'Deep_Blue_Aerosol_Optical_Depth_550_Land'  ## (3)
```
* Here we are going to sort the MODIS files to read by resolution, product and year in each AERONET station:
``` python
#open several data
INPUT_PATH = '../imagen_data/modis/DATA/'
listdir = os.listdir(INPUT_PATH)

for user_lat,user_lon,name_station in zip(sta_lat,sta_lon,station):
    for k in range(len(listdir)):    #### 3K  and 10K
        if listdir[k] == "3K":
            var_name = 'Optical_Depth_Land_And_Ocean'
            name = "DT_AOD"
            input_modis = INPUT_PATH+listdir[k]+"/"
            for ano in range(2014,2021,1):
                input_modis = INPUT_PATH+str(listdir[k])+"/"+str(ano)+"/"
                print(input_modis)
                list_mod = os.listdir(input_modis) 
                dim=len(list_mod)
                order=sorted(list_mod, key=str.lower)
                mylist=[]
                listdirr = []
                time_serie = pd.DataFrame({'IP':[]})
                for i in range(len(order)):
                    if i == (len(order)-1):
                        break;      
                    else:
                        if order[i][0:17] == order[i + 1][0:17]:
                            listdirr.append(order[i])          
                            if i == (len(order)-2):
                                listdirr.append(order[len(order)-1])
                                mylist.append(listdirr)               
                        else:
                            listdirr.append(order[i])
                            mylist.append(listdirr)
                            listdirr = []
                count=0
                for n in range(len(mylist)):
                    for FILE_NAME in mylist[n]:
                        FILE_NAME=FILE_NAME.strip()                                       
                        hdf = SD(input_modis+FILE_NAME, SDC.READ)
                        ...
```
* Then, we going to extract the latitudes, longitudes, times and AOD data.
* Calculating the shortest distance between two points, using the haversine formula:

```python
R=6371000  ## Radius of the earth in meters 
lat1=np.radians(user_lat)
lat2=np.radians(latitude)
delta_lat=np.radians(latitude-user_lat)
delta_lon=np.radians(longitude-user_lon)
a=(np.sin(delta_lat/2))*(np.sin(delta_lat/2))+(np.cos(lat1))*(np.cos(lat2))*(np.sin(delta_lon/2))*(np.sin(delta_lon/2))
c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
d=R*c 
```
* After, let's calculate the appropriate position of the closest distance:
```python
x,y=np.unravel_index(d.argmin(),d.shape) 
print('the pixel closest to the entered point is: Latitude:', latitude[x,y], 'longitude:', longitude[x,y])
```
* Now, the UTC and local time, latitude, longitude, AOD data and distance will be stored:
```python
if scan_time[x,y] == 0.0:
    scan_time[x,y] = scan_time.max()
time_serie.loc[count,'scan_time'] = scan_time[x,y]
# temp=time.gmtime(scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC')))   ### UTC time
temp=scan_time[x,y]+calendar.timegm(time.strptime('Dec 31, 1992 @ 23:59:59 UTC','%b %d, %Y @ %H:%M:%S UTC'))   ### timestamps utc
time_serie.loc[count,'year'] = datetime.fromtimestamp(temp).strftime('%Y')  ## Local Time
time_serie.loc[count,'month'] = datetime.fromtimestamp(temp).strftime('%m')
time_serie.loc[count,'day'] = datetime.fromtimestamp(temp).strftime('%d')
time_serie.loc[count,'hour'] = datetime.fromtimestamp(temp).strftime('%H')
time_serie.loc[count,'min'] = datetime.fromtimestamp(temp).strftime('%M')
time_serie.loc[count,'sec'] = datetime.fromtimestamp(temp).strftime('%S')
time_serie.loc[count,'distancia'] = d[x,y]
time_serie.loc[count,'latitud'] = latitude[x,y]
time_serie.loc[count,'longitud'] = longitude[x,y]                
time_serie.loc[count,'AOD'] = round(data[x,y]*scale_factor,3)
```
* If the AOD = fillvalue, then the AOD value will be calculated with the neighboring pixels, considering an area of 3x3, in which the Fillvalue pixel is in the center. 
```ptyhon
if x < 1:
    x+=1
if x > data.shape[0]-2:
    x-=2
if y < 1:
    y+=1
if y > data.shape[1]-2:
    y-=2
three_by_three=data[x-1:x+2,y-1:y+2]
three_by_three=three_by_three.astype(float)
three_by_three[three_by_three==float(fillvalue)]=np.nan
nnan=np.count_nonzero(~np.isnan(three_by_three))
time_serie.loc[count,'count 3x3'] = nnan
if nnan==0:
    print('There are no valid pixels on a 3x3 grill in the given location')
    time_serie.loc[count,'AOD 3x3 mean'] = np.nan
    count=count+1
else:
    three_by_three=three_by_three*scale_factor
    three_by_three_average=np.nanmean(three_by_three)
    three_by_three_std=np.nanstd(three_by_three)
    three_by_three_median=np.nanmedian(three_by_three)
    if nnan==1:
        npixels='is'
        mpixels='pixel'
    else:
        npixels='are'
        mpixels='pixels'
    time_serie.loc[count,'AOD 3x3 mean'] = three_by_three_average
    time_serie.loc[count,'AOD_std'] = three_by_three_std
    time_serie.loc[count,'AOD_median'] = three_by_three_median
    count=count+1
```
* Finally, the stored data will be saved:
```python
time_serie.to_csv(OUT_PATH+FILE_NAME[10:14]+"_"+name+"_"+FILE_NAME[6:8]+"_MODIS_"+str(name_station)+".csv", index=False)
```

### Third, Compare both data (AERONET and Satellite)
```python
INPUT_AERONET ="../in-situ/aeronet/AOD/"
INPUT_MODIS = "../modis/results/mod_local/"
OUTPUT = "../modis/results/aero_mod/"

listdir_aero = os.listdir(INPUT_AERONET)
listdir_modis = os.listdir(INPUT_MODIS)

for m in listdir_aero:
    for n in listdir_modis:  
        if m[0:4] in n:       ### select the year  
            if m[5:-8] in n:
                aer = pd.read_csv(INPUT_AERONET+m)
                mod = pd.read_csv(INPUT_MODIS+n)
```
* Use,  `mod["year"] = mod["year"].astype(int).astype(str)` for "year,month,day,hour,min and sec".
* This script is important because it selects the AOD data from the AERONET stations with a time of 60, 30 and 15 minutes before and after the passage of the MODIS sensor: 
```python
for k in range(len(aer)):
    ####  group by day
    if (modis["year"][j]+"-"+modis["month"][j]+"-"+modis["day"][j] == aer["Date(dd:mm:yyyy)"][k][6:10]+"-"+aer["Date(dd:mm:yyyy)"][k][3:5]+"-"+aer["Date(dd:mm:yyyy)"][k][0:2]):                                               
        print("same day:", modis["day"][j] + "-" + modis["month"][j] + "-" + modis["year"][j])
        ### group by 60 minutes
        cal = (float(modis["hour"][j])*60+float(modis["min"][j])) - (float(aer["Time(hh:mm:ss)"][k][0:2])*60+float(aer["Time(hh:mm:ss)"][k][3:5]))
        if -60 <= cal and cal <=60:
            print('less the +-60 min')
            date_aer.append(aer["AOD_550nm-AOD"][k])
            data.loc[j,"time_+-60_min_aero"] = aer["Time(hh:mm:ss)"][k]
        prom = np.nanmean(date_aer)
        data.loc[j, "prom_60_min_AOD_aero"] = prom
        #### group by 30 minutes
        if -30<=cal and cal<=30:
            print('less the +-30 min')
            minu_30_aer.append(aer["AOD_550nm-AOD"][k])
            data.loc[j,"time_+-30_min_aero"] = aer["Time(hh:mm:ss)"][k]
        prom_30_minu = np.nanmean(minu_30_aer)
        data.loc[j, "prom_30_min_AOD_aero"] = prom_30_minu
        #### group by 15 minutes
        if -15<=cal and cal<=15:
            print('less the +-15 min')
            minu_15_aer.append(aer["AOD_550nm-AOD"][k])
            data.loc[j,"time_+-15_min_aero"] = aer["Time(hh:mm:ss)"][k]
        prom_15_minu = np.nanmean(minu_15_aer)
        data.loc[j, "prom_15_min_AOD_aero"] = prom_15_minu
data['AOD modis'][data['AOD modis']<0.0] = np.nan
data['AOD 3x3 mean'][data['AOD 3x3 mean']<0.0] = np.nan

data.to_csv(OUTPUT+n[0:-4] + "_AERONET.csv", index=None)           
```           
### Finally, Analysis both data (AERONET and Satellite)

![Alt text](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/figures/Sao_Paulo_3K_DT_AOD_terra.png)
![Alt text](https://github.com/rnoeliab/AERONET-Brazil-/blob/main/figures/Sao_Paulo_3K_DT_AOD_aqua.png)







