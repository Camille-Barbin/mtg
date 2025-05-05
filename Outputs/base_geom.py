# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:09:26 2024

@author: Camille
"""

import geopandas as gpd

# Sets up outfile and projection
outfile="MTG.gpkg"
utm15n=26915

# Reads in Census and USACE shapefiles
bg=gpd.read_file("../Inputs/cb_2019_22_bg_500k.zip")
levee=gpd.read_file("../Inputs/levees-geojson.zip")
parish=gpd.read_file("../Inputs/cb_2023_us_county_500k.zip")

# Creates a layer for the levee, projected to UTM15N
levee=levee.to_crs(epsg=utm15n)
levee.to_file(outfile,layer="Levee")

# Creates a layer for Lafourche and Terrebonne parishes, the protection area of
# the levee, projected to UTM15N
protect=parish[(parish["GEOID"]=="22109")|(parish["GEOID"]=="22057")]
protect=protect.to_crs(epsg=utm15n)
protect.to_file(outfile, layer="Terrebonne+Lafourche")

# Creates a block group layer projected to UTM15N
bg=bg.to_crs(epsg=utm15n)
bg.to_file(outfile, layer="Block_Group")

# Creates a basic filled state outline layer projected to UTM15N
la=bg.dissolve()
la=la.to_crs(epsg=utm15n)
la.to_file(outfile,layer="State")






