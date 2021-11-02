# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:14:49 2021

Script will work as a more thorough analysis of the vaccination data

@author: jis
"""
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%

# Contains time series of vaccinations
time_series_covid19_vaccine_global = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\"\
        "time_series_covid19_vaccine_global.csv")


# This contains vaccine type per state
vaccine_data_us_timeline = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\"\
        "vaccine_data_us_timeline.csv")



# Analyzing and cleaning US dataset only
# Dropping combined key column as it is unnecesary

vaccine_data_us_timeline.drop('Combined_Key',axis=1,inplace=True)

# %Dropping full nan rows

vaccine_data_us_timeline.dropna(how='all', inplace=True)

time_series_covid19_vaccine_global.dropna(how='all', inplace=True)


vaccine_data_us_timeline.reset_index(inplace=True, drop = True)
time_series_covid19_vaccine_global.reset_index(inplace=True, drop = True)
# %%
# Assigning data types
vaccine_data_us_timeline['Date'] = vaccine_data_us_timeline[
    'Date'].astype('datetime64[ns]')

# vaccine_data_us_timeline = vaccine_data_us_timeline.convert_dtypes()

time_series_covid19_vaccine_global['Date'] = time_series_covid19_vaccine_global['Date'].astype('datetime64[ns]')

# time_series_covid19_vaccine_global = time_series_covid19_vaccine_global.convert_dtypes()


# %%

#Checking unique values of states in US dataset

#unique_us_states = set(vaccine_data_us_timeline['Province_State'])

# There are some values in the state column which arent actual US states
# or are just departments related to the US states.

# %%

# Creating a list of "states" in the vaccine_data_us_timeline which are departments
# from the US dataframe:
not_really_states = ["Long Term Care (LTC) Program",
                      "Veterans Health Administration",
                      "Bureau of Prisons", "Department of Defense",
                      "Federal Bureau of Prisons", "Indian Health Services"]
# # Dropping them
# for element in not_really_states:
#     vaccine_data_us_timeline = vaccine_data_us_timeline[~(
#         vaccine_data_us_timeline['Province_State'] == element)]


# %%

# Checking unique value of country regions from US dataset

#unique_us_regions = set(vaccine_data_us_timeline['Country_Region'])

# We can see that US is the only value here

# %%

# Checking for unique values of Vaccine_Type from US dataset

#unique_vax_us = set(vaccine_data_us_timeline['Vaccine_Type'])

# We can see that there are Unnassigned and Unknown values as well as Pfizer,
# Moderna and Jannsen. Theres also an All which i assume contains a sum of them.

# I believe Unknown and Unassigned can be merged as one

# %%

# Merging all rows that are unnassigned and unknown to a single one

# unknown_and_unnassigned = vaccine_data_us_timeline[
#     (vaccine_data_us_timeline["Vaccine_Type"] == 'Unassigned') | 
#     (vaccine_data_us_timeline["Vaccine_Type"] == 'Unknown')]

# # Dropping the unknown and unnassigned from the main dataframe
# vaccine_data_us_timeline.drop(index = unknown_and_unnassigned.index, inplace = True)

# Doing a common sum of values of Unknown and unnassigned on equal 
# country, state, and date

# unknown_and_unnassigned.groupby(['Province_State','Date',
#                                  'Country_Region','FIPS','Lat','Long_',
#                                  ])

#Filtering in all with Unnasigned value
filter_in = (vaccine_data_us_timeline["Vaccine_Type"].str.lower().str.contains('unassigned'))

# Reassigning the filtered ones to Unknown
vaccine_data_us_timeline.loc[filter_in, 'Vaccine_Type'] = 'Unknown'
# This will possibly create duplicate entries that we can handle by merging them
# with a sum

dups = vaccine_data_us_timeline[vaccine_data_us_timeline.duplicated(['Date','Province_State','Country_Region','Vaccine_Type'])]

# There dont seem to be any duplicates after the renaming.

# %%

# Creating a dataframe of only

# %%

# time_series_covid19_vaccine_global[time_series_covid19_vaccine_global['Province_State'] == "NewYork"].plot('Date','People_partially_vaccinated')
# plt.show()

# %%
unique_global_regions = set(time_series_covid19_vaccine_global["Country_Region"])
# print(set(time_series_covid19_vaccine_global[time_series_covid19_vaccine_global['Country_Region'] == "US"]["Province_State"]))
# print(set(time_series_covid19_vaccine_global[time_series_covid19_vaccine_global['Country_Region'] == "US (Aggregate)"]["Province_State"]))
# print(set(time_series_covid19_vaccine_global[time_series_covid19_vaccine_global['Country_Region'] == "World"]["Province_State"]))
unique_global_states = set(time_series_covid19_vaccine_global['Province_State'])

unique_global_regions_with_nan_states = set(
    time_series_covid19_vaccine_global[time_series_covid19_vaccine_global['Province_State'].isna()]['Country_Region'])

# %%

#print(ts_vaccine_doses_admin_df[ts_vaccine_doses_admin_df['Country_Region'] == "US"])

# For some reason the global data does not have the US states separately.
# This means i gotta import and merge the us data with the global data


# %%
# Dropping all of the US values from the global dataframe
# as well as World values
to_remove = ["US", "US (Aggregate)", "World"]

for element in to_remove:
    
    filter_out = np.logical_not(time_series_covid19_vaccine_global["Country_Region"] == element)
    
    time_series_covid19_vaccine_global = time_series_covid19_vaccine_global[filter_out]


# %%



# %%
# Creating a list of "states" in the vaccine_data_us_timeline which arent really states
# from the US dataframe:
# not_really_states = ["Long Term Care (LTC) Program",
#                      "Veterans Health Administration",
#                      "Bureau of Prisons", "Department of Defense",
#                      "Federal Bureau of Prisons", "Indian Health Services"]

# # Dropping them
# for element in not_really_states:
#     vaccine_data_us_timeline = vaccine_data_us_timeline[~(
#         vaccine_data_us_timeline['Province_State'] == element)]


# %%
# Checking if states in us dataset are in global dataset

unique_us_states = set(vaccine_data_us_timeline['Province_State'])
unique_global_states = set(time_series_covid19_vaccine_global['Province_State'])

in_both = unique_us_states.intersection(unique_global_states)

# According to this, they both have unique values of state by this point
# This means the global dataset only contains US values on a country level
# %%
# Adding Vaccine_Type column equaling to all for the global dataset for the merging
time_series_covid19_vaccine_global["Vaccine_Type"] = "All"

# %%
# The column "People_partially_vaccinated" from the global dataset is the most
# similar to "Stage_One_Doses" from the US dataset
# This goes the same for the People_fully_vaccinated and Stage_two_doses
# so these will be renamed for the merger

time_series_covid19_vaccine_global.rename(columns={"People_partially_vaccinated": "Stage_One_Doses",
                              "People_fully_vaccinated": "Stage_Two_Doses"}, inplace=True)

# These columns seem to contain lots of nans at times so it might not be as
# important as Doses_admin

# %%
# Merging global dataframe with us dataframe
vax_df = pd.merge(vaccine_data_us_timeline, time_series_covid19_vaccine_global, how='outer',
                    on=['Country_Region', 'Province_State', 'Vaccine_Type', 'Doses_admin',
                        'Stage_One_Doses', 'Stage_Two_Doses', 'Date'])

# %% Dropping some unnecesary columns

drop = ['Lat', 'Long_','Report_Date_String']

vax_df = vax_df.drop(drop, axis=1)

# %% Resetting index

vax_df.reset_index(inplace=True, drop = True)
#%% Assigning propper datatypes

# vax_df = vax_df.convert_dtypes()
# %%some dtypes are not being assigned propperly.
# Assigning float instead of int for interpolation to work

dtypes = {'Doses_admin': "float64",
          'Stage_One_Doses': "float64",
          'Stage_Two_Doses': "float64",
          'Doses_alloc':'float64',
          'Doses_shipped':'float64'}

vax_df = vax_df.astype(dtypes)

# %% Make sure all numbers are positive
abs_cols = ['Doses_alloc', 'Doses_shipped', 'Doses_admin', 'Stage_One_Doses',
            'Stage_Two_Doses']

for col in abs_cols:
    vax_df[col] = vax_df[col].abs()

# %%
# Stripping string columns

str_cols = ['Province_State', 'Vaccine_Type', 'Country_Region']

for col in str_cols:
    vax_df[col] = vax_df[col].str.strip()

# %%Rename some countries

merge_countries = [('Bahamas, The', 'Bahamas'),
                   ('Czech Republic', 'Czechia'),
                   ('Gambia, The', 'Gambia'),
                   ('Hong Kong SAR','Hong Kong'),
                   ('Iran (Islamic Republic of)', 'Iran'),
                   ('Macao SAR', 'Macau'),
                   ('Russian Federation', 'Russia'),
                   ('Korea, South','South Korea'),
                   ('Republic of Korea','South Korea'),
                   ('Taipei and environs','Taiwan'), # WHO name Taiwan Taipei and environs
                   ('Taiwan*','Taiwan'),
                   ('Mainland China', 'China'),  # Maybe?
                   ('United Kingdom','UK')]

for old,new in merge_countries:
    vax_df.loc[vax_df['Country_Region'] == old,'Country_Region'] = new


# %%

#Df with only "All" vaccine types


# total_global_vax = vax_df[["Province_State", "Vaccine_Type", "Country_Region",
#                              "Doses_admin", "Stage_One_Doses",
#                              "Stage_Two_Doses"
#                              ]].groupby(["Province_State","Country_Region","Vaccine_Type"]).sum().reset_index()

#%%

# vax_df.sort_values([''])

vax_df.sort_values('Date').reset_index(inplace = True, drop = True)


# %% Filling nan values, by interpolation

def filler(x):
    
    
    # Assumes data is already sorted by date
    
    # Simple forward filling
    # x.Doses_alloc = x.Doses_alloc.ffill().bfill()
    # x.Doses_shipped = x.Doses_shipped.ffill().bfill()
    # x.Doses_admin = x.Doses_admin.ffill().bfill()
    # x.Stage_One_Doses = x.Stage_One_Doses.ffill().bfill()
    # x.Stage_Two_Doses = x.Stage_Two_Doses.ffill().bfill()
    
    #Setting first values to 0 for interpolation to work best
    
    first_index = x.head(1).index
    
    x.loc[first_index,'Doses_alloc'] = 0
    x.loc[first_index,'Doses_shipped'] = 0
    x.loc[first_index,'Doses_admin'] = 0
    x.loc[first_index,'Stage_One_Doses'] = 0
    x.loc[first_index,'Stage_Two_Doses'] = 0
    
    # Interpolation filling. Making sure they are all round numbers
    x['Doses_alloc'] = x['Doses_alloc'].interpolate().round()
    x['Doses_shipped'] = x['Doses_shipped'].interpolate().round()
    x['Doses_admin'] = x['Doses_admin'].interpolate().round()
    x['Stage_One_Doses'] = x['Stage_One_Doses'].interpolate().round()
    x['Stage_Two_Doses'] = x['Stage_Two_Doses'].interpolate().round()
    
    
    return x

vax_df = vax_df.groupby(['Province_State','Country_Region','Vaccine_Type'],dropna=False).apply(filler)

# %% Creating column with new vaccines only, instead of cummulative

def date_cases(x):
        
    
    x['New_Doses_admin'] = x.Doses_admin.sub(x.Doses_admin.shift().fillna(0)).abs()
    
    x['Doses_admin'] = x['New_Doses_admin'].cumsum()
    
    x['New_Stage_One_Doses'] = x.Stage_One_Doses.sub(x.Stage_One_Doses.shift().fillna(0)).abs()
    
    x['Stage_One_Doses'] = x['New_Stage_One_Doses'].cumsum()
    
    x['New_Stage_Two_Doses'] = x.Stage_Two_Doses.sub(x.Stage_Two_Doses.shift().fillna(0)).abs()
    
    x['Stage_Two_Doses'] = x['New_Stage_Two_Doses'].cumsum()
    
    return x
    

vax_df = vax_df.groupby(['Province_State','Country_Region','Vaccine_Type'],dropna=False).apply(date_cases)


# %%

vax_df.to_csv('.\\vax_cleaned.csv')