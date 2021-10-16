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

#set the plot's theme to something more beautiful
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
file = ".\\cases_cleaned.csv"
cases_cleaned = pd.read_csv(file)
cases_cleaned = cases_cleaned[cases_cleaned["date"] == "2021-09-28"]
#%%
#file = cases_cleaned['date'].max()

# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
cases_cleaned_locations = cases_cleaned[["Deaths","Lat", "Long_"]]

# %%
#removing nan values and replacing them with 0 for the time being
cases_cleaned_locations_NA_removed = cases_cleaned_locations.fillna(8)

# %%
# Centering the map with the latitude and longitude mean values 

covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                       zoom_start=4, control_scale=True)

#heat_info = [[info["Lat"],info["Long_"],info["Deaths"]] for index, 
 #            info in cases_cleaned_locations_NA_removed.iterrows()]

heat_info = [[[info["Lat"],info["Long_"]] for index, 
             info in cases_cleaned_locations_NA_removed[cases_cleaned_locations_NA_removed['Deaths'] == i].iterrows()] for i in range(0,1000)]

hm = plugins.HeatMapWithTime(heat_info,auto_play=True, min_opacity=0.3, radius=29)

#hm = plugins.HeatMapWithTime(heat_info,auto_play=True, min_opacity=0.3, 
 #            radius=29,blur=25,max_zoom=1)

hm.add_to(covid_country_map)

#covid_country_map.add_child(hm)
# %%
#HeatMap(heat_data).add_to(map_hooray)  
covid_country_map.save("mymap.html")   