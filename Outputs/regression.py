# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 22:45:55 2025

@author: Camille
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np

# Reads in data for high sea level rise scenario
vars=pd.read_pickle("regression_variables_high.pkl")

# Creates a dummy variable for at risk of inundation (everyday flooding)
thresh=0
vars["inun_risk"]=(vars["flood_pct_52"]>thresh).astype(int)

#Creates a dummy variable for at risk of storm surge
thresh=0
vars["ss_risk"]=(vars["ss_median_52"]>thresh).astype(int)

# Creates interaction of ss_risk and inun_risk dummy variables
vars["inun_risk_x_ss_risk"]=vars["inun_risk"]*vars["ss_risk"]

# Creates natural log of population variables
for pop in ['pop_12','pop_52']:
    vars[f'ln_{pop}'] = vars[pop].apply(np.log)

# Drops rows with missing values
vars=vars.dropna()
    
# Sets up dependent and independent variables
dep_var='ln_pop_52'
ind_vars=['inun_risk','ss_risk','inun_risk_x_ss_risk','flood_change','ss_change',
          'ln_pop_12','unemploy_rate', 'poverty_rate','fertility_rate','median_inc']
Y = vars[dep_var]
X = vars[ind_vars]
X = sm.add_constant(X)

# Runs regression and prints results
model = sm.OLS(Y,X)
results = model.fit()
print( results.summary() )
