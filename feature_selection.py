# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 17:19:24 2021

This script will be used to do feature selection on the merged us data, as well
as checking best modeling/algorithm for the data.

@author: jis
"""
#%% Global vars
dpi = 600
width = 8
height = 5

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
plt.figure(figsize=(8, 5), dpi = dpi) 
sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed')
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths', color='red')
# plt.xticks(rotation = 45)
plt.title('Cumulative Cases and Deaths not Properly Scaled (US)')
plt.ylabel("Cumulative Cases and Deaths")
plt.xlabel("Date (YYYY-MM)")
plt.show()
# %% cumulative Cases and Death scaled properly
fig, ax1 = plt.subplots(figsize=(8,5),dpi=dpi)

ax1.set_ylabel('Cumulative Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed',color='blue')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Deaths',color='red')
sns.lineplot(data = us_country_all_vax,x='date',y='Deaths',color='red')

plt.title('Cumulative Cases and Deaths Properly Scaled (US)')

ax1.set_xlabel("Date (YYYY-MM)")

# plt.xticks(rotation = 45)
plt.show()

# %% daily cases and death unscaled
sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')
sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths',color='red')
plt.xticks(rotation = 45)
plt.title('Daily Cases and Deaths Not Scaled (US)')
plt.xlabel("Date (YYYY-MM)")
plt.ylabel("Daily Cases and Deaths")
plt.show()

# %% daily cases and death scaled

fig, ax1 = plt.subplots(figsize=(8,5),dpi=dpi)

ax1.set_ylabel('Daily Cases',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')

ax2 = ax1.twinx()

ax2.set_ylabel('Daily Deaths',color='red')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Deaths',color='red')
plt.xticks(rotation = 45)
plt.title('Daily Cases and Deaths Properly Scaled (US)')
ax1.set_xlabel('Date (YYYY-MM)')
plt.show()


# %%cumulative cases and vaccines

fig, ax1 = plt.subplots(figsize=(8,5),dpi=dpi)

ax1.set_ylabel('Cumulative Cases',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed',color='blue')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Doses Administered',color='purple')
sns.lineplot(data = us_country_all_vax,x='date',y='Doses_admin',color='purple')

plt.title("Cumulative Cases and Administered Vaccines (US)")
ax1.set_xlabel('Date (YYYY-MM)')
plt.xticks(rotation = 45)
plt.show()

# %%
# sns.lineplot(data = us_country_all_vax,x='date',y='Confirmed',color='blue')
# sns.lineplot(data = us_country_all_vax,x='date',y='Doses_admin',color='purple')
# plt.show()
# %%cumulative deaths and vaccines

fig, ax1 = plt.subplots(figsize=(8,5),dpi=dpi)

ax1.set_ylabel('Cumulative Deaths',color='red')

sns.lineplot(data = us_country_all_vax,x='date',y='Deaths',color='red')

ax2 = ax1.twinx() #Instantiate second axe sharing the same x axis

ax2.set_ylabel('Cumulative Doses Administered',color='purple')
sns.lineplot(data = us_country_all_vax,x='date',y='Doses_admin',color='purple')


plt.title("Cumulative Deaths and Administered Vaccines (US)")
ax1.set_xlabel('Date (YYYY-MM)')
plt.xticks(rotation = 45)
plt.show()

# %%
plt.figure(figsize=(8, 5), dpi = dpi) 
sns.lineplot(data = us_country, x = 'date', y = 'New_Doses_admin',
             hue='Vaccine_Type')

plt.title("Daily Vaccines Administered per Type (US)")
plt.ylabel('Daily Vaccines Administered')
plt.xlabel('Date (YYYY-MM)')
plt.xticks(rotation = 45)
plt.show()

# %% daily cases and vaccines
fig, ax1 = plt.subplots(figsize=(8,5),dpi=dpi)

ax1.set_ylabel('Daily Confirmed',color='blue')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Confirmed',color='blue')

ax2 = ax1.twinx()

ax2.set_ylabel('Daily Vaccines',color='purple')

sns.lineplot(data = us_country_all_vax,x='date',y='New_Doses_admin',
             color='purple')

plt.title('Daily Cases and Vaccines (US)')
ax1.set_xlabel('Date (YYYY-MM)')
plt.xticks(rotation = 45)
plt.show()


# %%
plt.figure(figsize=(8, 5), dpi = dpi) 
sns.lineplot(data = us_country, x = 'date', y = 'Doses_admin',
             hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.title('Cumulative Vaccines per Type (US)')
plt.ylabel('Cumulative Vaccines Administered')
plt.xlabel('Date (YYYY-MM)')
plt.show()
# %%
plt.figure(figsize=(6, 6), dpi = dpi) 
sns.lineplot(data = us_country, x = 'date', y = 'Stage_One_Doses',
             hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()
# %%
plt.figure(figsize=(6, 6), dpi = dpi) 
sns.lineplot(data = us_country, x = 'date', y = 'Stage_Two_Doses',
             hue='Vaccine_Type')
plt.xticks(rotation = 45)
plt.show()

# %% lmplot function
def lmplot(x_col, y_col, data, title,x_label, y_label, width = width,
           height = height, dpi = dpi, show = True, hue = None, metric = True):
    
    
    if hue:
        g = sns.lmplot(x=x_col,y = y_col,data = data, hue = hue)
    else:
        g = sns.lmplot(x=x_col,y = y_col,data = data)

    g.fig.set_figwidth(width)
    g.fig.set_figheight(height)
    g.fig.set_dpi(dpi)

    if(metric):
        correlation = data[[x_col]].corrwith(data[y_col])
        correlation = round(correlation, 4)
        plt.legend(title='Correlation', loc='upper left',
                   labels=[str(correlation[0])])
    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if(show):
        plt.show()


# %% Cumulative Doses vs Daily Cases
lmplot(x_col='Doses_admin', y_col='New_Confirmed',
        data = us_country_all_vax, title = 'Cumulative Vaccines VS. Daily Cases (US)',
        x_label = 'Cumulative Vaccines Administered', y_label ='Daily Cases' )

# g = sns.lmplot(x='Doses_admin',y='New_Confirmed',data = us_country_all_vax)
# g.fig.set_figwidth(width)
# g.fig.set_figheight(height)
# g.fig.set_dpi(dpi)
# plt.title('Cumulative Vaccines VS. Daily Cases (US)')
# plt.xlabel("Cumulative Vaccines Administered")
# plt.ylabel("Daily Cases")
# plt.show()
# %% Cumulative Doses vs Daily Deaths

lmplot(x_col='Doses_admin', y_col='New_Deaths',
        data = us_country_all_vax, title = 'Cumulative Vaccines VS. Daily Deaths (US)',
        x_label = 'Cumulative Vaccines Administered', y_label ='Daily Deaths' )

# g = sns.lmplot(x='Doses_admin',y='New_Deaths',data = us_country_all_vax)
# g.fig.set_figwidth(width)
# g.fig.set_figheight(height)
# g.fig.set_dpi(dpi)
# plt.title('Cumulative Vaccines VS. Daily Deaths (US)')
# plt.xlabel("Cumulative Vaccines Administered")
# plt.ylabel("Daily Deaths")
# plt.show()
# %% Daily Confirmed vs Daily Deaths
lmplot(x_col='New_Confirmed', y_col='New_Deaths',
        data = us_country_all_vax, title = 'Daily Cases VS. Daily Deaths (US)',
        x_label = 'Daily Cases', y_label ='Daily Deaths' )

 
# g=sns.lmplot(x='New_Confirmed',y='New_Deaths',data = us_country_all_vax)
# g.fig.set_figwidth(width)
# g.fig.set_figheight(height)
# g.fig.set_dpi(dpi)
# plt.xlabel('Daily Cases')
# plt.ylabel('Daily Deaths')
# plt.title('Daily Cases VS. Daily Deaths (US)')
# plt.show()

# %% lm function with hue compatibility
def lmplot_hue(x_col, y_col, data, title,x_label, y_label, width = width,
           height = height, dpi = dpi, states = []):
    
    
    states_only_data = data[data['Province_State'].isin(states)]

    # lmplot(x_col=x_col, y_col=y_col,
    #        data = states_only_data,
    #        title = title,
    #        x_label = x_label, y_label =y_label, hue = 'Province_State',
    #        metric=False, show=False)


    correlations = [ ]
                                         
    # To keep same order as graph i must get the states from the dataframe itself          
    for state in states_only_data.Province_State.unique():
        data = states_only_data[states_only_data['Province_State'] == state]
        
        corr = data[[x_col]].corrwith(data[y_col])
        
        corr = round(corr,4)
        
        correlations.append(str(corr[0]))
                                                   
    # plt.legend(title='Correlation', loc='upper left',
    #            labels=correlations)

    
    # plt.show()
    
    n = round(len(states)/2)
    

    
    fig, axs = plt.subplots(ncols=n, nrows = n, figsize=(14,10),dpi=dpi)
    fig.suptitle(title, fontsize=20)
    count=0
    row=0
    col=0
    for state in states_only_data.Province_State.unique():
        data = states_only_data[states_only_data['Province_State'] == state]
        
        
        sns.regplot(x = x_col, y=y_col, data = data, ax = axs[row,col])
        
        axs[row, col].set_title(state)
        axs[row, col].set_xlabel(x_label)
        axs[row, col].set_ylabel(y_label)
        axs[row, col].legend(['Corr: ' + correlations[count]])
        
        count +=1
        row +=1
        if row == n:
            col += 1
            row = 0
    
    
    plt.show()

# %%
states = ['Puerto Rico', 'Florida','California', 'New York']
# %% Avg temp vs daily cases
lmplot_hue(x_col='average_temperature_celsius', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Average Temp. VS Daily Cases',
           x_label = 'Average Temp. C', y_label ='Daily Cases',
           states = states)



# %% Max Temp vs daily cases


lmplot_hue(x_col='maximum_temperature_celsius', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Maximum Temp. VS Daily Cases',
           x_label = 'Maximum Temp. C', y_label ='Daily Cases',
           states = states)

# %% Min temp vs daily cases


lmplot_hue(x_col='minimum_temperature_celsius', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Minimum Temp. VS Daily Cases',
           x_label = 'Minimum Temp. C', y_label ='Daily Cases',
           states = states)

# %% Precipitation vs daily cases

lmplot_hue(x_col='rainfall_mm', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Precipitation VS Daily Cases',
           x_label = 'Rainfall (mm)', y_label ='Daily Cases',
           states = states)

# %% Snowfall vs daily cases

lmplot_hue(x_col='snowfall_mm', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Snowfall VS Daily Cases',
           x_label = 'Snowfall (mm)', y_label ='Daily Cases',
           states = states)

# %% dew point vs daily cases

lmplot_hue(x_col='dew_point', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Dew Point VS Daily Cases',
           x_label = 'Dew Point', y_label ='Daily Cases',
           states = states)

# %% relative humidity vs daily cases

lmplot_hue(x_col='relative_humidity', y_col='New_Confirmed',
           data = us_state_all_vax, title = 'Relative Hymidity VS Daily Cases',
           x_label = 'Relative Humidity', y_label ='Daily Cases',
           states = states)

# %%
keys = us_state_all_vax.columns[27:]

# %%
# for key in keys[:40]:
#     sns.lmplot(x=key,y = 'New_Confirmed',data = us_state_all_vax[us_state_all_vax[key] > 0])
#     plt.plot()

# %%
corr = pd.DataFrame()
for key in keys:
    data = pd.DataFrame(us_state_all_vax[[key]].corrwith(
        us_state_all_vax['New_Confirmed'] / us_state_all_vax['New_Confirmed'].max()))
    corr = corr.append(data)

corr.sort_values(by=0, inplace=True,ascending=False)

# %% Barplot of corelations
# plt.figure(figsize=(14, 6), dpi = 800) 
# sns.barplot(y=corr[0], x=corr.index)
# plt.ylabel('Weight')
# plt.xlabel('Word')
# plt.xticks(rotation = 60)
# plt.show()

# %% Barplot of top corelations
top_corr = corr[(corr[0]> 0.35) | (corr[0] < -0.35)]
plt.figure(figsize=(14, 6), dpi = dpi) 
sns.barplot(y=top_corr[0], x=top_corr.index)
plt.title('Corelation Between Word and Daily Cases')
plt.ylabel('Weight')
plt.xlabel('Word')
plt.xticks(rotation = 60)
plt.show()

# %%

sns.lmplot(x='mask',y = 'New_Confirmed',data = us_state_all_vax[us_state_all_vax['mask'] > 0])
plt.show()
# %%
sns.lineplot(data= us_state_all_vax, x='date',y='covid')
plt.show()
# %%
sns.lineplot(data= us_state_all_vax, x='date',y='mask')
plt.show()