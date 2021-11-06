# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 19:25:37 2021

Script will serve to test and model various algos.

@author: jis
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt

# %% Importing csv and separating between state only and country only

us_df = pd.read_csv('.\\merged_US.csv', index_col=0)

us_df['date']= us_df['date'].astype('datetime64[ns]')

state_filter = us_df['Province_State'].notna()

us_state = us_df[state_filter].copy()

us_country = us_df[np.logical_not(state_filter)].copy()

# %% Selecting only All and nan vaxx types for the moment

vax_filter = ((us_state['Vaccine_Type'] == 'All') | us_state['Vaccine_Type'].isna())

us_state_all_vax = us_state[vax_filter].copy()

vax_filter = ((us_country['Vaccine_Type'] == 'All') | us_country['Vaccine_Type'].isna())

us_country_all_vax = us_country[vax_filter].copy()

# %% Functions for plotting train predictions and test predictions
def train_plotter(name, prediction, x_train, y_train):
    fig, ax = plt.subplots(figsize=(18,8))
    
    
    sns.lineplot(x = x_train.index, y = y_train.values, color = 'red', label='Real', ax=ax)
    sns.lineplot(x = x_train.index.values, y = prediction, color = 'blue', ax=ax, label = 'Fit')
        
    # elif(city == 'iq'):
    #     sns.lineplot(X_iq_train.index, y_iq_train.values[:,0], color = 'red', label='Real', ax=ax)
    #     sns.lineplot(X_iq_train.index.values, prediction, color = 'blue', ax=ax, label = 'Fit')

    plt.legend()
    plt.title(name)
    plt.show()                
    
def test_plotter(name, prediction, x_test, y_test):
    fig, ax = plt.subplots(figsize=(18,8))
    
    
    sns.lineplot(x=x_test.index, y_test.values, color = 'red', label='Real', ax=ax)
    sns.lineplot(x=x_test.index.values, prediction, color = 'blue', ax=ax, label = 'Fit')
    
    # elif(city=='iq'):
    #     fig, ax = plt.subplots(figsize=(18,8))
    #     sns.lineplot(X_iq_test.index, y_iq_test.values[:,0], color = 'red', label='Real', ax=ax)
    #     sns.lineplot(X_iq_test.index.values, prediction, color = 'blue', ax=ax, label = 'Fit')
        
    plt.legend()
    plt.title(name)
    plt.show()

# %%

train_df,test_df = train_test_split(us_state_all_vax[us_state_all_vax['Province_State'] =='New York'].fillna(0), test_size=0.3, train_size=0.7)

train_df = train_df.sort_values('date').set_index('date')
test_df = test_df.sort_values('date').set_index('date')

# %%
rfr = RandomForestRegressor(n_estimators = 1000)

train_cols = train_df.columns.values

cols_to_drop = ['Country_Region','Province_State','Lat','Long_','Confirmed','Deaths',
                'Recovered', 'Active','New_Confirmed','New_Deaths',
                'New_Recovered','Vaccine_Type','policy','word_count','date',
                'Case_Fatality_Ratio','Incident_Rate']

train_cols = np.setdiff1d(train_cols, cols_to_drop)

y_train = train_df['New_Confirmed'] #Target cols
X_train = train_df[train_cols] # Train

y_test = test_df['New_Confirmed']
X_test = test_df[train_cols]

rfr.fit(X_train, y_train)
# %%
train_plotter('Random Forest NY Train', rfr.predict(X_train),X_train,y_train)

test_plotter('Random Forest NY Test',rfr.predict(X_test),X_test, y_test )