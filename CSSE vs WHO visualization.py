# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:10:58 2021

@author: LuisGa
"""
#%% Libraries

import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt



#%%
#Loading csv files and putting it into dataframe

path = "C:/Users/LuisGa/Documents/GitHub/C19A-COVID-19-Prediction-Algorithm-CAPSTONE/cases_cleaned"

df = pd.read_csv("cases_cleaned.csv")

df.head()
#%%
#filtering by most recent day recorded from dataframe
Last_day = df.loc[(df['date'] == '2021-09-21')]

print(Last_day)

#%%
#Top 10 results for death cases in countries

Top_10 = Last_day.nlargest(10,'Deaths')

print(Top_10)

#Other countries

Other_Countries = Last_day.nsmallest(3978,'Deaths')

Other_Countries.head()
#%% 
#plotting bubble plot based on data

#reason the y axis has exponential value on top is because the number is too big so 7 is actually 7M

sns.scatterplot(data=Top_10, x="Deaths", y="Confirmed", size=200, legend=False, sizes=(20, 2000))

x,y= Top_10['Deaths'],Top_10['Confirmed']

for i, txt in enumerate(Top_10.Country_Region):
    plt.annotate(txt,(Top_10.Deaths.iat[i],Top_10.Confirmed.iat[i]))

#Trying to add Other countries label as one
for i, txt in enumerate(Other_Countries.Country_Region):
    plt.annotate(txt,(Other_Countries.Deaths.iat[i],Other_Countries.Confirmed.iat[i]))
#%%


#varaibles for plot


plt.scatter(x = Top_10['Deaths'],
            y = Top_10['Confirmed'],
            s = Top_10['Recovered']/1000,
            alpha = 0.5)

#Trying to add Other regions to same bubble chart
plt.scatter(x = Other_Countries['Deaths'],
           y = Other_Countries['Confirmed'],
           s= Other_Countries['Recovered']/1000,
           alpha = 0.5)

#Title and labels
plt.title('Top 10 Country/Regions(Deaths) Bubble Chart')
plt.xlabel('Deaths')
plt.ylabel('Confirmed')


