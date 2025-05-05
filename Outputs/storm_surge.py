# -*- coding: utf-8 -*-
"""
Created on Sun May  4 10:09:30 2025

@author: Camille
"""

import pandas as pd

# Defines a function that reads csv files for different sea level rise and policy
# scenarios at year 12 (2035) and year 52 (2055), finds the change in median
# storm surge at the block group level between these years, and saves the dataframe
# to a pickle
def ss_change (slr,scen):
    twelve=pd.read_csv(f"../Inputs/median-ss-{slr}-12-{scen}plan.csv",dtype={"GEOID":str})
    twelve=twelve[["GEOID","median_12"]]
    fifty_two=pd.read_csv(f"../Inputs/median-ss-{slr}-52-{scen}plan.csv",dtype={"GEOID":str})
    fifty_two=fifty_two[["GEOID","median_52"]]
    merge=twelve.merge(fifty_two, on="GEOID", how="inner",validate="1:1",indicator=True)
    print(merge["_merge"].value_counts())
    merge=merge.drop(columns="_merge")
    cols=["median_12","median_52"]
    for col in cols:
        merge[col]=merge[col].where(merge[col]>=0,None)
        merge=merge.rename(columns={col:("ss_"+col)})
    merge["ss_change"]=merge["ss_median_52"]-merge["ss_median_12"]
    merge=merge.set_index("GEOID")
    pickle=merge.to_pickle(f"ss_change_{slr}_{scen}plan.pkl")
    return pickle

# Call the above function for four different scenarios of high and low sea level 
# rise, with and without the coastal management plan
ss_high_without=ss_change("high","without")
ss_high_with=ss_change("high","with")

ss_low_without=ss_change("low","without")
ss_low_with=ss_change("low","with")
