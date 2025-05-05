# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 19:49:06 2025

@author: Camille
"""
import pandas as pd
import geopandas as gpd
import requests
import json

# Sets outfile
outfile="land_points.gpkg"

# Reads in parish file and points 
parish=gpd.read_file("../Inputs/model-geometries.gpkg",layer='parish')
points=gpd.read_file("../Inputs/model-geometries.gpkg",layer="extraction_point")

point_parish=parish.sjoin(points, how='inner', predicate="contains")
point_geoid_list=point_parish["GEOID"].unique().tolist()
point_name_list=point_parish["NAME"].unique().tolist()

print(point_name_list)

#%%
# Sets up area and linear water dataframes by looping through the hydrography
# file for each parish with extraction points and appending them to one another
a_water=gpd.GeoDataFrame()
l_water=gpd.GeoDataFrame()

for geo in point_geoid_list:
    a_file=gpd.read_file(f"../Inputs/Census_water/tl_2024_{geo}_areawater.zip")
    l_file=gpd.read_file(f"../Inputs/Census_water/tl_2024_{geo}_linearwater.zip")
    a_water=pd.concat([a_water,a_file])
    l_water=pd.concat([l_water,l_file])
 
#%%
# Sets projection and reprojects geodataframes
utm15n=26915

a_water=a_water.to_crs(epsg=utm15n)
l_water=l_water.to_crs(epsg=utm15n)
points=points.to_crs(epsg=utm15n)

#%%    
# Draws buffers around linear water
radius_m=50
buffer=l_water.buffer(radius_m)
buffer=buffer.to_frame()
buffer=buffer.rename(columns={'0':'geometry'})

#%%
# Finds points within area water or linear water
area_points=points.sjoin(a_water,how='inner',predicate='within')
linear_points=points.sjoin(buffer, how="inner", predicate='within')
bad_points=pd.concat([area_points,linear_points])

#%%
# Converts bad points to a list
bad_points=bad_points.set_index("qaqc_filet")
bad_points=bad_points.index.to_list()

#%%
# Drops any points in the bad points list and writes the remaining points to 
# a geopackage
keep_points=points[~points["qaqc_filet"].isin(bad_points)]
keep_points=keep_points.drop(columns=["site_no",'ecoregion'])
keep_points.to_file(outfile)


