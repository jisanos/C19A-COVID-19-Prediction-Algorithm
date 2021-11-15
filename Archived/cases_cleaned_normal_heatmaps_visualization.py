# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 15:26:31 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import seaborn as sns
import calendar
import matplotlib.pyplot as plt
#set the plot's theme to something more beautiful
sns.set()
# %%
# use dataset for the other heatmap
cases_cleaned = pd.read_csv(".\\cases_cleaned_categorizable.csv")

# %%
#Filtering cases cleaned categorizable for only country region uses
cases_cleaned = cases_cleaned[cases_cleaned['Country_Region'].notna() & 
              cases_cleaned['Province_State'].isna() &
              cases_cleaned['Admin2'].isna()]

#taking out the unknown
cases_cleaned = cases_cleaned[cases_cleaned['Province_State'] != 'Unknown']
cases_cleaned = cases_cleaned[cases_cleaned['Country_Region'] != 'Unknown']
# %%

#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
#group_CSSE = cases_cleaned[['date','New_Confirmed']].groupby(['date']).max().reset_index()
group_CSSE = cases_cleaned
# %%
# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month','New_Confirmed','year']].groupby(
    ['month','year']).sum().reset_index()

# %%
#finally change the dataframe structure
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='New_Confirmed')

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

# %%
#plot heatmap and show numbers
sns.heatmap(group_CSSE, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)
# adding a title to it
plt.title('Monthly Confirmed Cases (Globally)')
plt.show()
#%%
print(group_CSSE.info())
# %%
total = group_CSSE.loc[:,2020].sum() + group_CSSE.loc[:,2021].sum()
print(total)



# %%

#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
cases_cleaned['date'] = pd.to_datetime(cases_cleaned['date'], format='%Y/%m/%d')
cases_cleaned.sort_values(by='date', inplace=True)
#group_CSSE = cases_cleaned[['date','New_Confirmed']].groupby(['date']).max().reset_index()
group_CSSE = cases_cleaned
# %%
# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month','New_Deaths','year']].groupby(['month','year']).sum().reset_index()

# %%
#finally change the dataframe structure
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='New_Deaths')

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

# %%
#plot heatmap and show numbers
sns.heatmap(group_CSSE, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)
# adding a title to it
plt.title('Monthly Deaths (Globally)')
plt.show()