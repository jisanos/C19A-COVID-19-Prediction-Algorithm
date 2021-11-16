# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:46:15 2021

This will merge all the cleaned case, vax, and policies data into a single df

@author: jis
"""

import pandas as pd
import numpy as np
import data_imports

# %% Handing weather data first
weather_df = pd.read_csv('.\\weather.csv')


# %%
abbreviations_to_us_states = data_imports.abbreviations_to_us_states

    
# %% only select US weather data
weather_df = weather_df.dropna(subset=['date','location_key']) # Dropping key nans

weather_df = weather_df.reset_index(drop = True)

location_key_split = pd.DataFrame(list(weather_df.location_key.str.upper().str.split('_')))

weather_df['State'] = location_key_split[1]

weather_df = weather_df[(location_key_split[0] == 'US')]



del location_key_split #Free up memory

# %% Converting state abbreviations

def state_conv(x):
    
    if x != None:
        return abbreviations_to_us_states[x]
    
    else:
        return np.nan

weather_df['State'] = weather_df['State'].apply(state_conv)

# %% Rename and drop some columns

rename = {'State':'Province_State'}
drop = ['location_key']
weather_df = weather_df.rename(columns=rename)
weather_df = weather_df.drop(drop,axis="columns")
## Adding new Country_Region column for the merger later
weather_df['Country_Region'] = 'US'
weather_df = weather_df.reset_index(drop = True)

# %% Merging duplicates by mean

weather_df = weather_df.groupby(['date','Province_State','Country_Region']
                                ).mean().reset_index()

#%% Importing rest of data
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
# policies_df = policies_df[['date', 'State', 'policy', 'word_count']]

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

#%% Forward filling policies

merge_us['policy'] = merge_us.groupby(['Province_State','Country_Region'])['policy'].apply( lambda x: x.ffill())
# %% merging weather data


cols_to_merge_on = ['date','Province_State','Country_Region']
merge_us = merge_us.merge(weather_df, how='left', on = cols_to_merge_on)

# %% Interpolating any missing data

def fill_missing(x):
    cols_to_interpolate = ['average_temperature_celsius',
                           'minimum_temperature_celsius',
                           'maximum_temperature_celsius',
                           'rainfall_mm','snowfall_mm',
                           'dew_point','relative_humidity']
    
    x[cols_to_interpolate] = x[cols_to_interpolate].interpolate()
    
    return x

merge_us = merge_us.groupby(['Province_State','Country_Region'], dropna=False).apply(fill_missing)

# %% Exporting

merge_glob.to_csv('.\\merged_global.csv')
merge_us.to_csv('.\\merged_US.csv')