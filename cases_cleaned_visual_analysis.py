# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:22:11 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import matplotlib.pyplot as plt
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
# opening up the file that isn't 
cases_cleaned_categorizable = pd.read_csv(".\\cases_cleaned_normal.csv")

# %%
print(cases_cleaned_categorizable.info())
# %%
group_CSSE = cases_cleaned_categorizable[['Confirmed','Deaths','Province_State']].groupby('Province_State').max().reset_index().sort_values("Deaths",ascending=False)

# %%
filtering = cases_cleaned_categorizable[cases_cleaned_categorizable['Province_State'].isin(['Sao Paulo','Maharashtra','England','Lima'])]
# %%
sns.violinplot(x='Province_State', y='Deaths', data = filtering)
#%%

# %%
group_CSSE = cases_cleaned_categorizable[['Confirmed','Deaths','Province_State']].groupby('Province_State').max().reset_index().sort_values("Deaths",ascending=False)
# %%
sns.jointplot(data=group_CSSE, x="Confirmed", y="Deaths", kind="reg")
# %%

# %%
group_CSSE = cases_cleaned_categorizable[['Province_State','Deaths']].groupby('Province_State').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Deaths',color='red',title = 'States with more deaths',rot=0)
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more deaths')
plt.show()
print(cases_cleaned_categorizable.head(5))
#print(group_CSSE.sort_values("Deaths",ascending=False))
# %%
group_CSSE = cases_cleaned_categorizable[['Province_State','Confirmed']].groupby('Province_State').sum().reset_index().sort_values("Confirmed",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Confirmed',color='red',title = 'States with more confirmed',rot=0)
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()
print(cases_cleaned_categorizable.head(5))

# %%
group_CSSE = cases_cleaned_categorizable[['Province_State','Recovered']].groupby('Province_State').sum().reset_index().sort_values("Recovered",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Recovered',color='red',title = 'States with more Recovered',rot=0)
sns.barplot(x='Province_State', y='Recovered', data = group_CSSE.head(5)).set_title('States with more recovered')
plt.show()
print(cases_cleaned_categorizable.head(5))

# %%
group_CSSE = cases_cleaned_categorizable[['Country_Region','Deaths']].groupby('Country_Region').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Country_Region',y='Deaths',color='red',title = 'Regions with more deaths',rot=0)
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()
print(cases_cleaned_categorizable.head(5))
# %%
group_CSSE = cases_cleaned_categorizable[['Country_Region','Deaths']].groupby('Country_Region').sum().reset_index().sort_values("Deaths",ascending=False)
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(5).plot.pie(y='Deaths', figsize=(6, 10))
# %%
print(cases_cleaned_categorizable.info())
# %%

cases_cleaned_categorizable['date'] = pd.to_datetime(cases_cleaned_categorizable['date'], format='%Y/%m/%d')
cases_cleaned_categorizable.sort_values(by='date', inplace=True)
group_CSSE = cases_cleaned_categorizable[['date','Confirmed']].groupby(['date']).max().reset_index()

group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
group_CSSE = group_CSSE[['month','Confirmed','year']].groupby(['month','year']).max().reset_index()

# %%
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='Confirmed')

# %%
monthsOrdered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
group_CSSE.index = pd.CategoricalIndex(group_CSSE.index, categories=monthsOrdered, ordered=True)
group_CSSE = group_CSSE.sort_index()

#%%
group_CSSE = group_CSSE.fillna(8)
#%%
#group_CSSE['year'] = group_CSSE['year'].astype(int)
group_CSSE = group_CSSE.astype(int)
print(group_CSSE.info())
#%%
sns.heatmap(group_CSSE,linewidths=.5,fmt="d")

# %%
sns.heatmap(group_CSSE, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)


