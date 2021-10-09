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

# %%
# Changing the date type to a datetime object
vaccine_data_us_timeline['Date'] = vaccine_data_us_timeline[
    'Date'].astype('datetime64[ns]')

# %%

#Checking unique values of states in US dataset

unique_us_states = set(vaccine_data_us_timeline['Province_State'])

# There are some values in the state column which arent actual US states
# or are just departments related to the US states.

# %%

# Creating a list of "states" in the vaccine_data_us_timeline which are departments
from the US dataframe:
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

unique_us_regions = set(vaccine_data_us_timeline['Country_Region'])

# We can see that US is the only value here

# %%

# Checking for unique values of Vaccine_Type from US dataset

unique_vax_us = set(vaccine_data_us_timeline['Vaccine_Type'])

# We can see that there are Unnassigned and Unknown values as well as Pfizer,
# Moderna and Jannsen. Theres also an All which i assume contains a sum of them.

# I believe Unknown and Unassigned can be merged as one
# %%

print(vaccine_data_us_timeline['Doses_admin'].max())
# %%

# Merging all rows that are unnassigned and unknown to a single one

unknown_and_unnassigned = vaccine_data_us_timeline[
    (vaccine_data_us_timeline["Vaccine_Type"] == 'Unassigned') | 
    (vaccine_data_us_timeline["Vaccine_Type"] == 'Unknown')]

# Dropping the unknown and unnassigned from the main dataframe
vaccine_data_us_timeline.drop(index = unknown_and_unnassigned.index, inplace = True)

# Doing a common sum of values of Unknown and unnassigned on equal 
# country, state, and date

# unknown_and_unnassigned.groupby(['Province_State','Date',
#                                  'Country_Region','FIPS','Lat','Long_',
#                                  ])



# del unknown_and_unnassigned # Deleting from memory


# %%
# Changing date column to a date variable

time_series_covid19_vaccine_global['Date'] = time_series_covid19_vaccine_global['Date'].astype('datetime64[ns]')


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
    time_series_covid19_vaccine_global[~time_series_covid19_vaccine_global['Province_State'].notna()]['Country_Region'])

# %%

#print(ts_vaccine_doses_admin_df[ts_vaccine_doses_admin_df['Country_Region'] == "US"])

# For some reason the global data does not have the US states separately.
# This means i gotta import and merge the us data with the global data


# %%
# Dropping all of the US values from the global dataframe
# as well as World values
to_remove = ["US", "US (Aggregate)", "World"]

for element in to_remove:

    time_series_covid19_vaccine_global = time_series_covid19_vaccine_global[~(
        time_series_covid19_vaccine_global["Country_Region"] == element)]


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

in_both = [
    element for element in unique_us_states if element in unique_global_states]

# According to this, they both have unique values of state by this point
# %%
# Adding Vaccine_Type column equaling to all for the global dataset for the merging
# time_series_covid19_vaccine_global["Vaccine_Type"] = "All"

# %%
# The column "People_partially_vaccinated" from the global dataset is the most
# similar to "Stage_One_Doses" from the US dataset
# This goes the same for the People_fully_vaccinated and Stage_two_doses
# so these will be renamed for the merger

# time_series_covid19_vaccine_global.rename(columns={"People_partially_vaccinated": "Stage_One_Doses",
#                               "People_fully_vaccinated": "Stage_Two_Doses"}, inplace=True)

# These columns seem to contain lots of nans at times so it might not be as
# important as Doses_admin

# %%
# Merging global dataframe with us dataframe
# merge_df = pd.merge(vaccine_data_us_timeline, time_series_covid19_vaccine_global, how='outer',
#                     on=['Country_Region', 'Province_State', 'Vaccine_Type', 'Doses_admin',
#                         'Stage_One_Doses', 'Stage_Two_Doses', 'Date'])

# %%

#Df with only "All" vaccine types


# total_global_vax = merge_df[["Province_State", "Vaccine_Type", "Country_Region",
#                              "Doses_admin", "Stage_One_Doses",
#                              "Stage_Two_Doses"
#                              ]].groupby(["Province_State","Country_Region","Vaccine_Type"]).sum().reset_index()




