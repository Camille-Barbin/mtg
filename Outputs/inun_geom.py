# -*- coding: utf-8 -*-
"""
Created on Sun May  4 18:08:03 2025

@author: Camille
"""

import pandas as pd
import geopandas as gpd

outfile="MTG.gpkg"
outlayer_h="Inundation_Points_High"
outlayer_l="Inundation_Points_Low"

# Reads in data files
inun_h52=pd.read_csv("../Inputs/inundation-depth-high-52-withoutplan.csv")
inun_h12=pd.read_csv("../Inputs/inundation-depth-high-12-withoutplan.csv")

inun_l52=pd.read_csv("../Inputs/inundation-depth-low-52-withoutplan.csv")
inun_l12=pd.read_csv("../Inputs/inundation-depth-low-12-withoutplan.csv")
points=gpd.read_file("land_points.gpkg")

# Sets projection
utm15n=26915

# Merges inundation sets
inun_high=inun_h52.merge(inun_h12, on="geography", how="outer",validate='1:1', suffixes=('_52', '_12'))
inun_low=inun_l52.merge(inun_l12, on="geography", how="outer",validate='1:1', suffixes=('_52', '_12'))
inun_merge=inun_high.merge(inun_low, on="geography", how="outer",validate='1:1', suffixes=('_high', '_low'))
inun_merge=inun_merge[["geography",'value_12_low','value_12_high','value_52_low','value_52_high']]

#%%
# Merges inundation levels onto extraction points
inun_merge=points.merge(inun_merge,left_on="qaqc_filet", right_on="geography", how="inner",validate='1:1',indicator=True)
print(inun_merge["_merge"].value_counts())
inun_merge=inun_merge[['geometry', 'geography', 'value_12_low', 'value_12_high',
                       'value_52_low', 'value_52_high']]

#%%
# Separates inundation geodataframe into high and low scenarios
inun_low=inun_merge[['geometry', 'geography', 'value_12_low','value_52_low']]
inun_high=inun_merge[['geometry', 'geography', 'value_12_high','value_52_high']]

#%%
# Reprojects dataframes
inun_high=inun_high.to_crs(epsg=utm15n)
inun_low=inun_low.to_crs(epsg=utm15n)

#%%
# Writes dataframes to geopackage layers
inun_high.to_file(outfile,layer=outlayer_h)
inun_low.to_file(outfile,layer=outlayer_l)