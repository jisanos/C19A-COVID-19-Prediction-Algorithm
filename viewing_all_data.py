# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:33:53 2021

@author: jis
"""
# %%
# Libs
import pandas as pd
import glob

extension = 'csv'
# %%
# CSSE (Johns Hopkins Center for Systems Science and Engineering)


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


# %%
# CCI (Johns Hopkins Centers for Civic Impact)


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

# %% Cleaning Variable Explorer
del path
del df
del extension
del filepath
del allFilesInFolder
del content
del policies_files



