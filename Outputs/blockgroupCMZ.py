# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 22:02:20 2025

@author: Camille
"""
import geopandas as gpd
import pandas as pd

outfile="MTG.gpkg"
outlayer="Block Groups-Coastal Zone"

# Sets projection EPSG
utm15n=26915

# Reads in block group shapefile and state coastal zone shapefile
bg=gpd.read_file("MTG.gpkg",layer="Block_Group")
cmz=gpd.read_file("../Inputs/Louisiana Coastal Zone Shapefile.zip")

# Reprojects block groups and coastal management zone, corrects any validity issues
# for the coastal management zone polygon
bg=bg.to_crs(epsg=utm15n)
cmz["geometry"]=cmz["geometry"].make_valid()
cmz=bg.to_crs(epsg=utm15n)

# Clips the block groups with the CMZ
bg=bg.set_index("GEOID")
clip=bg.clip(cmz,keep_geom_type=True)

#%%
# Block groups and CMZ do not align perfectly, so there are some block groups
# with only a small portion in the CMZ. Calculates what percent
# of each block group is located within the CMZ, and creates a list with any
# block groups over 25%
areas=pd.DataFrame()
areas["bg"]=bg.area
areas["clip"]=clip.area
areas["pct"]=100*areas["clip"]/areas["bg"]

#%%
# Trims down the block groups to only those with at least 25% of the area in the 
# CMZ
keep=areas.query("pct>=25").index.to_list()
bg=bg.reset_index()
trim_bg=bg[bg["GEOID"].isin(keep)]

# Writes the trimmed block groups to the project geopackage
trim_bg.to_file(outfile,layer=outlayer)
