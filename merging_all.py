# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:46:15 2021

This will merge all the cleaned case, vax, and policies data into a single df

@author: jis
"""

import pandas as pd
import numpy as np


#%%
vax_df = pd.read_csv('.\\vax_cleaned_categorizable.csv', index_col=0)

cases_df = pd.read_csv('.\\cases_cleaned_categorizable.csv', index_col=0)

policies_df = pd.read_csv('.\\policies_cleaned.csv', index_col=0)

# %% Removing county level data from cases (we only need state with country)

# Filtering in only where county is nan
filter_in_nan_counties = ( cases_df['Admin2'].isna() )


cases_df = cases_df.loc[filter_in_nan_counties,:]

# Dropping some columns
cols_to_drop = ['Admin2','FIPS']

cases_df.drop(cols_to_drop, inplace=True, axis=1)

# %% Selecting all vaccinations only

# filter_in_all_vaccines = (vax_df['Vaccine_Type'] == 'All')

# vax_df = vax_df.loc[filter_in_all_vaccines,:]

# %%Renaming vax columns accordingly

rename = {'Date':'date'}

vax_df = vax_df.rename(columns = rename)

# Dropping FIPS
cols_to_drop = ['FIPS','UID']

vax_df.drop(cols_to_drop,inplace=True,axis=1)

#%%
cols_to_merge_on = ['date','Province_State','Country_Region']
merge_glob = cases_df.merge(vax_df,how='outer',on = cols_to_merge_on)



# %% Only keeping important columns from policies
policies_df = policies_df[['date', 'State', 'policy', 'word_count']]

# %% renaming state column
rename = {'State':'Province_State'}

policies_df = policies_df.rename(columns=rename)

# %%Setting date to datetime on policies
#policies_df['date'] = policies_df['date'].astype('datetime64[ns]')

# %% Selecting only US data
merge_us = merge_glob.loc[merge_glob['Country_Region'] == 'US'].copy()

#%% Merging policies
cols_to_merge_on = ['date','Province_State']
merge_us = merge_us.merge(policies_df,how='outer',on=cols_to_merge_on)

# %% Forward filling policies


merge_us['policy'] = merge_us.groupby(['Province_State','Country_Region'])['policy'].apply( lambda x: x.ffill())

# %% Exporting

merge_glob.to_csv('.\\merged_global.csv')
merge_us.to_csv('.\\merged_US.csv')