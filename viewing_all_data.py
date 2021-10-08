# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:33:53 2021

Script will serve as a framework of imports of the most prevalent
the data within the JHUCSSE and JHUCCI repositories. Will also work as a way
to visualize the raw data easier within the variable explorer and do some basic
analysis within the IPython console.

@author: jis
"""
# %%
# Libs
import pandas as pd
import glob

extension = 'csv'
# %%
# CSSE (Johns Hopkins Center for Systems Science and Engineering)

################## csse_covid_19_daily_reports
# CSSE_C-19\csse_covid_19_data\README.md
# 
# This one contains CUMMULATIVE daily case reports GLOBALLY.
#
# Also contains US and each of its states.
#
# Updated daily.
# 
# Confirmed values here are cummulative.
# 
path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
allFilesInFolder = [i for i in glob.glob((path + '*.{}').format(extension))]

csse_covid_19_daily_reports = pd.concat(
    [pd.read_csv(file).assign(
        date = file.replace(path,"").replace(
            ".csv","")) for file in allFilesInFolder],ignore_index = True)



################## csse_covid_19_daily_reports_us
# Same as previous, but this one contains only US states and
# some columns that might differ
# 
# is cumulative
path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports_us\\"
allFilesInFolder = [i for i in glob.glob((path + '*.{}').format(extension))]

csse_covid_19_daily_reports_us = pd.concat(
    [pd.read_csv(file).assign(
        date = file.replace(path,"").replace(
            ".csv","")) for file in allFilesInFolder],ignore_index = True)

################### time_series_covid19
# CSSE_C-19\csse_covid_19_data\csse_covid_19_time_series\README.md
# 
# Contains daily time series summary tables of confirmed cases, deaths and
# recovered. Updated daily.
#
# Values are CUMULATIVE
#
path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_time_series\\"
# US only
# 
# Contains US States separately as well as County
time_series_covid19_deaths_US = pd.read_csv(
    path + "time_series_covid19_deaths_US.csv")
time_series_covid19_confirmed_US = pd.read_csv(
    path + "time_series_covid19_confirmed_US.csv")

# Global
#
# Do not contain US states separately. Not all countries contain states either.
time_series_covid19_confirmed_global = pd.read_csv(
    path+ "time_series_covid19_confirmed_global.csv")
time_series_covid19_deaths_global = pd.read_csv(
    path + "time_series_covid19_deaths_global.csv")
time_series_covid19_recovered_global = pd.read_csv(
    path + "time_series_covid19_recovered_global.csv")


################### who_covid_19_sit_rep_time_series
# This one is a summary of confirmed cases from world health organization
# from the covid 19 situation reports. These are "Lab confirmed" cases.
# it should work as complement to csse_covid_19_daily_reports.
#
# Contains Global data 
#
# This was last updated on Aug 18, 2020.
#
# The last signigicant amount of data was on March 15, 2020.
# 
# Is cummulative
#
# Does not contain enough significant data so it could be ignored.
# 
path = ".\\CSSE_C-19\\who_covid_19_situation_reports\\"\
    "who_covid_19_sit_rep_time_series\\who_covid_19_sit_rep_time_series.csv"
who_covid_19_sit_rep_time_series = pd.read_csv(path)


# %%
# CCI (Johns Hopkins Centers for Civic Impact)

################# time_series_covid19_US
# CCI_C-19\data_tables\testing_data\readme.md
# CCI_C-19\data_tables\testing_data\data_dictionary.csv
#
# This mainly focuses on the number of confirmed and probable cases in the US
# it has columns cummulative totals of confirmed and
# probable cases.
#
# Values here are cummulative.
#
path = ".\\CCI_C-19\\data_tables\\testing_data\\time_series_covid19_US.csv"
time_series_covid19_US = pd.read_csv(path)



################## policy_data_current
# CCI_C-19_Policies\data_tables\policy_data\README.txt
#
# Contains policies stated by their date and their respective state. US only.
# Updated daily (If new policies are stated)
path = ".\\CCI_C-19_Policies\\data_tables\\policy_data\\table_data\\Current\\"
policies_files = glob.glob(path + "*.csv")

content = []  # store contents from files

for filepath in policies_files:

    df = pd.read_csv(filepath, index_col=None)
    # Stripping the string to store the name of the file to a State column
    # State column should be the second column
    df.insert(1, "State", filepath.replace(
        path, "").replace("_policy.csv", ""))
    content.append(df)


policy_data_current = pd.concat(content,ignore_index=True)

#################### demographics_by_state_standardized
# CCI_C-19\data_tables\demographic_data\README.md
# CCI_C-19\data_tables\demographic_data\COVID19_demographics_standardized_data_dictionary.md
# 
# Demographic data of various states in US
# 
# Reported twice a month starting April 2021 (semi monthly)
path = ".\\CCI_C-19\\data_tables\\demographic_data\\"\
    "demographics_by_state_standardized.csv"
demographics_by_state_standardized = pd.read_csv(path)

################# world_pop_by_country
# Contains countries with their respective populations, as of 2018 (currently)
#
#
#
#
path = ".\\CCI_C-19\\data_tables\\world_pop_by_country.csv"
world_pop_by_country=pd.read_csv(path)

################# vaccine_data global_data
# 
# 
#
# CCI_C-19\data_tables\vaccine_data\global_data\readme.md
# CCI_C-19\data_tables\vaccine_data\global_data\data_dictionary.csv
#
#

# vaccine_data_global and time_series_covid19_vaccine_global contain the same
# columns.

# This is a vertical time series (Long format)
# Contains all historical data
#
# This is the one that should be used.
#
path = ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\"\
    "time_series_covid19_vaccine_global.csv"
time_series_covid19_vaccine_global = pd.read_csv(path)

# This is a vertical (Long format)
# Only contains recent data (current day data)
#
#
path = ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\"\
    "vaccine_data_global.csv"
vaccine_data_global = pd.read_csv(path)

# This is a horizontal time series (Wide format)
path = ".\\CCI_C-19\\data_tables\\vaccine_data\\global_data\\"\
    "time_series_covid19_vaccine_doses_admin_global.csv"
time_series_covid19_vaccine_doses_admin_global = pd.read_csv(path)



################# vaccine_data us_data
# CCI_C-19\data_tables\vaccine_data\us_data\readme.md
# CCI_C-19\data_tables\vaccine_data\us_data\data_dictionary.csv
#
#
#
#
#

# vertical time series (long format) containing historical data
# this one only contains total vaccinations (not by vaccine type)
people_vaccinated_us_timeline = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\"\
        "people_vaccinated_us_timeline.csv")


# vertical time series (long format) containing historical data
# This one contains more specific data such as vaccine type, soses shipped,
# and other
#
# This is the one that should be used
vaccine_data_us_timeline = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\"\
        "vaccine_data_us_timeline.csv")


# This is horizontal time series (wide format)
path = ".\\CCI_C-19\\data_tables\\vaccine_data\\us_data\\time_series\\"\
            "time_series_covid19_vaccine_doses_admin_US.csv"
time_series_covid19_vaccine_doses_admin_US = pd.read_csv(path)

# %% Cleaning Variable Explorer
del path
del df
del extension
del filepath
del allFilesInFolder
del content
del policies_files



