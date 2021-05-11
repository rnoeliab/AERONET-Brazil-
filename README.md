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
 
* Before extracting the AOD values for a certain position, the MODIS sensor data will have to be reprojected, from sinusoidal coordinate to vertical coordinate, 

```
POINTS:
sta_lat, sta_lon = ([-23.561,-22.413,-23.482,-22.689],[-46.735,-45.452,-46.500,-45.006])
station = ['Sao_Paulo','Itajuba','SP-EACH','Cachoeira_Paulista']

PRODUCTS of MODIS sensor:
#var_name = 'AOD_550_Dark_Target_Deep_Blue_Combined'   ## (1)
#var_name = 'Optical_Depth_Land_And_Ocean'              ## (2)   
#var_name = 'Deep_Blue_Aerosol_Optical_Depth_550_Land'  ## (3)

For both resolutions, in listdir, we have stored all the data *hdf 
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


```
* 

### Third, Compare both data (AERONET and Satellite)
*
### Finally, Analysis both data (AERONET and Satellite)

