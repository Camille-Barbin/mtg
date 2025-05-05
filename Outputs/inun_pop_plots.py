# -*- coding: utf-8 -*-
"""
Created on Sun May  4 18:37:26 2025

@author: Camille
"""
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns

# Reads in data
inun_pop_high=pd.read_pickle("Inundation_by_population_highSLR.pkl")
inun_pop_low=pd.read_pickle("Inundation_by_population_lowSLR.pkl")

# Bins changes in inundation
bins=[0,10,20,30,40,50,60,70,80,90,100]
labels=[10,20,30,40,50,60,70,80,90,100]
inun_pop_high["flood_bins"]=pd.cut(inun_pop_high['flood_change'], bins=bins,
                                   include_lowest=True, right=True, labels=labels)
inun_pop_low["flood_bins"]=pd.cut(inun_pop_low['flood_change'], bins=bins,
                                  include_lowest=True, right=True, labels=labels)
#%%
# Creates boxen plots showing the difference in population change for change in
# inundation
fig,ax1=plt.subplots()
sns.boxenplot(data=inun_pop_high,x="flood_bins",y="pop_change",ax=ax1)
fig.suptitle('Population Change by Inundation Change, High SLR, 2035-2055')
ax1.set_xlabel('Inundation Bins(%)')
ax1.set_ylabel('Population Change')
fig.tight_layout()
fig.savefig("../Figures/pop_by_inun_change_high_boxen.png")

fig,ax1=plt.subplots()
sns.boxenplot(data=inun_pop_low,x="flood_bins",y="pop_change",ax=ax1)
fig.suptitle('Population Change by Inundation Change, Low SLR, 2035-2055')
ax1.set_xlabel('Inundation Bins(%)')
ax1.set_ylabel('Population Change')
fig.tight_layout()
fig.savefig("../Figures/pop_by_inun_change_low_boxen.png")

fig,ax1=plt.subplots()
plt.scatter(inun_pop_high["flood_change"], inun_pop_high["pop_change"])
fig.suptitle('Population Change by Inundation Change, High SLR, 2035-2055')
ax1.set_xlabel('Change in Percent Flooded')
ax1.set_ylabel('Population Change')
fig.tight_layout()
fig.savefig("../Figures/pop_by_inun_change_high_scatter.png")

fig,ax1=plt.subplots()
plt.scatter(inun_pop_low["flood_change"], inun_pop_low["pop_change"])
fig.suptitle('Population Change by Inundation Change, Low SLR, 2035-2055')
ax1.set_xlabel('Change in Percent Flooded')
ax1.set_ylabel('Population Change')
fig.tight_layout()
fig.savefig("../Figures/pop_by_inun_change_low_scatter.png")




