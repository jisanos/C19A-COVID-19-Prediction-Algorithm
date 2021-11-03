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
import numpy as np
# %%
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
file = ".\\cases_cleaned_normal.csv"
cases_cleaned = pd.read_csv(file)

#%%
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
#cases_cleaned['date'] = cases_cleaned['date'].sort_values(ascending=True)
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%Y/%m/%d')

# %%
#removing nan or 0 lat long values
cases_cleaned = cases_cleaned[cases_cleaned['Lat'].notna() & cases_cleaned['Long_'].notna() & 
                              (cases_cleaned['Lat'] != 0) & (cases_cleaned['Long_'] != 0)]

# %% Selecting only US data to plot

filter_us = cases_cleaned['Country_Region'] == 'US'

cases_cleaned = cases_cleaned[filter_us]
# %%
cases_cleaned['Weight'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].max()

# %% Replacing zeros with the smallest possible number

filter_ = (cases_cleaned['Weight'] == 0)

cases_cleaned.loc[filter_ ,'Weight'] = sys.float_info.min

# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
#cases_cleaned_locations = cases_cleaned[["Weight","date","Lat", "Long_"]]


# %% Interpolating missing dates data

#%% data for heatmap
# Ref https://stackoverflow.com/questions/64325958/heatmapwithtime-plugin-in-folium



heat_data = defaultdict(list)

for row in cases_cleaned.itertuples():
    heat_data[row.date].append([row.Lat,row.Long_,row.Weight])


heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# %% export the heatmap
covid_country_map = folium.Map(location=[cases_cleaned["Lat"].mean(), 
                                        cases_cleaned["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()),
                             auto_play=True,max_speed=60)
hm.add_to(covid_country_map)

covid_country_map.save("mymap.html")

# %%
webbrowser.open("mymap.html")


# %%
california = cases_cleaned[(cases_cleaned['Country_Region'] == 'US') &
                           (cases_cleaned['Province_State'] == 'California') &
                           (cases_cleaned['date'] == '2020/02/21')]

# %% plotting unique points to identify outlier
unique_lat_long = cases_cleaned.groupby(['Lat','Long_']).size().reset_index(name='Freq')

# %%
# Getting states with lat or long as 0
# cases_zero = cases_cleaned[(cases_cleaned['Lat'] == 0) & (cases_cleaned['Long_'] == 0)]