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
import matplotlib.patches as mpatches


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
#plotting bubble plot based on data

#reason the y axis has exponential value on top is because the number is too big so 7 is actually 7M

#the function commented below is to modify it manually but most data gets cut-off if decreased 
sns.scatterplot(data=Last_day, x="Deaths", y="Confirmed", size=200, legend=False, sizes=(20, 2000))

#plt.ylim(0,7000000)


#%%

#Trying to plot using another bubble plot but that the bubbles displays the countries

#varaibles for plot


plt.scatter(x = Last_day['Deaths'],
            y = Last_day['Confirmed'],
            s = Last_day['Recovered']/1000,
            alpha = 0.5)

#Title and labels
plt.title('Country/Regions Bubble Chart')
plt.xlabel('Deaths')
plt.ylabel('Confirmed')

#Bubble labels

x,y= Last_day['Deaths'],Last_day['Confirmed']

for i, txt in enumerate(Last_day['Country_Region']):
    plt.annotate(txt,x[i],y[i])
    
#legend

Country_list = list(Last_day['Country_Region'])

legend =[]

for i in range(0,len(Last_day.index)):
    legend.append(mpatches.Patch(color = 255,
                                 alpha = 0.5,
                                 label = Country_list[i]))
plt.legend(handles=1, loc=(1.05,0))
    
