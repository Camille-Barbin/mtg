# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 10:12:14 2025

@author: Camille
"""


import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

#%%
pd.options.mode.copy_on_write=True

# Reads in population dataset and sets the fips codes as strings
pop_file="../Inputs/population-change-block-group-decadal-all.csv"
fips={"geography":str}
pop_raw=pd.read_csv(pop_file,dtype=fips)

#%%
# Breaks up the population data set into separate files by SSP and year and unstacks
# the data so there is a population column for each SLR and migration scenario
# within each file
ssps=pop_raw["ssp"].unique()
years=pop_raw["elapsed_year"].unique()
for ssp in ssps:
    for year in years:
        keepssp=pop_raw["ssp"]==ssp
        keepyr=pop_raw["elapsed_year"]==year
        both=keepssp & keepyr
        pop=pop_raw[both]
        pop["varname"]=pop["migration"]+"_"+pop["scenario_name"]
        trim=pop[["value_05","value_50","value_95"]]
        trim["GEOID"]=pop["geography"]
        trim["varname"]=pop["varname"]
        trim=trim.set_index(["GEOID","varname"])
        trim=trim.stack().reset_index()
        trim["varname"]=trim["varname"]+trim["level_2"].str[-3:]
        trim=trim.set_index(["GEOID","varname"])[0]
        trim=trim.unstack()
        trim.to_pickle(f"ssp{ssp}_eyear{year}.pkl")
        print("wrote ssp+year",ssp,year)

