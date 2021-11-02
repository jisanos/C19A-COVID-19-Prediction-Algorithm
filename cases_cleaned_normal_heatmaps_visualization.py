# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 15:26:31 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import seaborn as sns
import folium
from folium import plugins
from folium.plugins import HeatMap
import calendar

#set the plot's theme to something more beautiful
sns.set()
# %%
## open cases_cleaned.csv and store it in an dataframe and then filter the date to the newest date
cases_cleaned = pd.read_csv(".\\cases_cleaned_normal.csv")
cases_cleaned = cases_cleaned.head(100000)
# %%
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
cases_cleaned['date'] = cases_cleaned['date'].dt.strftime('%Y/%m/%d')

# %%
cases_cleaned['Confirmed2.0'] = cases_cleaned['Confirmed'] / cases_cleaned['Confirmed'].max()
# %%
#Take away the unnessary columns and only use longitude, latitude and the countries for the map specifically
cases_cleaned_locations = cases_cleaned[["Confirmed2.0","date","Lat", "Long_"]]

#%%
#print to check info on this dataset
print(cases_cleaned_locations.info())
# %%
'''
#iteration where it iterates regarding the date in order in which lat, long and the weight of 
#confirmed gets used to determine the spread throughout 2020 to 2021
heat_info = []
     
for _, d in cases_cleaned_locations.groupby('date'):
   heat_info.append([[row['Lat'], row['Long_'], row['Confirmed2.0']] for _, row in d.iterrows()])
 ''' 
#%% Hector
# Ref https://stackoverflow.com/questions/64325958/heatmapwithtime-plugin-in-folium

from collections import defaultdict, OrderedDict

heat_data = defaultdict(list)

for _, d in cases_cleaned_locations.groupby('date'):
    
    for _, row in d.iterrows():
        
        heat_data[row['date']].append([row['Lat'], row['Long_'],row['Confirmed2.0']])

heat_data = OrderedDict(sorted(heat_data.items(),key=lambda t:t[0]))

# %%
'''
#Centering the map with the latitude and longitude mean values 
covid_country_map = folium.Map(location=[cases_cleaned_locations["Lat"].mean(), 
                                        cases_cleaned_locations["Long_"].mean()], 
                                      zoom_start=4, control_scale=True,attr="Stadia.AlidadeSmoothDark")



hm = plugins.HeatMapWithTime(heat_info, auto_play=True,max_opacity=0.8)
hm.add_to(covid_country_map)

covid_country_map.save("mymap.html")
'''
# %% Hector
covid_country_map = folium.Map(location=[cases_cleaned_locations["Lat"].mean(), 
                                        cases_cleaned_locations["Long_"].mean()], 
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

# this is for the total of the map (not the time series heatmap)  
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
# use dataset for the other heatmap
cases_cleaned = pd.read_csv(".\\cases_cleaned_normal.csv")
# %%

#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
group_CSSE = cases_cleaned[['date','Confirmed']].groupby(['date']).max().reset_index()

# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month','Confirmed','year']].groupby(['month','year']).max().reset_index()

# %%
#finally change the dataframe structure
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='Confirmed')

# %%
#put the months in the correct order
monthsOrdered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
group_CSSE.index = pd.CategoricalIndex(group_CSSE.index, categories=monthsOrdered, ordered=True)
group_CSSE = group_CSSE.sort_index()
#%%
#remove the dates that have no values since theyre future months of 2021
group_CSSE = group_CSSE.fillna(0)
#%%
#change the dataframe to an int type
group_CSSE = group_CSSE.astype(int)
print(group_CSSE.info())
#%%
#plot heatmap without showing numbers
sns.heatmap(group_CSSE,linewidths=.5,fmt="d")

# %%
#plot heatmap and show numbers
sns.heatmap(group_CSSE, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)

