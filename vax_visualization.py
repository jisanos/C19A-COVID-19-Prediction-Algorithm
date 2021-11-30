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
import data_imports
#set the plot's theme to something more beautiful
sns.set()

# %%
vax_cleaned_cat = pd.read_csv(".\\vax_cleaned_categorizable.csv")
vax_cleaned_normal = pd.read_csv(".\\vax_cleaned_normal.csv")
world_pop = data_imports.world_pop_by_country()
# %% Renaming world population country column
world_pop = world_pop.rename(columns={'Country Name':'Country_Region',
                                      "2018":"Population"})
#%%
vax_cleaned_cat['Date']= pd.to_datetime(
    vax_cleaned_cat['Date'])
# %%
'''
#Filtering cases cleaned categorizable for only country region uses
country_vax_df = vax_cleaned_cat[vax_cleaned_cat['Country_Region'].notna() & 
              vax_cleaned_cat['Province_State'].isna()]
#taking out the unknown
country_vax_df = country_vax_df[country_vax_df['Province_State'] != 'Unknown']
country_vax_df = country_vax_df[country_vax_df['Country_Region'] != 'Unknown']
'''
# %%
# Getting country level data only
country_vax_df = vax_cleaned_cat[vax_cleaned_cat['Country_Region'].notna() & 
                                 vax_cleaned_cat['Province_State'].isna()]
#taking out the unknown
country_vax_df = country_vax_df[country_vax_df['Province_State'] != 'Unknown']
country_vax_df = country_vax_df[country_vax_df['Country_Region'] != 'Unknown']

# Adding country population
country_vax_df = country_vax_df.merge(world_pop, on='Country_Region')
# %% First dosage per country
agg_dic = {'Stage_One_Doses':'max'}

latest_values = country_vax_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Stage_One_Doses'], ascending=False)
          
          
plt.figure(figsize=(14, 6), dpi = 800) 
sns.barplot(x='Country_Region', y='Stage_One_Doses',data = latest_values.head(10)
            ).set_title('First Dosage Distribution per Country (Global)')
plt.xlabel('Country')
plt.ylabel('First Dosage')
plt.show()
# %% Second dosage per country
agg_dic = {'Stage_Two_Doses':'max'}

latest_values = country_vax_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Stage_Two_Doses'], ascending=False)


plt.figure(figsize=(14, 6), dpi = 800) 
sns.barplot(x='Country_Region', y='Stage_Two_Doses', data = latest_values.head(10)
            ).set_title('Second Dosage Distribution per Country (Global)')
plt.xlabel('Country')
plt.ylabel('Second Dosage')
plt.show()
# %% Total doses per country

agg_dic = {'Doses_admin':'max'}

latest_values = country_vax_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Doses_admin'], ascending=False)

plt.figure(figsize=(14, 6), dpi = 800)
sns.barplot(x='Country_Region',y='Doses_admin',data = latest_values.head(10))
plt.title('Doses Administered per Country (Global)')
plt.xlabel('Country')
plt.ylabel('Total Doses')
plt.show()

# %% Doses administered pie chart

# plt.figure(figsize=(6, 6), dpi = 800) 

# latest_values = latest_values.set_index('Country_Region')
# latest_values.head(10).plot.pie(y='Doses_admin', autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
# plt.title("Doses Administered per Country (Global)", bbox={'facecolor':'0.8', 'pad':5})
# plt.xlabel('')
# plt.ylabel('')
# plt.show()
# %%
# group by country region
# group_CSSE = country_vax_df[['Country_Region','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Country_Region')
# group_CSSE.head(10).plot.pie(y='Stage_One_Doses', figsize=(10, 10),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
# plt.title('Top 10 country with where people have taken the first dosis the most', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()

# %%
# %%
# group by country region
# group_CSSE = country_vax_df[['Country_Region','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Country_Region')
# group_CSSE.head(10).plot.pie(y='Stage_Two_Doses', figsize=(10, 10),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
# plt.title('Top 10 country with where people have taken the second dosis the most', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()



# %%
# group by country region
# group_CSSE = country_vax_df[['Country_Region','Doses_admin']].sort_values('Doses_admin',ascending=False)

# #a bar plot to show the top 5 second dosis of countries
# sns.set(rc = {'figure.figsize':(9,9)})
# sns.barplot(x='Country_Region', y='Doses_admin', data = group_CSSE.head(5)).set_title("Top 5 number of doses of admin per country")
# plt.show()

# %%
'''
#Filtering cases cleaned categorizable for only country region uses
country_vax_df_without_date_filter = vax_cleaned_cat_Without_Date_Filter[
    vax_cleaned_cat_Without_Date_Filter['Country_Region'].notna() & 
              vax_cleaned_cat_Without_Date_Filter['Province_State'].isna()]

#filtering out the unknown values
vax_cleaned_cat_Without_Date_Filter = country_vax_df_without_date_filter[
    country_vax_df_without_date_filter['Country_Region'] != 'Unknown']

vax_cleaned_cat_Without_Date_Filter = country_vax_df_without_date_filter[
    country_vax_df_without_date_filter['Province_State'] != 'Unknown']

vax_cleaned_cat_Without_Date_Filter = country_vax_df_without_date_filter[
    country_vax_df_without_date_filter['Vaccine_Type'] != 'Unknown']

vax_cleaned_cat_Without_Date_Filter = country_vax_df_without_date_filter[
    country_vax_df_without_date_filter['Vaccine_Type'] != 'All']

'''

# %% prepairing heatmap data

filter_out =    (country_vax_df['Country_Region'] != 'Unknown') & (
                country_vax_df['Province_State'] != 'Unknown') & (
                country_vax_df['Vaccine_Type'] != 'Unknown')   & (
                country_vax_df['Vaccine_Type'] != 'All')

hm_df = country_vax_df[filter_out]

hm_df['Date'] = pd.to_datetime(hm_df['Date'], format='%Y/%m/%d')
hm_df.sort_values(by='Date', inplace=True)


#%%
# # %%
# # creating columns of but with month,year seperately 
# group_CSSE['month'] = group_CSSE['Date'].dt.month
# group_CSSE['year'] = group_CSSE['Date'].dt.year
# #change the number of months to name of months
# group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# group_CSSE['month/year'] = group_CSSE['month'] + '/' + group_CSSE['year'].astype(str) 
# # %%
# # needed to groupby again to date since i need to group by month and year 
# group_CSSE = group_CSSE[['month/year','Vaccine_Type','New_Doses_alloc']].groupby(['month/year','Vaccine_Type']).sum().reset_index()
# # %%
# #put the months in the correct order
# monthsOrdered = ['Dec/2020', 'Jan/2021','Feb/2021', 'Mar/2021', 'Apr/2021', 'May/2021', 'Jun/2021', 'Jul/2021', 'Aug/2021', 'Sep/2021']
# group_CSSE['month/year'] = pd.CategoricalIndex(group_CSSE['month/year'], categories=monthsOrdered, ordered=True)
# group_CSSE.sort_values(by='month/year', inplace=True)
# # %%
# ax = sns.barplot(y='month/year', x='New_Doses_alloc', hue="Vaccine_Type", data=group_CSSE)
# plt.title('Yearly and monthly doses of allocation for each vaccine type')
# plt.show()
# # %%
# ax = sns.barplot(x='month/year', y='New_Doses_alloc', hue="Vaccine_Type", data=group_CSSE)
# plt.title('Yearly and monthly doses of allocation for each vaccine type')
# plt.xticks(rotation=90)
# plt.show()

# %% Plotting heatmap of total doses administerd
# creating columns of but with month,year seperately 

hm_doses_df = hm_df
hm_doses_df['month'] = hm_doses_df['Date'].dt.month
hm_doses_df['year'] = hm_doses_df['Date'].dt.year
#change the number of months to name of months
hm_doses_df['month'] = hm_doses_df['month'].apply(lambda x: calendar.month_abbr[x])

# needed to groupby again to date since i need to group by month and year 
hm_doses_df = hm_doses_df[['month','New_Doses_admin','year']].groupby(
    ['month','year']).sum().reset_index()


hm_doses_df = hm_doses_df.pivot(index='month', columns='year',
                                values='New_Doses_admin')


months_ordered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep',
                  'Oct', 'Nov', 'Dec']

hm_doses_df.index = pd.CategoricalIndex(hm_doses_df.index,
                                       categories=months_ordered, ordered=True)
hm_doses_df = hm_doses_df.sort_index()

hm_doses_df = hm_doses_df.fillna(0)

hm_doses_df = hm_doses_df.astype(int)

plt.figure(figsize=(6, 6), dpi = 600) 
sns.heatmap(hm_doses_df, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)
plt.title('Monthly Administered Doses (Globally)')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()
# %%

# %%
# creating columns of but with month,year seperately 
# group_CSSE['month'] = group_CSSE['Date'].dt.month
# group_CSSE['year'] = group_CSSE['Date'].dt.year
# #change the number of months to name of months
# group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# # %%
# # needed to groupby again to date since i need to group by month and year 
# group_CSSE = group_CSSE[['month','Stage_One_Doses','year']].groupby(['month','year']).sum().reset_index()

# # %%
# #finally change the dataframe structure
# group_CSSE = group_CSSE.pivot(index='month', columns='year', values='Stage_One_Doses')

# # %%
# #put the months in the correct order
# monthsOrdered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
# group_CSSE.index = pd.CategoricalIndex(group_CSSE.index, categories=monthsOrdered, ordered=True)
# group_CSSE = group_CSSE.sort_index()
# #%%
# #remove the dates that have no values since theyre future months of 2021
# group_CSSE = group_CSSE.fillna(0)
# #%%
# #change the dataframe to an int type
# #group_CSSE = group_CSSE.astype(int)
# #print(group_CSSE.info())

# # %%
# #plot heatmap and show numbers
# sns.heatmap(group_CSSE, fmt="f", annot=True, cmap='YlGnBu',linewidths=.5)
# plt.title('Yearly and monthly of the stage one dosis being used globally')
# plt.show()
# # %%

# #turning the data to datatime and then sorting it by date and groupby with date and 
# #confirm to find the max value of each date
# vax_cleaned_cat_Without_Date_Filter['Date'] = pd.to_datetime(
#     vax_cleaned_cat_Without_Date_Filter['Date'], format='%Y/%m/%d')
# vax_cleaned_cat_Without_Date_Filter.sort_values(by='Date', inplace=True)
# group_CSSE = vax_cleaned_cat_Without_Date_Filter

# # %%
# # creating columns of but with month,year seperately 
# group_CSSE['month'] = group_CSSE['Date'].dt.month
# group_CSSE['year'] = group_CSSE['Date'].dt.year
# #change the number of months to name of months
# group_CSSE['month'] = group_CSSE['month'].apply(lambda x: calendar.month_abbr[x])
# # %%
# # needed to groupby again to date since i need to group by month and year 
# group_CSSE = group_CSSE[['month','Stage_Two_Doses','year']].groupby(['month','year']).sum().reset_index()

# # %%
# #finally change the dataframe structure
# group_CSSE = group_CSSE.pivot(index='month', columns='year', values='Stage_Two_Doses')

# # %%
# #put the months in the correct order
# monthsOrdered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
# group_CSSE.index = pd.CategoricalIndex(group_CSSE.index, categories=monthsOrdered, ordered=True)
# group_CSSE = group_CSSE.sort_index()
# #%%
# #remove the dates that have no values since theyre future months of 2021
# group_CSSE = group_CSSE.fillna(0)
#%%
#change the dataframe to an int type
#group_CSSE = group_CSSE.astype(int)
#print(group_CSSE.info())

# %%
#plot heatmap and show numbers
# sns.heatmap(group_CSSE, fmt="f", annot=True, cmap='YlGnBu',linewidths=.5)
# plt.title('Yearly and monthly of the stage two dosis being used globally')
# plt.show()


# %%
#Filtering cases cleaned categorizable for only province state uses
state_vax_df = vax_cleaned_cat[vax_cleaned_cat['Country_Region'].notna() & 
              vax_cleaned_cat['Province_State'].notna()
              ]

#taking out the unknown
state_vax_df = state_vax_df[state_vax_df['Province_State'] != 'Unknown']
state_vax_df = state_vax_df[state_vax_df['Country_Region'] != 'Unknown']

# %%
#Filtering cases cleaned categorizable for only province state uses but for US states
us_state_vax_df = state_vax_df[state_vax_df['Country_Region'] == 'US']

# %% US stated stage 1 dosages
agg_dic = {'Stage_One_Doses':'max'}

to_plot = us_state_vax_df.groupby(
    'Province_State', as_index=False).agg(
        agg_dic).sort_values('Stage_One_Doses',ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Stage_One_Doses', data = to_plot.head(10)
            ).set_title('First Dosage Administered per State (US)')
plt.title('Stage One Dosage Distribution (US)')
plt.xlabel('State')
plt.ylabel('Stage One Doses')
plt.show()
# %%
# group by country region
# group_CSSE =  us_state_vax_df[['Province_State','Stage_One_Doses']].sort_values('Stage_One_Doses',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Province_State')
# group_CSSE.head(10).plot.pie(y='Stage_One_Doses', figsize=(13, 13),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
# plt.title('Top 10 US province state with where people have taken the first dosis the most', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %% US states dtage 2 dosages
agg_dic = {'Stage_Two_Doses':'max'}

to_plot = us_state_vax_df.groupby(
    'Province_State', as_index=False).agg(
        agg_dic).sort_values('Stage_Two_Doses',ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Stage_Two_Doses', data = to_plot.head(10)
            ).set_title('Second Dosage Administered per State (US)')
plt.title('Stage Two Dosage Distribution (US)')
plt.xlabel('State')
plt.ylabel('Stage Two Doses')
plt.show()

# # %%
# # group by country region
# group_CSSE =  us_state_vax_df[['Province_State','Stage_Two_Doses']].sort_values('Stage_Two_Doses',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Province_State')
# group_CSSE.head(10).plot.pie(y='Stage_Two_Doses', figsize=(13, 13),autopct='%1.1f%%',legend=None,shadow=True, startangle=140)
# plt.title('Top 10 US province state with where people have taken the second dosis the most', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %% Catplot of different vaccine types (US)

agg_dic = {'Doses_admin':'max'}

top_states = us_state_vax_df.groupby(
    ['Province_State'], as_index=False).agg(
        agg_dic).sort_values(['Doses_admin'],ascending=False)

top_states = top_states['Province_State'].unique()[:11] #Getting the first states

to_plot = us_state_vax_df[us_state_vax_df.Province_State.isin(top_states)]
        


g=sns.catplot(data=to_plot,kind='bar',x='Province_State',y='Doses_admin',
            hue='Vaccine_Type')

g.fig.set_figwidth(14)
g.fig.set_figheight(6)
g.fig.set_dpi(600)

plt.title('Vaccine Brand Distribution per State (US)')
plt.xlabel('State')
plt.ylabel('Doses Administered')

plt.show()

# %% Catplot of first and second stage doses

