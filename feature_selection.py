# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 17:19:24 2021

This script will be used to do feature selection on the merged us data, as well
as checking best modeling/algorithm for the data.

@author: jis
"""

# %% Importing libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# %% Importing csv and separating between state only and country only

us_df = pd.read_csv('.\\merged_US.csv', index_col=0)

us_df['date']= us_df['date'].astype('datetime64[ns]')

state_filter = us_df['Province_State'].notna()

us_state = us_df[state_filter].copy()

us_country = us_df[np.logical_not(state_filter)].copy()

# %% Selecting only All and nan vaxx types for the moment

vax_filter = ((us_state['Vaccine_Type'] == 'All') | us_state['Vaccine_Type'].isna())

us_state_all_vax = us_state[vax_filter].copy()

vax_filter = ((us_country['Vaccine_Type'] == 'All') | us_country['Vaccine_Type'].isna())

us_country_all_vax = us_country[vax_filter].copy()

# %% Setting year format

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y-%m')
# %% cumulative Cases and Death unscaled
sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed')
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths')
plt.xticks(rotation = 45)
plt.show()
# %% cumulative Cases and Death scaled
fig, ax1 = plt.subplots(figsize=(8,5))

ax1.set_ylabel('Cumulative Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed',color='blue')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Deaths',color='red')
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths',color='red')



plt.xticks(rotation = 45)
plt.show()

# # %% Plotting cumulative
# # fig, axes = plt.subplots(figsize=(8,5))
# sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed')
# # axes.xaxis.set_major_locator(months)
# # axes.xaxis.set_major_formatter(years_fmt)
# # axes.xaxis.set_minor_locator(years)
# plt.xticks(rotation = 45)
# plt.show()
# #%%
# sns.lineplot(data = us_country_all_vax,x='date',y='Deaths')
# plt.xticks(rotation = 45)
# plt.show()

# %% daily cases and death unscaled
sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')
sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths',color='red')
plt.xticks(rotation = 45)
plt.show()

# %% daily cases and death scaled

fig, ax1 = plt.subplots(figsize=(8,5))

ax1.set_ylabel('Daily Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')

ax2 = ax1.twinx()

ax2.set_ylabel('Daily Deaths',color='red')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths',color='red')
plt.xticks(rotation = 45)
plt.show()

# # %% Plotting daily

# sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed')
# plt.xticks(rotation = 45)
# plt.show()
# # %%
# sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths')
# plt.xticks(rotation = 45)
# plt.show()
# %%cumulative cases and vaccines

fig, ax1 = plt.subplots(figsize=(8,5))

ax1.set_ylabel('Cumulative Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed',color='blue')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Doses',color='purple')
sns.lineplot(data = us_country_all_vax,x='date',y='Doses_admin',color='purple')



plt.xticks(rotation = 45)
plt.show()

# %%cumulative deaths and vaccines

fig, ax1 = plt.subplots(figsize=(8,5))

ax1.set_ylabel('Cumulative Deaths',color='red')

sns.lineplot(data = us_country_all_vax,x='date',y='Deaths',color='red')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Doses',color='purple')
sns.lineplot(data = us_country_all_vax,x='date',y='Doses_admin',color='purple')



plt.xticks(rotation = 45)
plt.show()

# %%
sns.lineplot(data = us_country, x = 'date', y = 'New_Doses_admin',hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()

# %% daily cases and vaccines
fig, ax1 = plt.subplots(figsize=(8,5))

ax1.set_ylabel('Daily Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')

ax2 = ax1.twinx()

ax2.set_ylabel('Daily Vaccines',color='purple')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Doses_admin',color='purple')
plt.xticks(rotation = 45)
plt.show()


# %%
sns.lineplot(data = us_country, x = 'date', y = 'Doses_admin',hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()
# %%
sns.lineplot(data = us_country, x = 'date', y = 'Stage_One_Doses',hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()
# %%
sns.lineplot(data = us_country, x = 'date', y = 'Stage_Two_Doses',hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()

# %%

sns.lmplot(x='Doses_admin',y='New_Confirmed',data = us_country_all_vax)

# %%
sns.lmplot(x='Doses_admin',y='New_Deaths',data = us_country_all_vax)

# %%
sns.lmplot(x='New_Confirmed',y='New_Deaths',data = us_country_all_vax)
# %%

keys = us_state_all_vax.columns[27:]

# %%
for key in keys:
    sns.lmplot(x=key,y = 'New_Confirmed',data = us_state_all_vax[us_state_all_vax[key] > 0])

# %%

sns.lmplot(x='mask',y = 'New_Confirmed',data = us_state_all_vax[us_state_all_vax['mask'] > 0])
# %%
sns.lineplot(data= us_state_all_vax, x='date',y='covid')