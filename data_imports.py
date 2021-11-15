# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 15:03:56 2021

This package will serve as a station for all dataset imports. This way if
a path needs to be changed it can be done directly here and not on every
other script.

Will also contain other global variables

@author: jis
"""
import pandas as pd
import glob

extension = 'csv'

def csse_covid_19_daily_reports():
    
    path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
    allFilesInFolder = [
        i for i in glob.glob((path + '*.{}').format(extension))]
    
    return pd.concat(
        [pd.read_csv(file).assign(
            date = file.replace(path,"").replace(
                ".csv","")) for file in allFilesInFolder],ignore_index = True)


def csse_covid_19_daily_reports_us():
    path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports_us\\"
    allFilesInFolder = [i for i in glob.glob((path + '*.{}').format(extension))]
    
    return pd.concat(
        [pd.read_csv(file).assign(
            date = file.replace(path,"").replace(
                ".csv","")) for file in allFilesInFolder],ignore_index = True)


def policy_data_current():
    policies_path = ".\\CCI_C-19_Policies\\data_tables\\policy_data\\"\
        "table_data\\Current\\"
    policies_files = glob.glob(policies_path + "*.csv")

    content = []  # store contents from files

    for filepath in policies_files:

        df = pd.read_csv(filepath, index_col=None)
        # Stripping the string to store the name of the file to a State column
        # State column should be the second column
        df.insert(1, "State", filepath.replace(
            policies_path, "").replace("_policy.csv", ""))
        content.append(df)


    return pd.concat(content)


def world_pop_by_country():
    path = ".\\CCI_C-19\\data_tables\\world_pop_by_country.csv"
    return pd.read_csv(path)


# Dictionary of appreviated us states
us_states_abbreviations = {
    'Alaska': 'AK',
    'Alabama': 'AL', 'Arkansas': 'AR',
    'American Samoa': 'AS', 
    'Arizona': 'AZ', 'Colorado': 'CO',
    'Connecticut': 'CT',
    'District of Columbia': 'DC', 
    'Delaware': 'DE', 'Florida': 'FL','Georgia': 'GA',
    'Guam': 'GU', 'Hawaii': 'HI', 'Iowa': 'IA', 
    'Idaho': 'ID', 'Illinois': 'IL','Indiana': 'IN', 
    'Kentucky': 'KY', 'Louisiana': 'LA',
    'Massachusetts': 'MA', 'Maryland': 'MD', 
    'Maine': 'ME', 'Michigan': 'MI','Minnesota': 'MN',
    'Missouri': 'MO', 'Northern Mariana Islands': 'MP', 
    'Mississippi': 'MS', 'Montana': 'MT',
    'North Carolina': 'NC', 'North Dakota': 'ND',
    'Nebraska': 'NE', 
    'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'Nevada': 'NV', 'New York': 'NY', 
    'Ohio': 'OH', 'Oklahoma': 'OK','Oregon': 'OR',
    'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 
    'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 
    'Texas': 'TX', 'Utah': 'UT', 'Virginia': 'VA',
    'Virgin Islands': 'VI', 
    'Vermont': 'VT', 'Washington': 'WA',
    'Wisconsin': 'WI', 'West Virginia': 'WV', 
    'Wyoming': 'WY', 'California': 'CA', 'Kansas':'KS'}

# Inverse dictonary from us_states_abbreviations
abbreviations_to_us_states = {}
for val,key in us_states_abbreviations.items():
    abbreviations_to_us_states[key] = val
