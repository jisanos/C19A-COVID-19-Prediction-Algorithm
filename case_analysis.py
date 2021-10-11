# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:00:40 2021

This script will serve as a more in depth analysis of the covid test/cases data

@author: jis
"""
# %%

import pandas as pd
import glob
import matplotlib.pyplot as plt
import data_imports
import numpy as np


# %%

csse_covid_19_daily_reports = data_imports.csse_covid_19_daily_reports()

# Droppin all NaN rows
csse_covid_19_daily_reports.dropna(how='all', inplace=True)
csse_covid_19_daily_reports.reset_index(inplace=True)

# Setting datatypes
csse_covid_19_daily_reports['date'] = csse_covid_19_daily_reports['date'].astype(
    'datetime64[ns]')

csse_covid_19_daily_reports = csse_covid_19_daily_reports.convert_dtypes()

# %%

# Checking for nan values in Combined_Key

rows_without_combined_key = csse_covid_19_daily_reports[
    csse_covid_19_daily_reports['Combined_Key'].isnull()]

# %% Df of rows without regions

rows_with_no_regions = csse_covid_19_daily_reports[
    csse_covid_19_daily_reports['Country_Region'].isnull()]

# %%

# The size of rows without country_region and Combined_key are the same, which
# suggests that the Country/Region and Province/State columns are likely
# separate from Country_Region and Province_State columns.
# This means these columns have to be combined somehow.

# index_country_regions_A = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Country_Region'].notna()].index

# index_country_regions_B = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Country/Region'].notna()].index

# intersection_of_indexes = index_country_regions_A.intersection(
#     index_country_regions_B)

# index_state_A = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Province_State'].notna()].index

# index_state_B = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Province/State'].notna()].index

# intersection_2 = index_state_A.intersection(index_state_B)

# Intersection is emtpy meaning that they are exclusive

# %% Fillling values of one column with the other to combine them

csse_covid_19_daily_reports['Country_Region'] = csse_covid_19_daily_reports[
    'Country_Region'].fillna(csse_covid_19_daily_reports['Country/Region'])

csse_covid_19_daily_reports['Province_State'] = csse_covid_19_daily_reports[
    'Province_State'].fillna(csse_covid_19_daily_reports['Province/State'])

# %% re-verifyin indexes with no nans to check if the number changed

# index_country_regions_A = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Country_Region'].notna()].index

# index_country_regions_B = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Country/Region'].notna()].index

# intersection_of_indexes = index_country_regions_A.intersection(
#     index_country_regions_B)

# index_state_A = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Province_State'].notna()].index

# index_state_B = csse_covid_19_daily_reports[
#     csse_covid_19_daily_reports['Province/State'].notna()].index

# intersection_2 = index_state_A.intersection(index_state_B)

# %% Dropping cols
# csse_covid_19_daily_reports= csse_covid_19_daily_reports.drop(
#     ['Province/State','Country/Region'],axis=1)

# %% Checking how many rows dont contain lat and long

# rows_with_lat = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Lat'].notna()].index

# rows_with_latitude = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Latitude'].notna()].index

# rows_with_long_ = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Long_'].notna()].index

# rows_with_longitude =csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Longitude'].notna()].index


# %% Filling missing lat and long_ with Latitude and Longitude columns
csse_covid_19_daily_reports['Lat'] = csse_covid_19_daily_reports[
    'Lat'].fillna(csse_covid_19_daily_reports['Latitude'])

csse_covid_19_daily_reports['Long_'] = csse_covid_19_daily_reports[
    'Long_'].fillna(csse_covid_19_daily_reports['Longitude'])

# %% re-verifying

# rows_with_lat = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Lat'].notna()].index

# rows_with_latitude = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Latitude'].notna()].index

# rows_with_long_ = csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Long_'].notna()].index

# rows_with_longitude =csse_covid_19_daily_reports[
#      csse_covid_19_daily_reports['Longitude'].notna()].index


# %% Dropping cols
# csse_covid_19_daily_reports = csse_covid_19_daily_reports.drop(
#     ['Latitude','Longitude'],axis = 1)


# %% List of counties with no Lat or Long

counties_without_coordinates = set(csse_covid_19_daily_reports[
    (csse_covid_19_daily_reports['Lat'].isnull()) |
    (csse_covid_19_daily_reports['Long_'].isnull())]['Admin2'])
# %% df with rows that have no county

rows_without_county = csse_covid_19_daily_reports[
    csse_covid_19_daily_reports['Admin2'].isnull()]

# %% List of unique province_state

unique_province_states = set(csse_covid_19_daily_reports['Province_State'])

# %% List of unique Country_Region

unique_country_regions = set(csse_covid_19_daily_reports['Country_Region'])

# %% List of countries that might need to be merged
merge_countries = [('Bahamas', 'Bahamas, The'),
                   ('Czech Republic', 'Czechia'),
                   ('Gambia', 'Gambia, The'),
                   ('Hong Kong', 'Hong Kong SAR'),
                   ('Iran', 'Iran (Islamic Republic of)'),
                   ('Macau', 'Macao SAR'),
                   ('Russia', 'Russian Federation'),
                   ('South Korea', 'Korea, South'),
                   ('Taiwan', 'Taiwan*'),
                   ('Mainland China', 'China'),  # Maybe?
                   ]

# Noticed hat Puerto Rico is set as country as well as State within us country
# must check if there are any
# %%

# PR_as_country = csse_covid_19_daily_reports[csse_covid_19_daily_reports[
#     'Country_Region'] == 'Puerto Rico']

# PR_as_state = csse_covid_19_daily_reports[csse_covid_19_daily_reports[
#     'Province_State'] == 'Puerto Rico']

# PR_test = csse_covid_19_daily_reports[
#     (csse_covid_19_daily_reports['Province_State'] == 'Puerto Rico') &(
#         csse_covid_19_daily_reports['date'] == '03-16-2020')]

# %%
# Dropping puerto rico values as a Country since the values are pretty
# insignificant

csse_covid_19_daily_reports = csse_covid_19_daily_reports.drop(
    csse_covid_19_daily_reports[
        csse_covid_19_daily_reports['Country_Region'] == 'Puerto Rico'].index)

# %%
# Checking if puerto rico is still there
# PR_as_country = csse_covid_19_daily_reports[csse_covid_19_daily_reports[
#     'Country_Region'] == 'Puerto Rico']

# %%
# Checking differences between Case_Datality_Ratio and Case-Fatality_Ratio
# cols.
# csse_covid_19_daily_reports[csse_covid_19_daily_reports['Case-Fatality_Ratio'].notna()]
# csse_covid_19_daily_reports[csse_covid_19_daily_reports['Case_Fatality_Ratio'].notna()]

# %% Filling Case_Fatality_Ratio nans with Case-Fatality_Ratio

csse_covid_19_daily_reports['Case_Fatality_Ratio'
                            ] = csse_covid_19_daily_reports[
                                'Case_Fatality_Ratio'].fillna(
                                    csse_covid_19_daily_reports[
                                        'Case-Fatality_Ratio'])

# %% Dropping 'Case-Fatality_Ratio' columns

# csse_covid_19_daily_reports = csse_covid_19_daily_reports.drop(
#     'Case-Fatality_Ratio',axis = 1)

# %%
# Comparing insidence rates columns


# csse_covid_19_daily_reports[csse_covid_19_daily_reports['Incident_Rate'].notna()]
# csse_covid_19_daily_reports[csse_covid_19_daily_reports['Incidence_Rate'].notna()]

# %% Filling Incident_Rate nans with Incidence_Rate nans
csse_covid_19_daily_reports['Incident_Rate'
                            ] = csse_covid_19_daily_reports[
                                'Incident_Rate'].fillna(
                                    csse_covid_19_daily_reports[
                                        'Incidence_Rate'])

# %% Dropping Incidence_Rate column

# csse_covid_19_daily_reports = csse_covid_19_daily_reports.drop(
#     'Incidence_Rate',axis = 1)

# %% Dropping unnecesary columns

unnecessary_cols = ['Last_Update', 'Combined_Key',
                    'Last Update', 'Incidence_Rate', 'Case-Fatality_Ratio',
                    'Latitude', 'Longitude', 'Province/State', 'Country/Region',
                    'index'
                    ]

csse_covid_19_daily_reports.drop(unnecessary_cols, axis='columns',
                                 inplace=True)


# %% removing whitespaces from string columns

cols_to_strip = ['Admin2', 'Province_State', 'Country_Region']

for col in cols_to_strip:
    csse_covid_19_daily_reports[col] = csse_covid_19_daily_reports[
        col].str.strip()

# %% There are some columns which contain nan in all important values
# should take care of them somehow

# %% Case_Fatality_Ratio contains some "stringed" numbers which does not let it
# become a float dtype
#
# There are some #DIV/0! in the cells which doesnt allow it to become float
# Removing these should work

csse_covid_19_daily_reports['Case_Fatality_Ratio'
                            ] = csse_covid_19_daily_reports[
                                'Case_Fatality_Ratio'].str.replace('#DIV/0!', '')

# %% Turning to float type


csse_covid_19_daily_reports['Case_Fatality_Ratio'
                            ] = csse_covid_19_daily_reports[
                                'Case_Fatality_Ratio'].astype("Float64")

# %% Fixing negative values

cols_to_fix = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
               'Case_Fatality_Ratio']

for col in cols_to_fix:
    csse_covid_19_daily_reports[col] = csse_covid_19_daily_reports[col].abs()

# %% List of not real country regions within the dataset

non_country_regions = ['Summer Olympics 2020']

# %% List of unique province_state

unique_province_states = set(csse_covid_19_daily_reports['Province_State'])

# %% List of unique Country_Region

unique_country_regions = set(csse_covid_19_daily_reports['Country_Region'])

# %%

unique_counties = set(csse_covid_19_daily_reports['Admin2'])

# %% List of countries that might need to be merged
merge_countries = [('Bahamas', 'Bahamas, The'),
                   ('Czech Republic', 'Czechia'),
                   ('Gambia', 'Gambia, The'),
                   ('Hong Kong', 'Hong Kong SAR'),
                   ('Iran', 'Iran (Islamic Republic of)'),
                   ('Macau', 'Macao SAR'),
                   ('Russia', 'Russian Federation'),
                   ('South Korea', 'Korea, South'),
                   ('Taiwan', 'Taiwan*'),
                   ('Mainland China', 'China'),  # Maybe?
                   ]
