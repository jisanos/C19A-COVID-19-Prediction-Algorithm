# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:22:11 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
from folium.plugins import HeatMap
from numpy import nan
from numpy import isnan
from pandas import read_csv
from sklearn.impute import SimpleImputer
import webbrowser
import random
import datetime
import time
from datetime import datetime

#set the plot's theme to something more beautiful
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
file = ".\\cases_cleaned.csv"
cases_cleaned = pd.read_csv(file)
cases_cleaned_Copy = pd.read_csv(file)

#%%
#cases_cleaned['date']= pd.to_datetime(cases_cleaned['date'])
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
#cases_cleaned['date'] = cases_cleaned['date'].sort_values(ascending=True)
cases_cleaned.sort_values(by='date', inplace=True)
#cases_cleaned['date'] = cases_cleaned['date'].sort_values(ascending=True)
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%d/%m/%Y')

# using time series to filter data and sort it
#cases_cleaned['date']= pd.to_datetime(cases_cleaned['date'])
#cases_cleaned= cases_cleaned[cases_cleaned["date"] == cases_cleaned['date'].max()]
'''
cases_cleaned_Copy['date']= pd.to_datetime(cases_cleaned_Copy['date'])
cases_cleaned_Copy = cases_cleaned_Copy[cases_cleaned_Copy["date"] == cases_cleaned_Copy['date'].max()]
'''
# %%
cases_cleaned['Confirmed'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].sum()
# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
cases_cleaned_locations = cases_cleaned[["Confirmed","date","Lat", "Long_"]]
# %%
#removing nan values and replacing them with 0 for the time being
cases_cleaned_locations_NA_removed = cases_cleaned_locations.fillna(8)
#%%
#cases_cleaned_locations_NA_removed['date']= pd.to_datetime(cases_cleaned_locations_NA_removed['date'])
print(cases_cleaned.info())

# %%

heat_info = []
for _, d in cases_cleaned_locations_NA_removed.groupby('date'):
   heat_info.append([[row['Lat'], row['Long_'], row['Confirmed']] for _, row in d.iterrows()])
   
#%%
print(heat_info)
# %%

 #Centering the map with the latitude and longitude mean values 
covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")

#heat_info = cases_cleaned_locations_NA_removed[['Lat','Long_','Confirmed']].values.tolist()
   
#heat_info = [[info["Lat"],info["Long_"],info["Confirmed"]] for index, 
     #       info in cases_cleaned_locations_NA_removed.iterrows()]

'''
heat_info = [[[info["Lat"],info["Long_"]] for index, 
             info in cases_cleaned_locations_NA_removed[cases_cleaned_locations_NA_removed['Deaths'] == i].iterrows()] 
             for i in range(0,100)]
'''
#hm = plugins.HeatMapWithTime(heat_info,auto_play=True, min_opacity=0.3, radius=29)
hm = plugins.HeatMapWithTime(heat_info, auto_play=True,max_opacity=0.8)
hm.add_to(covid_country_map)

covid_country_map.save("mymap.html") 


# %%
'''
 #Centering the map with the latitude and longitude mean values 
covid_country_map = folium.Map(attr="<a href=https://endless-sky.github.io/>Endless Sky</a>",location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                      zoom_start=4, control_scale=True)

heat_info = [[info["Lat"],info["Long_"],info["Deaths"]] for index, 
             info in cases_cleaned_locations_NA_removed.iterrows()]

hm = HeatMap(heat_info, min_opacity=0.3, 
             radius=29,blur=25,max_zoom=1)

hm.add_to(covid_country_map)
'''
# %%
#Adding different tiles
folium.TileLayer('openstreetmap').add_to(covid_country_map)
folium.TileLayer('stamenterrain').add_to(covid_country_map)
folium.TileLayer('stamentoner').add_to(covid_country_map)
folium.TileLayer('stamenwatercolor').add_to(covid_country_map)
folium.TileLayer('cartodbpositron').add_to(covid_country_map)
folium.TileLayer('cartodbdark_matter').add_to(covid_country_map)

# control for switching between layers
folium.LayerControl().add_to(covid_country_map) 


# %%
covid_country_map.save("mymap.html")   