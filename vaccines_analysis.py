# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:14:49 2021

@author: jis
"""
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%

# vaccine_df = pd.read_csv(
#     ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\vaccine_data_global.csv")

ts_vaccine_df = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\time_series_covid19_vaccine_global.csv")

# ts_vaccine_df is this one already melted with dates as a single
# column so this one is unnecesary
# ts_vaccine_doses_admin_df = pd.read_csv(
#       ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\time_series_covid19_vaccine_doses_admin_global.csv")


# Importing US data only


# This contains general vaccinations per state
# ts_people_vaccine_us_df = pd.read_csv(
#     ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\people_vaccinated_us_timeline.csv")

# This contains vaccine type per state
ts_vaccine_us_df = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\vaccine_data_us_timeline.csv")

# %%
# Data Dictionary of Global Data:
# Metric Name 	                Definition
# Country_Region 	            Country or region name
# Date 	                        Data collection date
# Doses_admin 	                Cumulative number of doses administered. When
#                               a vaccine requires multiple doses, each one
# is counted independently
# People_partially_vaccinated 	Cumulative number of people who received at
# least one vaccine dose. When the person
# receives a prescribed second dose, it is not
# counted twice
# People_fully_vaccinated 	    Cumulative number of people who received all
# prescribed doses necessary to be considered
# fully vaccinated
# Report_Date_String 	        Data reported date
# UID 	                        Country code: https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv


# Data Dictionary of US data:
# Column name,Definition
# FIPS,U.S. State identification code
# Province_State,Name of the State
# Country_Region,Code of the country
# Date,Data collection date
# Lat,Latitude
# Long_,Longitude
# Vaccine_Type,"Common name of the vaccine provider. Can be either a combination of all vaccine types labeled as 'All', or a specific provider like Moderna or Pfizer"
# Doses_alloc,Cumulative number of doses allocated
# Doses_shipped,Cumulative number of doses that have arrived to the vaccination sites.
# Doses_admin,Cumulative number of doses administered
# Stage_One_Doses,Cumulative number of first doses administered
# Stage_Two_Doses,Cumulative number of second doses administered
# Combined_Key,"Combination of Province_State, Country_Region"
# %%
# print(vaccine_df.columns)

# %%

# This only contains current global data, and is not useful to
# train our algorithm

# print(vaccine_df[vaccine_df.notna()])

# %%
# %%
# Analyzing and cleaning US dataset only
# Dropping combined key column as it is unnecesary

ts_vaccine_us_df.drop('Combined_Key',axis=1,inplace=True)

# %%
# Changing the date type to a datetime object
ts_vaccine_us_df['Date'] = ts_vaccine_us_df['Date'].astype('datetime64[ns]')

# %%

#Checking unique values of states in US dataset

unique_us_states = set(ts_vaccine_us_df['Province_State'])

# There are some values in the state column which arent actual US states
# or are just departments related to the US states.

# %%

# Creating a list of "states" in the ts_vaccine_us_df which are departments
from the US dataframe:
not_really_states = ["Long Term Care (LTC) Program",
                      "Veterans Health Administration",
                      "Bureau of Prisons", "Department of Defense",
                      "Federal Bureau of Prisons", "Indian Health Services"]
# # Dropping them
# for element in not_really_states:
#     ts_vaccine_us_df = ts_vaccine_us_df[~(
#         ts_vaccine_us_df['Province_State'] == element)]


# %%

# Checking unique value of country regions from US dataset

unique_us_regions = set(ts_vaccine_us_df['Country_Region'])

# We can see that US is the only value here

# %%

# Checking for unique values of Vaccine_Type from US dataset

unique_vax_us = set(ts_vaccine_us_df['Vaccine_Type'])

# We can see that there are Unnassigned and Unknown values as well as Pfizer,
# Moderna and Jannsen. Theres also an All which i assume contains a sum of them.

# I believe Unknown and Unassigned can be merged as one
# %%

print(ts_vaccine_us_df['Doses_admin'].max())
# %%

# Merging all rows that are unnassigned and unknown to a single one

unknown_and_unnassigned = ts_vaccine_us_df[
    (ts_vaccine_us_df["Vaccine_Type"] == 'Unassigned') | 
    (ts_vaccine_us_df["Vaccine_Type"] == 'Unknown')]

# Dropping the unknown and unnassigned from the main dataframe
ts_vaccine_us_df.drop(index = unknown_and_unnassigned.index, inplace = True)

# Doing a common sum of values of Unknown and unnassigned on equal 
# country, state, and date

# unknown_and_unnassigned.groupby(['Province_State','Date',
#                                  'Country_Region','FIPS','Lat','Long_',
#                                  ])



# del unknown_and_unnassigned # Deleting from memory


# %%
# Changing date column to a date variable

ts_vaccine_df['Date'] = ts_vaccine_df['Date'].astype('datetime64[ns]')


# %%

# Creating a dataframe of only

# %%

# ts_vaccine_df[ts_vaccine_df['Province_State'] == "NewYork"].plot('Date','People_partially_vaccinated')
# plt.show()

# %%
unique_global_regions = set(ts_vaccine_df["Country_Region"])
# print(set(ts_vaccine_df[ts_vaccine_df['Country_Region'] == "US"]["Province_State"]))
# print(set(ts_vaccine_df[ts_vaccine_df['Country_Region'] == "US (Aggregate)"]["Province_State"]))
# print(set(ts_vaccine_df[ts_vaccine_df['Country_Region'] == "World"]["Province_State"]))
unique_global_states = set(ts_vaccine_df['Province_State'])

unique_global_regions_with_nan_states = set(
    ts_vaccine_df[~ts_vaccine_df['Province_State'].notna()]['Country_Region'])

# %%

#print(ts_vaccine_doses_admin_df[ts_vaccine_doses_admin_df['Country_Region'] == "US"])

# For some reason the global data does not have the US states separately.
# This means i gotta import and merge the us data with the global data


# %%
# Dropping all of the US values from the global dataframe
# as well as World values
to_remove = ["US", "US (Aggregate)", "World"]

for element in to_remove:

    ts_vaccine_df = ts_vaccine_df[~(
        ts_vaccine_df["Country_Region"] == element)]


# %%



# %%
# Creating a list of "states" in the ts_vaccine_us_df which arent really states
# from the US dataframe:
# not_really_states = ["Long Term Care (LTC) Program",
#                      "Veterans Health Administration",
#                      "Bureau of Prisons", "Department of Defense",
#                      "Federal Bureau of Prisons", "Indian Health Services"]

# # Dropping them
# for element in not_really_states:
#     ts_vaccine_us_df = ts_vaccine_us_df[~(
#         ts_vaccine_us_df['Province_State'] == element)]


# %%
# Checking if states in us dataset are in global dataset

unique_us_states = set(ts_vaccine_us_df['Province_State'])
unique_global_states = set(ts_vaccine_df['Province_State'])

in_both = [
    element for element in unique_us_states if element in unique_global_states]

# According to this, they both have unique values of state by this point
# %%
# Adding Vaccine_Type column equaling to all for the global dataset for the merging
# ts_vaccine_df["Vaccine_Type"] = "All"

# %%
# The column "People_partially_vaccinated" from the global dataset is the most
# similar to "Stage_One_Doses" from the US dataset
# This goes the same for the People_fully_vaccinated and Stage_two_doses
# so these will be renamed for the merger

# ts_vaccine_df.rename(columns={"People_partially_vaccinated": "Stage_One_Doses",
#                               "People_fully_vaccinated": "Stage_Two_Doses"}, inplace=True)

# These columns seem to contain lots of nans at times so it might not be as
# important as Doses_admin

# %%
# Merging global dataframe with us dataframe
# merge_df = pd.merge(ts_vaccine_us_df, ts_vaccine_df, how='outer',
#                     on=['Country_Region', 'Province_State', 'Vaccine_Type', 'Doses_admin',
#                         'Stage_One_Doses', 'Stage_Two_Doses', 'Date'])

# %%

#Df with only "All" vaccine types


# total_global_vax = merge_df[["Province_State", "Vaccine_Type", "Country_Region",
#                              "Doses_admin", "Stage_One_Doses",
#                              "Stage_Two_Doses"
#                              ]].groupby(["Province_State","Country_Region","Vaccine_Type"]).sum().reset_index()




