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

df = pd.read_csv("cases_cleaned_normal.csv")

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

Other_Countries['Other_Countries'] = Other_Countries['Deaths'].mean()

#Others['Country Region'] = 'Other Countries'
#%% 
#plotting bubble plot based on data

#reason the y axis has exponential value on top is because the number is too big so 7 is actually 7M

sns.scatterplot(data=Top_10, x="Deaths", y="Confirmed", size=200, legend=False, sizes=(20, 2000))

sns.scatterplot(data=Other_Countries, x="Other_Countries", y="Other_Countries", size=200, legend=False, sizes=(20, 2000))

x,y= Top_10['Deaths'],Top_10['Confirmed']

for i, txt in enumerate(Top_10.Country_Region):
    plt.annotate(txt,(Top_10.Deaths.iat[i],Top_10.Confirmed.iat[i]))

#Other Countries labels
for i, txt in enumerate(Other_Countries.Country_Region):
    plt.annotate('Other Countries',(Other_Countries.Other_Countries.iat[i],Other_Countries.Other_Countries.iat[i]))
#%%

#Title and labels
plt.title('Top 10 Country/Regions(Deaths) Bubble Chart')
plt.xlabel('Deaths')
plt.ylabel('Confirmed')


