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
cases_cleaned['date']= pd.to_datetime(cases_cleaned['date'])
cases_cleaned = cases_cleaned[cases_cleaned["date"] == cases_cleaned['date'].max()]
#%%
#file = cases_cleaned['date'].max()

# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
cases_cleaned_locations = cases_cleaned[["Deaths","date","Lat", "Long_"]]
# %%
#removing nan values and replacing them with 0 for the time being
cases_cleaned_locations_NA_removed = cases_cleaned_locations.fillna(8)

# %%
 #Centering the map with the latitude and longitude mean values 
covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")

#heat_info = [[info["Lat"],info["Long_"],info["Deaths"]] for index, 
 #            info in cases_cleaned_locations_NA_removed.iterrows()]

heat_info = [[[info["Lat"],info["Long_"]] for index, 
             info in cases_cleaned_locations_NA_removed[cases_cleaned_locations_NA_removed['Deaths'] == i].iterrows()] 
             for i in range(0,100)]

hm = plugins.HeatMapWithTime(heat_info,auto_play=True, min_opacity=0.3, radius=29)

hm.add_to(covid_country_map)

covid_country_map.save("mymap.html") 

# %%
 #Centering the map with the latitude and longitude mean values 
covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")

heat_info = [[info["Lat"],info["Long_"],info["Deaths"]] for index, 
             info in cases_cleaned_locations_NA_removed.iterrows()]

hm = HeatMap(heat_info, min_opacity=0.3, 
             radius=29,blur=25,max_zoom=1)

hm.add_to(covid_country_map)

covid_country_map.save("mymap.html") 
# %%
#lat_long_list = []
#for i in cases_cleaned_locations_NA_removed['date'].unique():
 #   temp=[]
 #   for index, instance in cases_cleaned_locations_NA_removed[cases_cleaned_locations_NA_removed['date'] == i].iterrows():
 #       temp.append([instance['Lat'],instance['Long_'],instance['Deaths']])
 #   lat_long_list.append(temp)

# %%
#converting it to datetime format
#cases_cleaned_locations_NA_removed['date']= pd.to_datetime(cases_cleaned_locations_NA_removed['date'])#creating a time index
#time_index = []
#for i in cases_cleaned_locations_NA_removed['date'].unique():
 #   time_index.append(i)#formatting the index
#date_strings = [d.strftime('%d/%m/%Y, %H:%M:%S') for d in time_index]

# %%
#Choosing the map type 
#m = folium.Map(location=[1.352083,103.819839],zoom_start = 11, 
 #              tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
  #             attr="Stadia.AlidadeSmoothDark")#Plot it on the map
#m = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
#                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
 #                                      zoom_start=4, control_scale=True)

#plugins.HeatMapWithTime(lat_long_list,radius=5,auto_play=True,position='bottomright',name="cluster",index=time_index,max_opacity=0.7).add_to(m)
# %% 
#m.save("mymap.html")   