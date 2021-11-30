# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 20:29:42 2021

@author: jis
"""

import pandas as pd
import folium
from folium import plugins
import webbrowser
from collections import defaultdict, OrderedDict
import sys
import numpy as np
# from geopy.geocoders import Nominatim


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


# %%
#removing nan or 0 lat long values
cases_cleaned = cases_cleaned[cases_cleaned['Lat'].notna() & cases_cleaned['Long_'].notna() & 
                              (cases_cleaned['Lat'] != 0) & (cases_cleaned['Long_'] != 0)]

# %% Interpolating missing dates data
# min_date = cases_cleaned.date.min()
# max_date = cases_cleaned.date.max()
# from https://stackoverflow.com/questions/30056399/interpolate-and-fill-pandas-dataframe-with-datetime-index

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





# %% Formatting the date column to work appropriately
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%Y/%m/%d')


# %%Getting only US data
filter_us = cases_cleaned['Country_Region'] == 'US'
cases_cleaned_us = cases_cleaned.loc[filter_us,:].copy()

# %% Getting only PR data
filter_pr = cases_cleaned['Province_State'] == 'Puerto Rico'
cases_cleaned_pr = cases_cleaned.loc[filter_pr,:].copy()



# %% creating weights
cases_cleaned['Weight'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].max()

cases_cleaned_us['Weight'] = cases_cleaned_us['Confirmed']/cases_cleaned_us['Confirmed'].max()

cases_cleaned_pr['Weight'] = cases_cleaned_pr['Confirmed']/cases_cleaned_pr['Confirmed'].max()

# %% Replacing zeros and nan weights with smalles number

cases_cleaned['Weight'] = cases_cleaned['Weight'].replace(0, sys.float_info.min)
cases_cleaned['Weight'] = cases_cleaned['Weight'].replace(np.nan, sys.float_info.min)

cases_cleaned_us['Weight'] = cases_cleaned_us['Weight'].replace(0, sys.float_info.min)
cases_cleaned_us['Weight'] = cases_cleaned_us['Weight'].replace(np.nan, sys.float_info.min)

cases_cleaned_pr['Weight'] = cases_cleaned_pr['Weight'].replace(0, sys.float_info.min)
cases_cleaned_pr['Weight'] = cases_cleaned_pr['Weight'].replace(np.nan, sys.float_info.min)
#%% global data for heatmap
# Ref https://stackoverflow.com/questions/64325958/heatmapwithtime-plugin-in-folium



heat_data = defaultdict(list)

for row in cases_cleaned.itertuples():
    heat_data[row.date].append([row.Lat,row.Long_,row.Weight])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# Export the heatmap
covid_country_map = folium.Map(location=[0,0],zoom_start=3, control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()),
                             auto_play=True,max_speed=60,max_opacity=1)
hm.add_to(covid_country_map)

covid_country_map.save("global_spread.html")

webbrowser.open("global_spread.html")
# %% US heatmap
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
# %% PR Heatmap
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




