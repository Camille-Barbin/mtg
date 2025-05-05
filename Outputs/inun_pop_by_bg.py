# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 12:29:49 2025

@author: Camille
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import seaborn as sns

outgeofile="MTG.gpkg"
outlayer_h="Inundation_by_population_highSLR"
outpkl_h="Inundation_by_population_highSLR.pkl"

outlayer_l="Inundation_by_population_lowSLR"
outpkl_l="Inundation_by_population_lowSLR.pkl"

#%%
# Reads in data for population and inundation points
pop_high=gpd.read_file("MTG.gpkg",layer="Population_High_SSP2")
pop_low=gpd.read_file("MTG.gpkg", layer="Population_Low_SSP2")

inun_high=gpd.read_file("MTG.gpkg", layer="Inundation_Points_High")
inun_low=gpd.read_file("MTG.gpkg",layer="Inundation_Points_Low")

#%%
# Spatial join of block groups and extraction points 
bg_high=pop_high.sjoin(inun_high,how='left',predicate='contains')

bg_low=pop_low.sjoin(inun_low,how='left',predicate='contains')

#%%
# Renaming and dropping columns in joined dataframes
rename_inunh={'value_12_high':'inun_12', 'value_52_high':'inun_52'}
bg_high=bg_high.rename(columns=rename_inunh)
bg_high=bg_high.drop(columns='index_right')
bg_high=bg_high.dropna()

rename_inunl={'value_12_low':'inun_12', 'value_52_low':'inun_52'}
bg_low=bg_low.rename(columns=rename_inunl)
bg_low=bg_low.drop(columns='index_right')
bg_low=bg_low.dropna()

#%%
# Finds inundation points with flood levels greater than half a meter
thresh=0.5
bg_high["flooded_12"]=(bg_high["inun_12"]>thresh).astype(int)
bg_high["flooded_52"]=(bg_high["inun_52"]>thresh).astype(int)
bg_low["flooded_12"]=(bg_low["inun_12"]>thresh).astype(int)
bg_low["flooded_52"]=(bg_low["inun_52"]>thresh).astype(int)

#%%
# Groups by block groups and finds the percent of each block group flooded
# more than 0.5 meters
high_grouped=bg_high.groupby("GEOID")
low_grouped=bg_low.groupby("GEOID")

points_bgh=high_grouped.size()
points_bgl=low_grouped.size()

flood_pct_high=pd.DataFrame()
flood_pct_low=pd.DataFrame()

flood_pct_high["flood_pct_12"]=high_grouped["flooded_12"].sum()/points_bgh*100
flood_pct_high["flood_pct_52"]=high_grouped["flooded_52"].sum()/points_bgh*100
flood_pct_low["flood_pct_12"]=low_grouped["flooded_12"].sum()/points_bgl*100
flood_pct_low["flood_pct_52"]=low_grouped["flooded_52"].sum()/points_bgl*100

#%%
# Merges percent flooded data with population data for each SLR scenario
inun_pop_high=pop_high.merge(flood_pct_high, on="GEOID", how="outer", validate="1:1")
inun_pop_low=pop_low.merge(flood_pct_low, on ="GEOID", how="outer", validate="1:1")

# Renames population columns
rename_poph={'BASE_Higher_50_52':'pop_52','BASE_Higher_50_12':'pop_12'}
inun_pop_high=inun_pop_high.rename(columns=rename_poph)

rename_popl={'BASE_Lower_50_52':'pop_52','BASE_Lower_50_12':'pop_12'}
inun_pop_low=inun_pop_low.rename(columns=rename_popl)


#%%
# Finds change in population and change in inundation from year 12 (2035) to 
# year 52 (2055)
inun_pop_high["pop_change"]=inun_pop_high["pop_52"]/inun_pop_high["pop_12"]
inun_pop_high["flood_change"]=inun_pop_high["flood_pct_52"]-inun_pop_high["flood_pct_12"]

inun_pop_low["pop_change"]= inun_pop_low["pop_52"]/inun_pop_low["pop_12"]
inun_pop_low["flood_change"]=inun_pop_low["flood_pct_52"]-inun_pop_low["flood_pct_12"]

#%%
# Finds population difference between high and low sea level rise scenario
pop_difference=inun_pop_high["pop_change"]-inun_pop_low["pop_change"]
flood_difference=inun_pop_high["flood_change"]-inun_pop_low["flood_change"]

#%%
# Drops rows with zero population in 12 or 52
inun_pop_high=inun_pop_high[(inun_pop_high["pop_12"]!=0) & (inun_pop_high["pop_52"]!=0)]
inun_pop_low=inun_pop_low[(inun_pop_low["pop_12"]!=0) & (inun_pop_low["pop_52"]!=0)]

#%%
# Drops block groups with missing values for inundation
inun_pop_low=inun_pop_low.dropna()
inun_pop_high=inun_pop_high.dropna()

#%%
# Writes inun_pop dataframes out to geopackages, drops the geometry, and writes
# the dataframes to pickle files for the regression
inun_pop_high.to_file(outgeofile, layer=outlayer_h)
inun_pop_low.to_file(outgeofile,layer=outlayer_l)

inun_pop_high=inun_pop_high.drop(columns="geometry")
inun_pop_low=inun_pop_low.drop(columns="geometry")

inun_pop_high.to_pickle(outpkl_h)
inun_pop_low.to_pickle(outpkl_l)
