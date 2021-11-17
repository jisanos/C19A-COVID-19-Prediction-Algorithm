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

us_data = pd.read_csv(".\\merged_US.csv")


# %%
fake = Faker('en_US')

# %%
states = us_data['Province_State'].values
region = us_data['Country_Region'].values

latest_date = us_data.date.max()

#%%

def synthetic(num = None, seed = None):
    
    np.random.seed(seed)
    Faker.seed(seed)
    
    fake_data = [
        
        {
            
            "Province_State": random.choice(states),
            "Country_Region": random.choice(region),
            "New_Confirmed": np.random.randint(30),
            "New_Deaths": np.random.randint(23),
            "date": fake.date_between(start_date=str(latest_date),end_date="2021-12-15")
            }
        
        for x in range(num)
        
        ]
    
    return fake_data

# %%
syntheticDataFrame = pd.DataFrame(synthetic(num = 50, seed = 0))




