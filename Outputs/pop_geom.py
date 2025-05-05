# -*- coding: utf-8 -*-
"""
Created on Sun May  4 18:04:39 2025

@author: Camille
"""

import pandas as pd
import geopandas as gpd

outfile="MTG.gpkg"
outlayer_h="Population_High_SSP2"
outlayer_l="Population_Low_SSP2"

# Reads in data files
bg=gpd.read_file("../Inputs/cb_2019_22_bg_500k.zip",dtype={"GEOID:str"})
pop_52=pd.read_pickle("ssp2_eyear52.pkl")
pop_12=pd.read_pickle("ssp2_eyear12.pkl")

# Sets projection
utm15n=26915

#%%
# Merges population sets after filtering down to desired scenarios
pop_52=pop_52[["BASE_Higher_50","BASE_Lower_50"]]
pop_12=pop_12[["BASE_Higher_50","BASE_Lower_50"]]
pop_merge=pop_52.merge(pop_12, on="GEOID", how="outer",validate='1:1', indicator=True, suffixes=('_52', '_12'))
print(pop_merge["_merge"].value_counts())
pop_merge=pop_merge.drop(columns="_merge")

#%%
# Merges population onto block group geometries
pop_merge=bg.merge(pop_merge, on="GEOID", how="inner",validate='1:1', indicator=True)
print(pop_merge["_merge"].value_counts()) 
pop_merge=pop_merge.drop(columns="_merge")

#%%
# Separates pop geodataframe into high and low scenarios
pop_high=pop_merge[["GEOID","BASE_Higher_50_52","BASE_Higher_50_12","geometry"]]
pop_low=pop_merge[["GEOID","BASE_Lower_50_52","BASE_Lower_50_12","geometry"]]
pop_high=pop_high.set_index("GEOID")
pop_low=pop_low.set_index("GEOID")

#%%
# Reprojects dataframes
pop_high=pop_high.to_crs(epsg=utm15n)
pop_low=pop_low.to_crs(epsg=utm15n)

#%%
# Writes dataframes to geopackage layers
pop_high.to_file(outfile,layer=outlayer_h)
pop_low.to_file(outfile,layer=outlayer_l)