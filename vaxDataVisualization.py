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
vax_cleaned_categorizable = pd.read_csv(".\\vax_cleaned_categorizable.csv")
vax_cleaned_normal = pd.read_csv(".\\vax_cleaned_normal.csv")
vax_cleaned_categorizable_Without_Date_Filter = pd.read_csv(".\\vax_cleaned_categorizable.csv")
#%%
#using the latest data instead of all the data
vax_cleaned_categorizable['Date']= pd.to_datetime(vax_cleaned_categorizable['Date'])
vax_cleaned_categorizable= vax_cleaned_categorizable[vax_cleaned_categorizable["Date"] == vax_cleaned_categorizable['Date'].max()]

# %%
'''
#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = vax_cleaned_categorizable[vax_cleaned_categorizable['Country_Region'].notna() & 
              vax_cleaned_categorizable['Province_State'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']
'''
# %%
#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = vax_cleaned_categorizable[vax_cleaned_categorizable['Country_Region'].notna() & 
              vax_cleaned_categorizable['Province_State'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)

#a bar plot to show the top 5 second dosis of countries
sns.set(rc = {'figure.figsize':(9,9)})
sns.barplot(x='Country_Region', y='Stage_One_Doses', data = group_CSSE.head(5)).set_title('Top 5 country regions with where people have taken the first dosis the most')
plt.show()
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

#a bar plot to show the top 5 second dosis of countries
sns.set(rc = {'figure.figsize':(9,9)})
sns.barplot(x='Country_Region', y='Stage_Two_Doses', data = group_CSSE.head(5)).set_title('Top 5 country regions with where people have taken the second dosis the most')
plt.show()

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Stage_One_Doses', figsize=(10, 10),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
plt.title('Top 10 country regions with where people have taken the first dosis the most', bbox={'facecolor':'0.8', 'pad':5})
plt.show()

# %%
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Stage_Two_Doses', figsize=(10, 10),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
plt.title('Top 10 country regions with where people have taken the second dosis the most', bbox={'facecolor':'0.8', 'pad':5})
plt.show()

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Doses_admin']].sort_values("Doses_admin",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Doses_admin', figsize=(10, 10),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
plt.title("Top 10 doses of admin by country region", bbox={'facecolor':'0.8', 'pad':5})
plt.show()

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Doses_admin']].sort_values('Doses_admin',ascending=False)

#a bar plot to show the top 5 second dosis of countries
sns.set(rc = {'figure.figsize':(9,9)})
sns.barplot(x='Country_Region', y='Doses_admin', data = group_CSSE.head(5)).set_title("Top 5 doses of admin by country region")
plt.show()

# %%
'''
#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly_without_date_filter = vax_cleaned_categorizable_Without_Date_Filter[
    vax_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() & 
              vax_cleaned_categorizable_Without_Date_Filter['Province_State'].isna()]
'''
# %%
#filtering out the unknown values
vax_cleaned_categorizable_Without_Date_Filter = vax_cleaned_categorizable_Without_Date_Filter[
    vax_cleaned_categorizable_Without_Date_Filter['Country_Region'] != 'Unknown']

vax_cleaned_categorizable_Without_Date_Filter = vax_cleaned_categorizable_Without_Date_Filter[
    vax_cleaned_categorizable_Without_Date_Filter['Province_State'] != 'Unknown']
# %%
#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
vax_cleaned_categorizable_Without_Date_Filter['Date'] = pd.to_datetime(
    vax_cleaned_categorizable_Without_Date_Filter['Date'], format='%Y/%m/%d')
vax_cleaned_categorizable_Without_Date_Filter.sort_values(by='Date', inplace=True)
group_CSSE = vax_cleaned_categorizable_Without_Date_Filter

# %%
print(group_CSSE.info())
# %%
# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['Date'].dt.month
group_CSSE['year'] = group_CSSE['Date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
group_CSSE['month/year'] = group_CSSE['month'] + '/' + group_CSSE['year'].astype(str) 
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month/year','Vaccine_Type','New_Doses_alloc']].groupby(['month/year','Vaccine_Type']).sum().reset_index()
# %%
#put the months in the correct order
monthsOrdered = ['Dec/2020', 'Jan/2021','Feb/2021', 'Mar/2021', 'Apr/2021', 'May/2021', 'Jun/2021', 'Jul/2021', 'Aug/2021', 'Sep/2021']
group_CSSE['month/year'] = pd.CategoricalIndex(group_CSSE['month/year'], categories=monthsOrdered, ordered=True)
group_CSSE.sort_values(by='month/year', inplace=True)
# %%
ax = sns.barplot(y='month/year', x='New_Doses_alloc', hue="Vaccine_Type", data=group_CSSE)

# %%

#turning the data to datatime and then sorting it by date and groupby with date and 
#confirm to find the max value of each date
vax_cleaned_categorizable_Without_Date_Filter['Date'] = pd.to_datetime(
    vax_cleaned_categorizable_Without_Date_Filter['Date'], format='%Y/%m/%d')
vax_cleaned_categorizable_Without_Date_Filter.sort_values(by='Date', inplace=True)
group_CSSE = vax_cleaned_categorizable_Without_Date_Filter

# %%
# creating columns of but with month,year seperately 
group_CSSE['month'] = group_CSSE['Date'].dt.month
group_CSSE['year'] = group_CSSE['Date'].dt.year
#change the number of months to name of months
group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# %%
# needed to groupby again to date since i need to group by month and year 
group_CSSE = group_CSSE[['month','New_Doses_admin','year']].groupby(['month','year']).sum().reset_index()

# %%
#finally change the dataframe structure
group_CSSE = group_CSSE.pivot(index='month', columns='year', values='New_Doses_admin')

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

# %%

# %%
#Filtering cases cleaned categorizable for only province state uses
ProvinceUsesOnly = vax_cleaned_categorizable[vax_cleaned_categorizable['Country_Region'].notna() & 
              vax_cleaned_categorizable['Province_State'].notna()
              ]

#taking out the unknown
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Province_State'] != 'Unknown']
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] != 'Unknown']

# %%
#Filtering cases cleaned categorizable for only province state uses but for US states
ProvinceUsesOnlyForUs = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] == 'US']

# %%
#US states most deaths only
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Stage_One_Doses', data = group_CSSE.head(5)).set_title('Top 5 US province state with where people have taken the first dosis the most')
plt.show()
# %%
# group by country region
group_CSSE =  ProvinceUsesOnlyForUs[['Province_State','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Stage_One_Doses', figsize=(13, 13),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
plt.title('Top 10 US province state with where people have taken the first dosis the most', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
#US states most deaths only
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Stage_Two_Doses', data = group_CSSE.head(5)).set_title('Top 5 US province state with where people have taken the second dosis the most')
plt.show()

# %%
# group by country region
group_CSSE =  ProvinceUsesOnlyForUs[['Province_State','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Stage_Two_Doses', figsize=(13, 13),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
plt.title('Top 10 US province state with where people have taken the second dosis the most', bbox={'facecolor':'0.8', 'pad':5})
plt.show()