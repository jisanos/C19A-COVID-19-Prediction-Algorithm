# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 17:19:24 2021

This script will be used to do feature selection on the merged us data, as well
as checking best modeling/algorithm for the data.

@author: jis
"""

# %% Importing libraries

import pandas as pd
import numpy as np
import seaborn as sns

# %% Importing csv and separating between state only and country only

us_df = pd.read_csv('.\\merged_US.csv')

state_filter = us_df['Province_State'].notna()

us_state = us_df[state_filter].copy()

us_country = us_df[np.logical_not(state_filter)].copy()

# %% Selecting only All and nan vaxx types for the moment

vax_filter = ((us_state['Vaccine_Type'] == 'All') | us_state['Vaccine_Type'].isna())

us_state_all_vax = us_state[vax_filter].copy()

vax_filter = ((us_country['Vaccine_Type'] == 'All') | us_country['Vaccine_Type'].isna())

us_country_all_vax = us_country[vax_filter].copy()

# %%

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed')
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths')
# %% Plotting cumulative

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed')

#%%
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths')

# %%
sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed')
sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths')
# %% Plotting daily

sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed')
# %%
sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths')