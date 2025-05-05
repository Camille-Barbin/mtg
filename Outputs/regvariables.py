# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 18:39:16 2025

@author: Camille
"""
import requests
import pandas as pd
import geopandas as gpd

# Reads in inundation and population change dataframe for high SLR scenario and sets
# the index to GEOID
inun_pop_high=pd.read_csv("Inundation_by_population_highSLR.csv",dtype={"GEOID":str})
inun_pop_high=inun_pop_high.set_index("GEOID")

# Reads in census variables dataframe
census=pd.read_pickle("census_regression_variables.pkl")

# Reads in storm surge dataframe for high SLR scenario
storm_surge=pd.read_pickle("ss_change_high_withoutplan.pkl")

# Joins the three above dataframes on GEOIDs
reg_var=pd.concat([inun_pop_high,census,storm_surge], axis=1)

# Saves the dataframe for high SLR scenario regression to a pickle file
reg_var.to_pickle("regression_variables_high.pkl")



