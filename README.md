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
¨¨¨python

¨¨¨

### Third, Compare both data (AERONET and Satellite)
*
### Finally, Analysis both data (AERONET and Satellite)

