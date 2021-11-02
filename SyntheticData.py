# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:16:12 2021

@author: rayni
"""
# %%
#adding libraries needed
import pandas as pd
from faker import Faker
import numpy as np
import random
# %%
file = ".\\cases_cleaned_categorizable.csv"
cases_cleaned = pd.read_csv(file)

# %%

us_Data_Only = cases_cleaned[cases_cleaned["Country_Region"] == "US"].head(50)

# %%
fake = Faker('en_US')

# %%
usPState = us_Data_Only['Province_State'].values
usRegion = us_Data_Only['Country_Region'].values

#%%

def synthetic(num = None, seed = None):
    
    np.random.seed(seed)
    Faker.seed(seed)
    
    fake_data = [
        
        {
            #"Country_Region": fake.country(),
            #"Province_State": fake.state(),
            "Province_State": random.choice(usPState),
            "Country_Region": random.choice(usRegion),
            "Confirmed": np.random.randint(30),
            "Deaths": np.random.randint(23),
            
            }
        
        for x in range(num)
        
        ]
    
    return fake_data

# %%
syntheticDataFrame = pd.DataFrame(synthetic(num = 50, seed = 0))


