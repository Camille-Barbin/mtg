# -*- coding: utf-8 -*-
"""
Created on Thu May  1 00:43:38 2025

@author: Camille
"""
import pandas as pd
import requests

outfile="census_regression_variables.pkl"

# Sets up a list of variables to pull from the ACS, and concatenates them into
# a string separated by commas

var_list=[
    'B19013_001E',  # Median household income
    'B23025_003E',  # Civilian labor force
    'B23025_005E',  # Unemployed
    'B13002_001E',  # Women 15 to 50
    'B13002_002E',  # Women who gave birth
    'B17010_001E',  # Families
    'B17010_002E'   # Families with income below poverty level
    ]
var_string=",".join(var_list)

#%%
# Defines a function that builds a Census API to pull variables at certain geographic
# levels for the entire state of Louisiana, calls the API, builds a dataframe
# from the responses, constructs a fips code for state+county+tract fips,
# changes missing value codes to None, and returns the dataframe
def call_api (var:str,for_clause:str):
    api='https://api.census.gov/data/2018/acs/acs5'
    in_clause="county:* state:22"
    key="b0f9294dec1d16302799e9a52bb135ff92442f06"
    payload={'get':var,'for':for_clause,'in':in_clause,'key':key}
    response=requests.get(api, payload)
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        assert False
    
    row_list=response.json()
    colnames=row_list[0]
    datarows=row_list[1:]
    geo=pd.DataFrame(columns=colnames,data=datarows)
    geo["tract_fp"]=geo["state"]+geo["county"]+geo["tract"]
    geo=geo.set_index("tract_fp")
    for col in var_list:
        geo[col]=geo[col].astype(float)
        geo[col]=geo[col].where(geo[col]>0,None)
    return geo

# Defines a function that calculates the unemployment rate, poverty rate, and 
# fertility rate out of the census values, and renames the median income column
def rate (geo):
    geo["unemploy_rate"]=geo["B23025_005E"]/geo["B23025_003E"]*100
    geo["poverty_rate"]=geo["B17010_002E"]/geo["B17010_001E"]*100
    geo["fertility_rate"]=geo["B13002_002E"]/geo["B13002_001E"]*100
    geo["median_inc"]=geo["B19013_001E"]
    return geo

# Calls the api function for tracts and block groups for the variables listed out
# at the beginning
tract = call_api(var_string,"tract:*")
bg = call_api(var_string,"block group:*")

# Calls the rate function for tracts and block groups, then drops the census
# variable columns for each dataframe
rate (tract)
rate (bg)

tract=tract.drop(columns=var_list)
bg=bg.drop(columns=var_list)

# Merges tract and block group dataframes 
census=bg.merge(tract, how="outer", on="tract_fp", validate="m:1", indicator=True, 
                suffixes=("_b","_t"))

# Fills missing block group values with tract values, drops tract variable columns, and 
# renames block group variable columns
cols=["unemploy_rate","poverty_rate","fertility_rate","median_inc"]
for col in cols:
    census[f"{col}_b"]=census[f"{col}_b"].fillna(census[f"{col}_t"])
    census=census.drop(columns=f"{col}_t")
    census=census.rename(columns={f"{col}_b":f"{col}"})

# Drops tract fips columns and renames block group fips columns
fips= ["state","county","tract"]
for col in fips:
    census=census.drop(columns=f"{col}_t")
    census=census.rename(columns={f"{col}_b":f"{col}"})

# Builds GEOIDs out of the fips codes and sets them as the GEOID then drops singular
# fips codes     
census["GEOID"]=census["state"]+census["county"]+census["tract"]+census["block group"]
census=census.set_index("GEOID")
census=census[["unemploy_rate","poverty_rate","fertility_rate","median_inc"]]

# Writes the dataframe to a pickle file
census.to_pickle(outfile)

