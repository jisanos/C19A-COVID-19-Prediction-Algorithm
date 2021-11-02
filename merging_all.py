# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:46:15 2021

This will merge all the cleaned case, vax, and policies data into a single df

@author: jis
"""

import pandas as pd
import numpy as np


#%%
vax_df = pd.read_csv('.\\vax_cleaned.csv')

cases_df = pd.read_csv('.\\cases_cleaned_categorizable.csv')

policies_df = pd.read_csv('.\\policies_cleaned.csv')

# %% Removing county level data from cases (we only need state with country)

# Filtering in only where county is nan
filter_in_nan_counties = ( cases_df['Admin2'].isna() )


cases_df = cases_df.loc[filter_in_nan_counties,:]

# Dropping the county column

cases_df.drop('Admin2', inplace=True, axis=1)

# %%

