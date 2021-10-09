# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 15:03:56 2021

This package will serve as a station for all dataset imports. This way if
a path needs to be changed it can be done directly here and not on every
other script.

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