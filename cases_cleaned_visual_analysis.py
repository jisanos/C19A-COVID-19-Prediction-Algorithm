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
from numpy import nan
from numpy import isnan
from pandas import read_csv
from sklearn.impute import SimpleImputer
import webbrwoser
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
cases_cleaned_locations = cases_cleaned[["Country_Region","Lat", "Long_"]]

# %%
#removing nan values and replacing them with 0 for the time being
cases_cleaned_locations_NA_removed = cases_cleaned_locations.fillna(8)
#print(cases_cleaned_locations.isnull().sum())
#cases_cleaned_locations_NA_removed = cases_cleaned_locations.dropna(inplace=True)
# mark zero values as missing or NaN
#cases_cleaned_locations_NA_removed[["Lat", "Long_"]] = dataset[[""]].replace(nan, 1.2)

# %%
# Centering the map with the latitude and longitude mean values
covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                         cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                        zoom_start=14, control_scale=True)

# %%
for index, info in cases_cleaned_locations_NA_removed.iterrows():
    folium.Marker([info["Lat"], info["Long_"]], 
                  popup=info["Country_Region"]).add_to(covid_country_map)
# %%    
covid_country_map.save("mymap.html")   

# %%
m = folium.Map(location=[45.5236, -122.6750])
m.save("mymap.html") 
# %%
display(m)