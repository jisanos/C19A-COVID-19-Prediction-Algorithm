# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:50:09 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
#set the plot's theme to something more beautiful
sns.set()

# %%
merged_US = pd.read_csv(".\\merged_US.csv")
merged_global = pd.read_csv(".\\merged_global.csv")
#vax_cleaned_categorizable_Without_Date_Filter = pd.read_csv(".\\vax_cleaned_categorizable.csv")

# %%
