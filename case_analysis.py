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

cases_df = data_imports.csse_covid_19_daily_reports()

# Droppin all NaN rows
cases_df.dropna(how='all', inplace=True)
cases_df.reset_index(inplace=True)

# Setting datatypes
cases_df['date'] = cases_df['date'].astype(
    'datetime64[ns]')

cases_df = cases_df.convert_dtypes()

# %%

# Checking for nan values in Combined_Key

rows_without_combined_key = cases_df[
    cases_df['Combined_Key'].isnull()]

# %% Df of rows without regions

rows_with_no_regions = cases_df[
    cases_df['Country_Region'].isnull()]

# %%

# The size of rows without country_region and Combined_key are the same, which
# suggests that the Country/Region and Province/State columns are likely
# separate from Country_Region and Province_State columns.
# This means these columns have to be combined somehow.

# index_country_regions_A = cases_df[
#     cases_df['Country_Region'].notna()].index

# index_country_regions_B = cases_df[
#     cases_df['Country/Region'].notna()].index

# intersection_of_indexes = index_country_regions_A.intersection(
#     index_country_regions_B)

# index_state_A = cases_df[
#     cases_df['Province_State'].notna()].index

# index_state_B = cases_df[
#     cases_df['Province/State'].notna()].index

# intersection_2 = index_state_A.intersection(index_state_B)

# Intersection is emtpy meaning that they are exclusive

# %% Fillling values of one column with the other to combine them

cases_df['Country_Region'] = cases_df[
    'Country_Region'].fillna(cases_df['Country/Region'])

cases_df['Province_State'] = cases_df[
    'Province_State'].fillna(cases_df['Province/State'])

# %% re-verifyin indexes with no nans to check if the number changed

# index_country_regions_A = cases_df[
#     cases_df['Country_Region'].notna()].index

# index_country_regions_B = cases_df[
#     cases_df['Country/Region'].notna()].index

# intersection_of_indexes = index_country_regions_A.intersection(
#     index_country_regions_B)

# index_state_A = cases_df[
#     cases_df['Province_State'].notna()].index

# index_state_B = cases_df[
#     cases_df['Province/State'].notna()].index

# intersection_2 = index_state_A.intersection(index_state_B)

# %% Dropping cols
# cases_df= cases_df.drop(
#     ['Province/State','Country/Region'],axis=1)

# %% Checking how many rows dont contain lat and long

# rows_with_lat = cases_df[
#      cases_df['Lat'].notna()].index

# rows_with_latitude = cases_df[
#      cases_df['Latitude'].notna()].index

# rows_with_long_ = cases_df[
#      cases_df['Long_'].notna()].index

# rows_with_longitude =cases_df[
#      cases_df['Longitude'].notna()].index


# %% Filling missing lat and long_ with Latitude and Longitude columns
cases_df['Lat'] = cases_df[
    'Lat'].fillna(cases_df['Latitude'])

cases_df['Long_'] = cases_df[
    'Long_'].fillna(cases_df['Longitude'])

# %% re-verifying

# rows_with_lat = cases_df[
#      cases_df['Lat'].notna()].index

# rows_with_latitude = cases_df[
#      cases_df['Latitude'].notna()].index

# rows_with_long_ = cases_df[
#      cases_df['Long_'].notna()].index

# rows_with_longitude =cases_df[
#      cases_df['Longitude'].notna()].index


# %% Dropping cols
# cases_df = cases_df.drop(
#     ['Latitude','Longitude'],axis = 1)


# %% List of counties with no Lat or Long

counties_without_coordinates = set(cases_df[
    (cases_df['Lat'].isnull()) |
    (cases_df['Long_'].isnull())]['Admin2'])
# %% df with rows that have no county

rows_without_county = cases_df[
    cases_df['Admin2'].isnull()]

# %% List of unique province_state

unique_province_states = set(cases_df['Province_State'])

# %% List of unique Country_Region

unique_country_regions = set(cases_df['Country_Region'])


# Noticed hat Puerto Rico is set as country as well as State within us country
# must check if there are any
# %%

# PR_as_country = cases_df[cases_df[
#     'Country_Region'] == 'Puerto Rico']

# PR_as_state = cases_df[cases_df[
#     'Province_State'] == 'Puerto Rico']

# PR_test = cases_df[
#     (cases_df['Province_State'] == 'Puerto Rico') &(
#         cases_df['date'] == '03-16-2020')]

# %%
# Dropping puerto rico values as a Country since the values are pretty
# insignificant

cases_df = cases_df.drop(
    cases_df[
        cases_df['Country_Region'] == 'Puerto Rico'].index)

# %%
# Checking if puerto rico is still there
# PR_as_country = cases_df[cases_df[
#     'Country_Region'] == 'Puerto Rico']

# %%
# Checking differences between Case_Datality_Ratio and Case-Fatality_Ratio
# cols.
# cases_df[cases_df['Case-Fatality_Ratio'].notna()]
# cases_df[cases_df['Case_Fatality_Ratio'].notna()]

# %% Filling Case_Fatality_Ratio nans with Case-Fatality_Ratio

cases_df['Case_Fatality_Ratio'
                            ] = cases_df[
                                'Case_Fatality_Ratio'].fillna(
                                    cases_df[
                                        'Case-Fatality_Ratio'])

# %% Dropping 'Case-Fatality_Ratio' columns

# cases_df = cases_df.drop(
#     'Case-Fatality_Ratio',axis = 1)

# %%
# Comparing insidence rates columns


# cases_df[cases_df['Incident_Rate'].notna()]
# cases_df[cases_df['Incidence_Rate'].notna()]

# %% Filling Incident_Rate nans with Incidence_Rate nans
cases_df['Incident_Rate'
                            ] = cases_df[
                                'Incident_Rate'].fillna(
                                    cases_df[
                                        'Incidence_Rate'])

# %% Dropping Incidence_Rate column

# cases_df = cases_df.drop(
#     'Incidence_Rate',axis = 1)

# %% Dropping unnecesary columns

unnecessary_cols = ['Last_Update', 'Combined_Key',
                    'Last Update', 'Incidence_Rate', 'Case-Fatality_Ratio',
                    'Latitude', 'Longitude', 'Province/State', 'Country/Region',
                    'index'
                    ]

cases_df.drop(unnecessary_cols, axis='columns',
                                 inplace=True)


# %% removing whitespaces from string columns

cols_to_strip = ['Admin2', 'Province_State', 'Country_Region']

for col in cols_to_strip:
    cases_df[col] = cases_df[
        col].str.strip()

# %% There are some columns which contain nan in all important values
# should take care of them somehow

# %% Case_Fatality_Ratio contains some "stringed" numbers which does not let it
# become a float dtype
#
# There are some #DIV/0! in the cells which doesnt allow it to become float
# Removing these should work

cases_df['Case_Fatality_Ratio'
                            ] = cases_df[
                                'Case_Fatality_Ratio'].str.replace('#DIV/0!', '')

# %% Turning to float type

cases_df['Case_Fatality_Ratio'] = pd.to_numeric(cases_df['Case_Fatality_Ratio'])

cases_df['Case_Fatality_Ratio'] = cases_df['Case_Fatality_Ratio'].astype("Float64")

# %% Fixing negative values

cols_to_fix = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
               'Case_Fatality_Ratio']

for col in cols_to_fix:
    cases_df[col] = cases_df[col].abs()

# %% List of not real country regions within the dataset

non_country_regions = ['Summer Olympics 2020', 'Cruise Ship','Diamond Princess',
                       ]

# %% List of unique province_state

unique_province_states = set(cases_df['Province_State'])

# %% List of unique Country_Region

unique_country_regions = set(cases_df['Country_Region'])

# %%

unique_counties = set(cases_df['Admin2'])

# %% List of countries that might need to be renamed
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


# %% Inspecting the aforementioned countries
# for i,j in merge_countries:
#     print(i)
#     print()
#     print(cases_df[cases_df['Country_Region'] == i][['Admin2','Province_State','Country_Region']])
#     print()
#     print(j)
#     print()
#     print(cases_df[cases_df['Country_Region'] == j][['Admin2','Province_State','Country_Region']])

# Bahamas, The only has 3 rows, while Bahamas has more.

# Czech Republic only has 10 rows, whilst Czechia has more

# Gambia, The only has 4 rows, while Gambia has more

# Hong Kong SAR only has 1 row and hong kong has 48. Should probably turn it
# into a Chinese state

# Iran (Islamic Republic of) only has 1 row while Iran has more

# Macao SAR only has 1 row while Macau has 48. Shoul probably turn into chinese
# state.

# Russian Federation only has 1 row while Russia has a bunch

# South Korea has 48 rows while Korea, South has 561

# Republic of Korea only has 1 row

# Taiwan has 48 rows while Taiwan* has 561. should probably turn into chinese
# state.

# Mainland China has 1517 rows while China has 19123

# UK has 40 rows while United Kingdom has 8490
# %% Renaming the above touples
for old,new in merge_countries:
    cases_df.loc[cases_df['Country_Region'] == old,'Country_Region'] = new
    
# %% Checking duplicates

# dups = cases_df.duplicated(['Admin2','Province_State','Country_Region','date'],
#                            keep=False)
# dups_df = cases_df[dups]

# %% Dropping the duplicates while keeping the highest values

cases_df = cases_df.sort_values(
    ['Confirmed','Deaths','Recovered']).drop_duplicates(
        ['Admin2','Province_State','Country_Region','date'],keep='last')

# test = cases_df[(cases_df['Province_State'] == 'District of Columbia') & (cases_df['date'] == '2020-03-22 00:00:00')]

# %%

# UK_data = cases_df[cases_df['Country_Region'] == 'UK']
# UK_data2 = cases_df[cases_df['Country_Region'] == 'United Kingdom']

# %% Fixing UK data

# Since UK rows are country level data, adding United Kingdom to its
# "State" column so that it is interpreted as so.

# cases_df.loc[cases_df['Country_Region'] == 'UK','Province_State'] = 'United Kingdom'

# Renaming UK to United Kingdom

# cases_df['Country_Region'] = cases_df['Country_Region'].replace('UK','United Kingdom')

# Replacing UK with United Kindom in the States column 

# cases_df['Province_State'] = cases_df['Province_State'].replace('UK','United Kingdom')

# Now replacing the NAN values in United Kingdom's Povince_State with
# United Kingdom as it is the same type of value.

# cases_df.loc[(cases_df['Province_State'].isna()) & 
#              (cases_df['Country_Region'] == 'United Kingdom'),
#              'Province_State'] = 'UK'

# Country level sum stopped after June 2020 so if i want to proceed with a sum
# ill have to do it myself

# %% Checking for UK dups
# dups = cases_df[cases_df['Country_Region'] == 'United Kingdom'].duplicated(['Province_State','Country_Region','date'])
# UK_data = UK_data2 = cases_df[cases_df['Country_Region'] == 'United Kingdom']

# UK_dups = UK_data[dups]

# No dups

# %%
# china_data = cases_df.loc[cases_df['Country_Region'] == 'China']

# china_mainland_data = cases_df.loc[cases_df['Country_Region'] == 'Mainland China']

# The midland china stopped being reported after march 2020, whilst
# china is up to date
# %%
# Getting unique chinese states and midland states
# unique_china_states = set(china_data['Province_State'])
# unique_midland_states = set(china_mainland_data['Province_State'])


# # Doing an intersection of their states
# china_intersection = unique_china_states.intersection(
#     unique_midland_states)

# # Getting their symmetric difference
# china_symmetric_diff = unique_china_states ^ unique_midland_states

# Hong Kong, Macau and Unknown are their differences
# These 3 lie in China data, not midland

# %%

# Renaming Mainland China to just China

# cases_df.loc[cases_df['Country_Region'] == 'Mainland China','Country_Region'] = 'China'

# %% Removing duplicate rows from china

# Keeping first and removing second of dups

# Boolean of dups from slice
# dups = cases_df[cases_df['Country_Region'] == 'China'].duplicated(['Province_State','Country_Region','date'])

# china_data = cases_df.loc[cases_df['Country_Region'] == 'China']

# china_dups = china_data[dups]

# %%
# cases_df[cases_df['Country_Region'] == 'China'] = cases_df[cases_df['Country_Region'] == 'China'].drop_duplicates(
#     ['Province_State','Country_Region','date'])

# %%

# bahamas_data = cases_df[cases_df['Country_Region'] == 'Bahamas']
# the_bahamas_data = cases_df[cases_df['Country_Region'] == 'Bahamas, The']

# %%
# Renaming Bahamas, The to simply Bahamas

# cases_df.loc[cases_df['Country_Region'] == 'Bahamas, The','Country_Region'] = 'Bahamas'

# %%
# bahamas_data = cases_df[cases_df['Country_Region'] == 'Bahamas']
# the_bahamas_data = cases_df[cases_df['Country_Region'] == 'Bahamas, The']


# %%
# dups = cases_df[cases_df['Country_Region'] == 'Bahamas'].duplicated(['Province_State','Country_Region','date'])

# bahamas_dups = bahamas_data[dups]
# No dups
# %%
# 'Czechia' to 'Czech Republic' to
# Czechia = cases_df.loc[cases_df['Country_Region'] == 'Czechia',:]

# Czech_Republic = cases_df.loc[cases_df['Country_Region'] == 'Czech Republic',:]

# %%
# Renaming Czechia to Czech Republic
# cases_df.loc[cases_df['Country_Region'] == 'Czechia','Country_Region'] = 'Czech Republic'

# %%
# Checking for dups
# dups = cases_df[cases_df['Country_Region'] == 'Czech Republic'].duplicated(['Province_State','Country_Region','date'])
# Czech_Republic = cases_df.loc[cases_df['Country_Region'] == 'Czech Republic',:]
# Czech_Republic_dups = Czech_Republic[dups]
# No dups

# %% Checking for strings that are in both countries and province
unique_province_states = set(cases_df['Province_State'])
unique_country_regions = set(cases_df['Country_Region'])

intersection = unique_province_states.intersection(unique_country_regions)

# There are a couple of strings in both that need to be dealt with.
# %%
for e in intersection:
    print(e)
    print()
    print("Country Len: ",len(cases_df[cases_df['Country_Region'] == e]))
    print("State Len: ",len(cases_df[cases_df['Province_State'] == e]))
    print()

# %%
# denmar_state = cases_df[cases_df['Province_State'] == 'Denmark']
# Denmark as state also has denmark as country already
# denmark_country = cases_df[cases_df['Country_Region'] == 'Denmark']
# This means that where Denmark is also a state, its the sum of all denmark
# state values, similar to with UK. This seems to be a pattern throughout the
# dataset

   

# %% Filtering only countries where there is an intersection (between state
# value and country value) but also where they are not equal within the same
# row (which indicates its not just a sum of every state in the country)


# List of touples with "regions" to be turned to state with their respective
# regions

regions_to_state = []
exceptions = ['Georgia','Diamond Princess','Cruise Ship','Luxembourg']
# There is a US state named georgia and a country as well
# Diamond Princess is a british cruise ship
# Luxembourg is a state in Belgium, but there is also a Luxembourg country
regions_unsure = []


for e in intersection:
    
    if e not in exceptions:
        rows_as_state = cases_df[(cases_df['Country_Region'] != e) &
                                           (cases_df['Province_State'] == e)]
        
        rows_as_region = cases_df[cases_df['Country_Region'] == e]
        
        len_as_state = len(rows_as_state)
        
        len_as_region = len(rows_as_region)
        
        country = set(rows_as_state['Country_Region'])
        
        
        if (len_as_state > 0) and (len_as_region > 0):
            print(e)
            print()
            print("Len as state: ",len_as_state)
            print()
            print("Len as region: ", len_as_region)
            print()
            print("Supposed country: ", country)
            print()
            
            #If the country set contains more than one then this wont work
            if len(country) == 1:
                
                # If it appears more as a region than a state then turn to full
                # region
                if len_as_region > len_as_state:
                
                    regions_unsure.append((e,country))
                    
                # If it appears more as state than region, then turn to full state
                # with its corresponding region
                elif len_as_region < len_as_state:
                    regions_to_state.append((e,country))
        
print(regions_to_state)

# %% Applying conversion of country to states fo the previously
# collected states.
for i,j in regions_to_state:
    
    country = list(j)[0] # Accessing first element of the set which is the country
    
    cases_df.loc[cases_df['Country_Region'] == i, 'Province_State'] = i
    
    cases_df.loc[cases_df['Country_Region'] == i, 'Country_Region'] = country

#%% removing dups again

cases_df = cases_df.sort_values(
    ['Confirmed','Deaths','Recovered']).drop_duplicates(
        ['Admin2','Province_State','Country_Region','date'],keep='last')

#%% Sorting dataframe by date

cases_df = cases_df.sort_values('date').reset_index()


#%% Forward fill nan cases,death,recoveries
# we would need to iterate ber Admin2, then state, and then country to do this
# propperly

# we gotta take into consideration values that are unknonwn or unnassigned

test =cases_df[cases_df['Admin2'].notna()].sort_values(
    ['Admin2','Province_State','Country_Region','date'])

test_nan_cases = test[test['Confirmed'].isna()]

# There dont seem to be any County level missing values
# %% Attempting the same only on a state level
test =cases_df[cases_df['Admin2'].isna()].sort_values(
    ['Province_State','Country_Region','date'])

# There are some rows with missing confirmed cases

# %% 

# Unique set of state,country touple
state_country = cases_df[cases_df['Admin2'].isna() & cases_df[
    'Province_State'].notna()][['Province_State','Country_Region']].values

state_country_set = set()

[state_country_set.add((element[0],element[1])) for element in state_country]

# for state,country in state_country



# %% Removing rows with NaN cases,deaths,recoveries



# %% Create column with estimated daily counts



# %% Create value (row) per country with Sum of all country cases,deaths,recoveries

# %% Turn some of the US states from "County, State" to pure state


# %%
# Fill lat and long nan values
rows_with_nan_lat_long = cases_df[(cases_df['Lat'].isna()) |
                                  (cases_df['Long_'].isna())]



# %% Take care of unnassigned values


# %% Exporting cleaned dataframe
#cases_df.to_csv(".\\cases_cleaned.csv")