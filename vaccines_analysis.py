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
# Data Dictionary According to the repository:
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


# %%
# print(vaccine_df.columns)

# %%

# This only contains current global data, and is not useful to
# train our algorithm

# print(vaccine_df[vaccine_df.notna()])

# %%
# Changing date column to a date variable

ts_vaccine_df['Date'] = ts_vaccine_df['Date'].astype('datetime64[ns]')
ts_vaccine_us_df['Date'] = ts_vaccine_us_df['Date'].astype('datetime64[ns]')

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

unique_us_states = set(ts_vaccine_us_df['Province_State'])

# %%
# Creating a list of "states" in the ts_vaccine_us_df which arent really states
# from the US dataframe:
not_really_states = ["Long Term Care (LTC) Program",
                     "Veterans Health Administration",
                     "Bureau of Prisons", "Department of Defense",
                     "Federal Bureau of Prisons", "Indian Health Services"]

# Dropping them
for element in not_really_states:
    ts_vaccine_us_df = ts_vaccine_us_df[~(
        ts_vaccine_us_df['Province_State'] == element)]


# %%
# Checking if states in us dataset are in global dataset

unique_us_states = set(ts_vaccine_us_df['Province_State'])
unique_global_states = set(ts_vaccine_df['Province_State'])

in_both = [
    element for element in unique_us_states if element in unique_global_states]

# According to this, they both have unique values of state by this point
# %%
# Adding Vaccine_Type column equaling to all for the global dataset for the merging
ts_vaccine_df["Vaccine_Type"] = "All"

# %%
# The column "People_partially_vaccinated" from the global dataset is the most
# similar to "Stage_One_Doses" from the US dataset
# This goes the same for the People_fully_vaccinated and Stage_two_doses
# so these will be renamed for the merger

ts_vaccine_df.rename(columns={"People_partially_vaccinated": "Stage_One_Doses",
                              "People_fully_vaccinated": "Stage_Two_Doses"}, inplace=True)

# These columns seem to contain lots of nans at times so it might not be as
# important as Doses_admin

# %%
# Merging global dataframe with us dataframe
merge_df = pd.merge(ts_vaccine_us_df, ts_vaccine_df, how='outer',
                    on=['Country_Region', 'Province_State', 'Vaccine_Type', 'Doses_admin',
                        'Stage_One_Doses', 'Stage_Two_Doses', 'Date'])

# %%


