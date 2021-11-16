# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:00:40 2021

This script will serve as a more in depth analysis of the covid test/cases data

@author: jis
"""
# %%

import pandas as pd
import data_imports
import numpy as np
import time
from geopy.geocoders import Nominatim


# %% Importing data

cases_df = data_imports.csse_covid_19_daily_reports()

# Droppin all full NaN rows
cases_df.dropna(how='all', inplace=True)
cases_df.reset_index(inplace=True)
cases_df.drop('index',axis = 1,inplace=True)

# Setting datatypes
cases_df['date'] = cases_df['date'].astype(
    'datetime64[ns]')

# cases_df = cases_df.convert_dtypes()

#Assigning datatypes
dtypes = {'Lat':'float64',
          'Long_':'float64',
          'Confirmed':'float64',
          'Deaths':'float64',
          'Recovered':'float64',
          'Active':'float64',
          'Incident_Rate':'float64',
          'Case_Fatality_Ratio':'float64', #is dealt with later
          'Latitude':'float64',
          'Longitude':'float64',
          'Incidence_Rate':'float64',
          'Case-Fatality_Ratio':'float64',
          'Admin2':'string',
          'Province_State':'string',
          'Country_Region':'string',
          'Province/State':'string',
          'Country/Region':'string',
          'Province_State':'string',}

cases_df = cases_df.astype(dtypes)
# %% defining function that will remove dups and reset index for later use
def remove_dups_and_reset_index(df):
    

    df = df.sort_values(
        ['Confirmed','Deaths','Recovered']).drop_duplicates(
            ['Admin2','Province_State','Country_Region','date'],keep='last')


    df = df.sort_values('date').reset_index(drop = True)
    
    return df
# %%

# Checking for nan values in Combined_Key

# rows_without_combined_key = cases_df[
#     cases_df['Combined_Key'].isnull()]

# %% Df of rows without regions

# rows_with_no_regions = cases_df[
#     cases_df['Country_Region'].isnull()]

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

# counties_without_coordinates = set(cases_df[
#     (cases_df['Lat'].isnull()) |
#     (cases_df['Long_'].isnull())]['Admin2'])
# %% df with rows that have no county

# rows_without_county = cases_df[
#     cases_df['Admin2'].isnull()]

# %% List of unique province_state

# unique_province_states = set(cases_df['Province_State'])

# %% List of unique Country_Region

# unique_country_regions = set(cases_df['Country_Region'])


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

cases_df['Case_Fatality_Ratio'] = cases_df[
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
cases_df['Incident_Rate'] = cases_df[
                                'Incident_Rate'].fillna(
                                    cases_df[
                                        'Incidence_Rate'])

# %% Dropping Incidence_Rate column

# cases_df = cases_df.drop(
#     'Incidence_Rate',axis = 1)

# %% Dropping unnecesary columns

unnecessary_cols = ['Last_Update',
                    'Combined_Key',
                    'Last Update', 'Incidence_Rate', 'Case-Fatality_Ratio',
                    'Latitude', 'Longitude', 'Province/State', 'Country/Region'
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

# cases_df['Case_Fatality_Ratio'
#                             ] = cases_df[
#                                 'Case_Fatality_Ratio'].str.replace('#DIV/0!', '')
# Issue seems to be resolved in the branch

# %% Turning to float type

cases_df['Case_Fatality_Ratio'] = pd.to_numeric(cases_df['Case_Fatality_Ratio'])

cases_df['Case_Fatality_Ratio'] = cases_df['Case_Fatality_Ratio'].astype("float64")

# %% Fixing negative values

cols_to_fix = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
               'Case_Fatality_Ratio']

for col in cols_to_fix:

    cases_df[col] = cases_df[col].abs()


# %% checking if all values are positive
#print((cases_df['Confirmed'].values < 0).any())
    
# %% List of not real country regions within the dataset

non_country_regions = ['Summer Olympics 2020', 'Cruise Ship','Diamond Princess',
                       ]
# Removing them for consistency and cleanliness

for element in non_country_regions:
    cases_df = cases_df.drop(
        cases_df[cases_df['Province_State'].str.contains(element)].index)

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

# cases_df = cases_df.sort_values(
#     ['Confirmed','Deaths','Recovered']).drop_duplicates(
#         ['Admin2','Province_State','Country_Region','date'],keep='last')

cases_df = remove_dups_and_reset_index(cases_df)

# test = cases_df[(cases_df['Province_State'] == 'District of Columbia') & (cases_df['date'] == '2020-03-22 00:00:00')]



# %% Checking for strings that are in both countries and province
unique_province_states = set(cases_df['Province_State'])
unique_country_regions = set(cases_df['Country_Region'])

intersection = unique_province_states.intersection(unique_country_regions)

# There are a couple of strings in both that need to be dealt with.
# %%
# for e in intersection:
#     print(e)
#     print()
#     print("Country Len: ",len(cases_df[cases_df['Country_Region'] == e]))
#     print("State Len: ",len(cases_df[cases_df['Province_State'] == e]))
#     print()

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
            # print(e)
            # print()
            # print("Len as state: ",len_as_state)
            # print()
            # print("Len as region: ", len_as_region)
            # print()
            # print("Supposed country: ", country)
            # print()
            
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

#%% removing dups again and Sorting dataframe by date

cases_df = remove_dups_and_reset_index(cases_df)

# %%
# Manually renaming Washington D.C. state to District of Columbia
cases_df.loc[cases_df.Province_State.str.contains('D.C.'),'Admin2'] = 'District of Columbia'

cases_df.loc[cases_df.Province_State.str.contains('D.C.'),'Province_State'] = 'District of Columbia'

# %% Turn some of the US states from "County, State" to just state with county
# as admin2

start_time = time.time()
filter_in_us = (cases_df['Country_Region'] == 'US') #only us states
filter_in_split = (cases_df['Province_State'].str.contains(',')) #only values that have commas in it
filter_out_diamond_princes = np.logical_not(cases_df['Province_State'].str.lower().str.contains('diamond')) # To ignore diamond princess entries
filter_out_states_with_US = np.logical_not(cases_df['Province_State'].str.contains('US') | 
                              cases_df['Province_State'].str.contains('U.S.'))

filter_all = filter_in_us & filter_in_split & filter_out_diamond_princes & filter_out_states_with_US

def reformat_county_state(x):
    
    # Splittin on comman and extracting county and state
    splt = x['Province_State'].str.split(',').values
    county = splt[0][0].strip()
    state = splt[0][1].strip()
    state = data_imports.abbreviations_to_us_states[state]
    print(state)
    
    x['Province_State'] = state
    x['Admin2'] = county
    
    return x

cases_df.loc[filter_all,:] = cases_df.loc[filter_all,:].groupby('Province_State').apply(reformat_county_state)



print(time.time() - start_time)



#%% removing dups again and reseting index
cases_df = remove_dups_and_reset_index(cases_df)
#%% Checking d.c. rows

# wa_dc = cases_df[cases_df['Province_State'].str.contains('D.C.')]
# dc = cases_df[cases_df['Province_State'].str.contains('District of Columbia')]
# dc_county = cases_df[cases_df['Admin2'].str.contains('Washington') &
#                      cases_df['Province_State'].str.contains('Virginia')]

# The D.C. rows seem to be a pre of the District of Columbia rows

# Washington County and Washington D.C. are different counties

# %% Replaces counties that are equal to state with NaN

filter_equal = (cases_df['Admin2'] == cases_df['Province_State'])


cases_df.loc[filter_equal,'Admin2'] = np.nan

# %% Same as before but with states to country

filter_equal = (cases_df['Province_State'] == cases_df['Country_Region'])

cases_df.loc[filter_equal,'Province_State'] = np.nan

#%% removing dups again and reseting index

cases_df = remove_dups_and_reset_index(cases_df)
# %%
import matplotlib.pyplot as plt
to_plot = cases_df.loc[cases_df.Country_Region == 'Peru',['Deaths','date']]

plt.plot(to_plot.date,to_plot.Deaths)
plt.show()

# %%
## Attempting groupby method (Which is a lot more efficient) to fill NaNs

def filler(x):        
    
    
    
    # removing outliers from cumulative data
    cols = ['Deaths', 'Confirmed', 'Recovered']   
    
    for col in cols:
        
        std = x[col].std() #Getting the standard deviations
        
        diff = x[col].diff() #getting the difference to compare with the std
        
        # Getting the index of only the outlier data
        # The shift back is to get the outlier since the diff will be 
        # shifted forward. 
        outliers = x.shift(-1)[diff.abs() > std].index
        
        # if there are outliers continue
        if len(outliers) > 0:
            
            # Asggigning nan to the outliers
            x.loc[outliers,col] = np.nan 
            
    
        
    # Doing interpolation method
    
    first_index = x.head(1).index
    
    x.loc[first_index,'Confirmed'] = 0
    x.loc[first_index,'Deaths'] = 0
    x.loc[first_index,'Recovered'] = 0

    x[cols] = x[cols].interpolate().round()

    # x['Confirmed'] = x['Confirmed'].interpolate().round()
    # x['Deaths'] = x['Deaths'].interpolate().round()
    # x['Recovered'] = x['Recovered'].interpolate().round()
    
    
    #According to the README, incident reate is cases per 100k persons
    #case fatality ratio is number of recorded deaths * 100/number of confirmed cases
    #Active is total cases - total recovered - total deaths
    
        
    x['Case_Fatality_Ratio'] = x['Deaths'] * 100 / x['Confirmed']
    # Incident rate should be calculated after "New values" are made
    
    # Setting lat and long values with their means for consistency.
    x['Lat'] = x['Lat'].mean()
    x['Long_'] = x['Long_'].mean()
    
 
    
    return x


start_time = time.time()
cases_df = cases_df.groupby(['Admin2','Province_State','Country_Region'
                             ],dropna=False).apply(filler)

print(time.time() - start_time)



# %%
import matplotlib.pyplot as plt
to_plot = cases_df.loc[(cases_df.Country_Region == 'Peru') & (cases_df.Province_State.notna()),['Deaths','date']]

plt.plot(to_plot.date,to_plot.Deaths)

plt.show()
grp = cases_df.loc[(cases_df.Country_Region == 'Peru')
                 & (cases_df.Province_State.notna()),['Province_State','Deaths','date']].groupby(['Province_State'])
for g,df in grp:
    plt.title(g)
    plt.plot(df.date, df.Deaths)
    plt.show()


# %% Create a column "New_Cases" with only the total cases on that date

def date_cases(x):
    # This method assumes that you are providing the grouped dataframes by date
    # x = x.reset_index(drop = True)
    
    # This will create new column by substracting confirmed with its shifted
    # self. Any value that is NA will be the first value which does not have
    # any prior value to substract with, thus filling these with 0 make no 
    # difference.

    x['New_Confirmed'] = x['Confirmed'].diff().fillna(0).abs()
    
    
    # Replacing zeros with nan so that interpolation can take care of them
    x['New_Confirmed'] = x['New_Confirmed'].replace(0,np.nan)
    
    
    x['New_Confirmed'] = x['New_Confirmed'].interpolate().round()
    
    # Now calculating the moving average
    x['New_Confirmed'] = x['New_Confirmed'].rolling(window=7).mean()
    
    # Since there is the chance of there being negative values due to inconsistent,
    # cumulative data, we will just take their absolute value and
    # then make a new cumulative sum
    
    x['Confirmed'] = x['New_Confirmed'].cumsum()
    
    
    # Doing the same with deaths and recoveries, but only if they are not
    # all NaNs.
    
    x['New_Deaths'] = x['Deaths'].diff().fillna(0).abs()
    x['Deaths'] = x['New_Deaths'].cumsum()
    

    x['New_Recovered'] = x['Recovered'].diff().fillna(0).abs()
    x['Recovered'] = x['New_Recovered'].cumsum()
        
    return x    
    

cases_df = cases_df.groupby(['Admin2','Province_State','Country_Region'
                              ],dropna=False).apply(date_cases)




# %%
import matplotlib.pyplot as plt
to_plot = cases_df.loc[(cases_df.Country_Region == 'Peru') & (cases_df.Province_State.notna()),['Deaths','date']]

plt.plot(to_plot.date,to_plot.Deaths)
plt.show()


to_plot = cases_df.loc[(cases_df.Country_Region == 'Peru'),['New_Deaths','date']]

plt.plot(to_plot.date,to_plot.New_Deaths)
plt.show()

# %% Finding latitude and longitude to locations that contain 0,0 or nans


# filter_zeros = ((cases_df['Lat'] == 0) | (cases_df['Long_'] == 0) |
#                   (cases_df['Lat'].isna()) | (cases_df['Long_'].isna()))

# cases_zeros = cases_df.loc[filter_zeros,:]


# locator = Nominatim(user_agent="http")

# def find_loc(x):
    
#     #Getting state and country values
#     state = list(set(x['Province_State']))[0]
#     country = list(set(x['Country_Region']))[0]
    
#     # Combining them to a single string
#     country_state = str(state) + ", " + str(country)
#     print(country_state)
#     # Getting their location
#     location = locator.geocode(country_state)
#     print(location)
#     # Assigning their location
#     if location != None:
#         x['Lat'] = location.latitude
#         x['Long_'] = location.longitude
    
#     return x

# cases_zeros = cases_zeros.groupby(['Province_State','Country_Region'],
#                                  dropna=False).apply(find_loc)




# cases_df = cases_df[np.logical_not(filter_zeros)] #Removing old entries

# # appending new entries
# cases_df = cases_df.append(cases_zeros,ignore_index = True)

# %%
cases_df = remove_dups_and_reset_index(cases_df)
# %% exporting a version without the additional entries
cases_df.to_csv(".\\cases_cleaned_normal.csv")


# %% Take care of unnassigned values


# %% Create value (row) per state containing the sum of all counties per date

def sum_of_counties(x):
    
    new_entry = pd.DataFrame(x.iloc[[-1]])
    
    new_entry['Admin2'] = np.nan
    new_entry['New_Confirmed'] = np.sum(x['New_Confirmed'])
    new_entry['New_Deaths'] = np.sum(x['New_Deaths'])
    new_entry['New_Recovered'] = np.sum(x['New_Recovered'])
    new_entry['Confirmed'] = 0
    new_entry['Deaths'] = 0
    new_entry['Recovered'] = 0
    new_entry['Incident_Rate'] = np.mean(x['Incident_Rate'])
    new_entry['Case_Fatality_Ratio'] = np.mean(x['Case_Fatality_Ratio'])
            
    return new_entry

filter_out_na_counties = (cases_df['Admin2'].notna())

start_time = time.time()

new_entries = cases_df.loc[filter_out_na_counties, :].groupby(['date','Province_State','Country_Region'
                                ]).apply(sum_of_counties)

print(time.time() - start_time)


# %% Appending new values to cases df

cases_df = cases_df.append(new_entries, ignore_index=True)

# %%
cases_df = remove_dups_and_reset_index(cases_df)
# %% Now doing the same, but with the sum of all states per date




def sum_of_states(x):
    
    last_index = x.tail(1).index
    
    new_entry = pd.DataFrame(x.loc[last_index,:])
    
    new_entry['Admin2'] = np.nan
    new_entry['Province_State'] = np.nan
    new_entry['New_Confirmed'] = np.sum(x['New_Confirmed'])
    new_entry['New_Deaths'] = np.sum(x['New_Deaths'])
    new_entry['New_Recovered'] = np.sum(x['New_Recovered'])
    new_entry['Confirmed'] = 0
    new_entry['Deaths'] = 0
    new_entry['Recovered'] = 0
    new_entry['Incident_Rate'] = np.mean(x['Incident_Rate'])
    new_entry['Case_Fatality_Ratio'] = np.mean(x['Case_Fatality_Ratio'])
            
    return new_entry

filter_out_non_na_counties = (cases_df['Admin2'].isna())
filter_out_na_states = (cases_df['Province_State'].notna())
all_filters = filter_out_non_na_counties & filter_out_na_states

start_time = time.time()

new_entries = cases_df.loc[all_filters, :].groupby(['date','Country_Region'
                                ]).apply(sum_of_states)

print(time.time() - start_time)

# %% Appending new values to cases df

cases_df = cases_df.append(new_entries, ignore_index=True)

# %%
cases_df = remove_dups_and_reset_index(cases_df)



# %% Now doing a cumulative sum of these newly creatied entries

def cum_sum(x):
    
        
    x['Confirmed'] = x['New_Confirmed'].cumsum() 
        
    x['Deaths'] = x['New_Deaths'].cumsum()
    
    x['Recovered'] = x['New_Recovered'].cumsum()
        
    return x
    
start_time = time.time()
cases_df = cases_df.groupby(['Province_State','Country_Region'
                              ],dropna=False).apply(cum_sum)

print(time.time() - start_time)

# %%
cases_df = remove_dups_and_reset_index(cases_df)

# %% Exporting cleaned dataframe
cases_df.to_csv(".\\cases_cleaned_categorizable.csv")



