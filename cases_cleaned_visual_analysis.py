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
import calendar

#set the plot's theme to something more beautiful
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
file = ".\\cases_cleaned.csv"
cases_cleaned = pd.read_csv(file)
cases_cleaned = cases_cleaned.head(800000)
#%%
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
#cases_cleaned['date'] = cases_cleaned['date'].sort_values(ascending=True)
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%Y/%m/%d')

# using time series to filter data and sort it
#cases_cleaned['date']= pd.to_datetime(cases_cleaned['date'])
#cases_cleaned= cases_cleaned[cases_cleaned["date"] == cases_cleaned['date'].max()]
'''
cases_cleaned_Copy['date']= pd.to_datetime(cases_cleaned_Copy['date'])
cases_cleaned_Copy = cases_cleaned_Copy[cases_cleaned_Copy["date"] == cases_cleaned_Copy['date'].max()]
'''
# %%
cases_cleaned['Confirmed2.0'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].max()
# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
cases_cleaned_locations = cases_cleaned[["Confirmed2.0","date","Lat", "Long_"]]
# %%
#removing nan values and replacing them with 0 for the time being
cases_cleaned_locations_NA_removed = cases_cleaned_locations.fillna(8)
#%%
#cases_cleaned_locations_NA_removed['date']= pd.to_datetime(cases_cleaned_locations_NA_removed['date'])
print(cases_cleaned_locations_NA_removed.info())

# %%
heat_info = []

'''
for date in cases_cleaned_locations_NA_removed['date'].sort_values().unique():
    heat_info.append(cases_cleaned_locations_NA_removed.loc[cases_cleaned_locations_NA_removed['date'] == date, # for each hour append to list  
    ['Lat', 'Long_', 'Confirmed']]\
    .groupby(['Lat', 'Long_'])\
    .sum().reset_index().values.tolist()) #sum totals per station, reset index and create list
'''
     
for _, d in cases_cleaned_locations_NA_removed.groupby('date'):
   heat_info.append([[row['Lat'], row['Long_'], row['Confirmed2.0']] for _, row in d.iterrows()])




#for _, d in cases_cleaned_locations_NA_removed.groupby('Confirmed'):
 #  heat_info.append([[row['Lat'], row['Long_']] for _, row in d.iterrows()])
  
#%% Hector
# Ref https://stackoverflow.com/questions/64325958/heatmapwithtime-plugin-in-folium

from collections import defaultdict, OrderedDict

heat_data = defaultdict(list)

for _, d in cases_cleaned_locations_NA_removed.groupby('date'):
    
    for _, row in d.iterrows():
        
        heat_data[row['date']].append([row['Lat'], row['Long_'],row['Confirmed2.0']])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))


#%%
#heat_info = cases_cleaned_locations_NA_removed[['Lat','Long_','Confirmed']].values.tolist()
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

# %% Hector
covid_country_map = folium.Map(location=[cases_cleaned_locations_NA_removed["Lat"].mean(), 
                                        cases_cleaned_locations_NA_removed["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")

hm = plugins.HeatMapWithTime(data = list(heat_data.values()),index=list(heat_data.keys()), auto_play=True,max_opacity=0.8)
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


'''
# %%
cases_cleaned_Copy = pd.read_csv(file)
#cases_cleaned_Copy = cases_cleaned_Copy.head(100000)
# %%

# %%
group_CSSE = cases_cleaned_Copy[['Province_State','Deaths']].groupby('Province_State').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Deaths',color='red',title = 'States with more deaths',rot=0)
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more deaths')
plt.show()
print(cases_cleaned_Copy.head(5))
#print(group_CSSE.sort_values("Deaths",ascending=False))
# %%
group_CSSE = cases_cleaned_Copy[['Province_State','Confirmed']].groupby('Province_State').sum().reset_index().sort_values("Confirmed",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Confirmed',color='red',title = 'States with more confirmed',rot=0)
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()
print(cases_cleaned_Copy.head(5))

# %%
group_CSSE = cases_cleaned_Copy[['Province_State','Recovered']].groupby('Province_State').sum().reset_index().sort_values("Recovered",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Recovered',color='red',title = 'States with more Recovered',rot=0)
sns.barplot(x='Province_State', y='Recovered', data = group_CSSE.head(5)).set_title('States with more recovered')
plt.show()
print(cases_cleaned_Copy.head(5))

# %%
group_CSSE = cases_cleaned_Copy[['Country_Region','Deaths']].groupby('Country_Region').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Country_Region',y='Deaths',color='red',title = 'Regions with more deaths',rot=0)
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()
print(cases_cleaned_Copy.head(5))

# %%
print(cases_cleaned_Copy.info())
# %%
cases_cleaned_Copy['date'] = pd.to_datetime(cases_cleaned_Copy['date'], format='%Y/%m/%d')
cases_cleaned_Copy.sort_values(by='date', inplace=True)
group_CSSE = cases_cleaned_Copy[['date','Confirmed']].groupby(['date']).max().reset_index()

group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
group_CSSE = group_CSSE[['month','Confirmed','year']].groupby(['month','year']).max().reset_index()

# %%
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='Confirmed')

#%%
sns.heatmap(group_CSSE,linewidths=.5)

# %%
sns.heatmap(group_CSSE, fmt="f", annot=True, cmap='YlGnBu',linewidths=.5)

'''
