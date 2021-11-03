# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 20:29:42 2021

@author: jis
"""

import pandas as pd
import seaborn as sns
import folium
from folium import plugins
import webbrowser
from collections import defaultdict, OrderedDict
import sys
# import numpy as np
# from geopy.geocoders import Nominatim


# %%
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
file = ".\\cases_cleaned_normal.csv"
cases_cleaned = pd.read_csv(file,index_col=0)

# %%
# cases_cleaned = cases_cleaned[cases_cleaned['Country_Region'].notna() &
#                               cases_cleaned['Province_State'].notna() &
#                               cases_cleaned['Admin2'].isna()]

#%%
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
#cases_cleaned['date'] = cases_cleaned['date'].sort_values(ascending=True)


# %% Replacing 0 lat long with Nominatim search

# THis is now implemented in the preprocessing steps

# # should now include nans as well
# filter_zeros = (cases_cleaned['Lat'] == 0) & (cases_cleaned['Long_'] == 0)
# cases_zero = cases_cleaned[filter_zeros]

# locator = Nominatim(user_agent="http")

# def find_loc(x):
    
#     #Getting state and country values
#     state = list(set(x['Province_State']))[0]
#     country = list(set(x['Country_Region']))[0]
    
#     # Combining them to a single string
#     country_state = str(state) + ", " + str(country)
#     print(country_state)
#     # Getting their location
#     location = locator.geocode(country_state)
    
#     # Assigning their location
#     if location != None:
#         x['Lat'] = location.latitude
#         x['Long_'] = location.longitude
    
#     return x
    
# cases_zero = cases_zero.groupby(['Province_State','Country_Region'], dropna=False).apply(find_loc)
# # %% appending new values
# cases_cleaned = cases_cleaned[np.logical_not(filter_zeros)]#removing old entries

# cases_cleaned = cases_cleaned.append(cases_zero,ignore_index=True)

# %%
#removing nan or 0 lat long values
cases_cleaned = cases_cleaned[cases_cleaned['Lat'].notna() & cases_cleaned['Long_'].notna() & 
                              (cases_cleaned['Lat'] != 0) & (cases_cleaned['Long_'] != 0)]

# %% Interpolating missing dates data
# min_date = cases_cleaned.date.min()
# max_date = cases_cleaned.date.max()

def fill_missing_dates(x):
    
    
    # Setting date index
    x.set_index('date',inplace=True)
    
    #x = x.reindex(pd.date_range(start=min_date,end = max_date, freq='1D'))
    
    # Rexampling by date and interpolating values
    x = x.resample('D').interpolate()
    
    #x = x.interpolate(method='linear')
    
    # Returning the group with date as a column again
    return x.reset_index()

cases_cleaned = cases_cleaned.groupby(['Admin2', 'Province_State', 'Country_Region'],
                      dropna=False).apply(fill_missing_dates).reset_index(drop=True)


# reindexed_df = cases_cleaned.set_index('date')

# test = reindexed_df.resample('D').interpolate('cubic')


# %% Formatting the date column to work appropriately
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%Y/%m/%d')


# %%Getting only US data
filter_us = cases_cleaned['Country_Region'] == 'US'
cases_cleaned_us = cases_cleaned.loc[filter_us,:]

# %% Getting only PR data
filter_pr = cases_cleaned['Province_State'] == 'Puerto Rico'
cases_cleaned_pr = cases_cleaned.loc[filter_pr,:]
# %% creating weights
cases_cleaned['Weight'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].max()

cases_cleaned_us['Weight'] = cases_cleaned_us['Confirmed']/cases_cleaned_us['Confirmed'].max()

cases_cleaned_pr['Weight'] = cases_cleaned_pr['Confirmed']/cases_cleaned_pr['Confirmed'].max()

# %% Replacing zeros with the smallest possible number

filter_ = (cases_cleaned['Weight'] == 0)

cases_cleaned.loc[filter_ ,'Weight'] = sys.float_info.min

cases_cleaned_us.loc[(cases_cleaned_us['Weight']==0),'Weight'] = sys.float_info.min

cases_cleaned_pr.loc[(cases_cleaned_pr['Weight']==0),'Weight'] = sys.float_info.min

#%% global data for heatmap
# Ref https://stackoverflow.com/questions/64325958/heatmapwithtime-plugin-in-folium



heat_data = defaultdict(list)

for row in cases_cleaned.itertuples():
    heat_data[row.date].append([row.Lat,row.Long_,row.Weight])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# Export the heatmap
covid_country_map = folium.Map(zoom_start=3, control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()),
                             auto_play=True,max_speed=60,max_opacity=1)
hm.add_to(covid_country_map)

covid_country_map.save("global_spread.html")

webbrowser.open("global_spread.html")
# %%
heat_data = defaultdict(list)

for row in cases_cleaned_us.itertuples():
    heat_data[row.date].append([row.Lat,row.Long_,row.Weight])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# Export the heatmap
covid_country_map = folium.Map(location=[cases_cleaned_us["Lat"].mean(), 
                                        cases_cleaned_us["Long_"].mean()], 
                                      zoom_start=4,control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()),
                             auto_play=True,max_speed=60,max_opacity=1)
hm.add_to(covid_country_map)

covid_country_map.save("us_spread.html")

webbrowser.open("us_spread.html")
# %%
heat_data = defaultdict(list)

for row in cases_cleaned_pr.itertuples():
    heat_data[row.date].append([row.Lat,row.Long_,row.Weight])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# Export the heatmap
covid_country_map = folium.Map(location=[cases_cleaned_pr["Lat"].mean(), 
                                        cases_cleaned_pr["Long_"].mean()], 
                                      zoom_start=9, control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()),
                             auto_play=True,max_speed=60,max_opacity=1)
hm.add_to(covid_country_map)

covid_country_map.save("pr_spread.html")

webbrowser.open("pr_spread.html")

# # %%
# california = cases_cleaned[(cases_cleaned['Country_Region'] == 'US') &
#                            (cases_cleaned['Province_State'] == 'California') &
#                            (cases_cleaned['date'] == '2020/02/21')]

# # %% plotting unique points to identify outlier
# unique_lat_long = cases_cleaned.groupby(['Lat','Long_']).size().reset_index(name='Freq')




