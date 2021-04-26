#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:56:45 2019

@author: noelia
"""

###############################################################################
### From the downloaded data from the AERONET station, choose the column of  ##
###        AOD-500 for each season and for each year of 2014 - 2019.         ##
###              After using this algorithm use modis_aeronet.py             ##
############################################################################### 

import pandas as pd
import numpy as np
from glob import glob
import zipfile

########################## decompressing the data  ##########################
input_path = "../in-situ/aeronet/data_original/"
out_path = "../in-situ/aeronet/data/"
df = sorted(glob(input_path+"*.zip"), key=str.lower)

# for i in df:
#     with zipfile.ZipFile(i, 'r') as zip_ref:
#         zip_ref.extractall(out_path)

############################# read the data ################################
listdir = sorted(glob(out_path+"*.tot_lev*"), key=str.lower)
OUTPUT = "../in-situ/aeronet/"

columns_name = ["340","380","440","500","675","870","1020"]

######################## separating the seasons  #############################
station = ['Sao_Paulo','Itajuba','SP_EACH','Cachoeira_Paulista','SP-EACH']
for i, n in enumerate(listdir, start=0):
    print(n)
########################### open the files #############################
    with open(n,"r") as f:
        dat=f.readlines()
    information = dat[6].split(",")
    df = pd.DataFrame([information])    ### READ DATA IN EXCEL FORMAT
    for j in range(7,len(dat)):
        inf = dat[j].split(",")
        df.loc[j-6] = inf
    name = df.loc[0]
    a = df[0::].drop(df.index[0:1])
    a = a.reset_index()
    a = a[np.arange(0,len(information))]
    a.columns = information
    tau = pd.DataFrame(columns=columns_name)
    tau["340"] = a["AOD_340nm-AOD"]
    tau["380"] = a["AOD_380nm-AOD"]
    tau["440"] = a["AOD_440nm-AOD"]
    tau["500"] = a["AOD_500nm-AOD"]
    tau["675"] = a["AOD_675nm-AOD"]
    tau["870"] = a["AOD_870nm-AOD"]
    tau["1020"] = a["AOD_1020nm-AOD"]        
#        data = data.convert_objects(convert_numeric=True)
    tau[tau==-999] = np.nan
    tau = tau.astype(float)
########################### calculate AOD in 550nm ###########################
    for t in range(tau.shape[0]):
        tau.loc[t,"anstrom"] = np.log(tau["340"][t]/tau["1020"][t])/np.log(1020.0/340.0)
        tau.loc[t,"550"] = tau["500"][t]*np.power((550.0/500.0),-1*tau["anstrom"][t])
    
    tau.to_csv(OUTPUT + "interpolacao_550/" + n[35:39] + "_" + n[53:-10] + "_550_interpolation.csv", index=None)
    
    aod=a[["Date(dd:mm:yyyy)", "Time(hh:mm:ss)"]]        
    aod["AOD_550nm-AOD"] = tau["550"]
    aod.to_csv(OUTPUT + "AOD/" + n[35:39] + "_" +n[53:-10]+ "_AOD.csv", index=None)
