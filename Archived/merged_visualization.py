# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:50:09 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
#set the plot's theme to something more beautiful
sns.set()

# %%
merged_US = pd.read_csv(".\\merged_US.csv")
merged_global = pd.read_csv(".\\merged_global.csv")
merged_US_Without_Date_Filter = pd.read_csv(".\\merged_US.csv")

#%%
'''
#using the latest data instead of all the data
merged_US['date']= pd.to_datetime(merged_US['date'])
merged_US= merged_US[merged_US["date"] == merged_US['date'].max()]
'''
# %%
# group by country region
# group_CSSE = merged_US[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

# #a bar plot to show the top 5 second dosis of countries
# sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(6)
#             ).set_title('Top 5 country regions with where people have taken the second dosis the most')
# plt.show()

# %%
'''
#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = merged_US[merged_US['Country_Region'].notna() & 
              merged_US['Province_State'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']

'''
# %%
'''
#Filtering cases cleaned categorizable for only province state uses
ProvinceUsesOnly = cases_cleaned_categorizable[cases_cleaned_categorizable['Country_Region'].notna() & 
              cases_cleaned_categorizable['Province_State'].notna() &
              cases_cleaned_categorizable['Admin2'].isna()]

#taking out the unknown
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Province_State'] != 'Unknown']
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] != 'Unknown']
'''
# %%
# group by country region
# group_CSSE = merged_US[['Province_State','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

# #a bar plot to show the top 5 second dosis of countries
# sns.set(rc = {'figure.figsize':(9,9)})
# sns.barplot(x='Province_State', y='Stage_Two_Doses', data = group_CSSE.head(5)).set_title('Top 5 country regions with where people have taken the second dosis the most')
# plt.show()
# %%
#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = merged_US_Without_Date_Filter[
    merged_US_Without_Date_Filter['Country_Region'].notna() & 
              merged_US_Without_Date_Filter['Province_State'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']
# %%
#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
CountryUsesOnly['date'] = pd.to_datetime(
    CountryUsesOnly['date'], format='%Y/%m/%d')
CountryUsesOnly.sort_values(by='date', inplace=True)

group_CSSE = CountryUsesOnly

# %%
# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['date'].dt.month
group_CSSE['year'] = group_CSSE['date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
group_CSSE['month/year'] = group_CSSE['month'] + '/' + group_CSSE['year'].astype(str) 
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month/year','Deaths','New_Doses_alloc']].groupby(['month/year']).sum()
# %%
#put the months in the correct order
monthsOrdered = ['Jan/2020','Feb/2020','Mar/2020','Apr/2020','May/2020','Jun/2020','Jul/2020','Aug/2020','Sep/2020','Oct/2020','Nov/2020','Dec/2020', 'Jan/2021','Feb/2021', 'Mar/2021', 'Apr/2021', 'May/2021', 'Jun/2021', 'Jul/2021', 'Aug/2021', 'Sep/2021']
group_CSSE.index = pd.CategoricalIndex(group_CSSE.index, categories=monthsOrdered, ordered=True)
#group_CSSE.sort_values(by=group_CSSE.index, inplace=True)
group_CSSE = group_CSSE.sort_index()
#group_CSSE['month/year'] = pd.CategoricalIndex(group_CSSE['month/year'], categories=monthsOrdered, ordered=True)
#group_CSSE.sort_values(by='month/year', inplace=True)

# %%
sns.heatmap(group_CSSE, annot=True)
# %%
ax = sns.lineplot(x='New_Doses_alloc', y='Deaths', data=group_CSSE)
#%%
