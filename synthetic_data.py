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
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
import pickle
# %%

us_data = pd.read_csv(".\\merged_US.csv", index_col=0)

us_data = us_data[(us_data['Vaccine_Type'] == 'All') | (us_data['Vaccine_Type'].isna()) ].copy()

cols_to_keep = ['Province_State', 'Country_Region',
                'date', 'Doses_admin',
                'Stage_One_Doses','Stage_Two_Doses',
                'New_Doses_admin','New_Stage_One_Doses','New_Stage_Two_Doses',
                'average_temperature_celsius',
                'minimum_temperature_celsius',
                'maximum_temperature_celsius',
                'rainfall_mm','snowfall_mm',
                'dew_point','relative_humidity',
                'New_Confirmed']

us_data = us_data[cols_to_keep].copy()

us_data = us_data[us_data["Province_State"].notna()].copy().reset_index(drop=True)


us_data['date'] = us_data['date'].astype('datetime64[ns]')

# %%
fake = Faker('en_US')

# %%
state = 'California' #us_data['Province_State'].values
region = 'US'# us_data['Country_Region'].values

state_data = us_data[us_data.Province_State == state]

state_data = state_data.reset_index(drop=True)

latest_date = state_data.date.max().date() #datetime.date.fromisoformat(us_data.date.max())



#%%

def synthetic(num = None, seed = None):
    
    np.random.seed(seed)
    Faker.seed(seed)
    
    # final_date = latest_date + datetime.timedelta(days=num)
    
    fake_data = [
        
        {
            
            "Province_State": state,
            "Country_Region": region,
            
            # "date": fake.date_between(start_date = latest_date,
            #                           end_date = final_date),
            "date": latest_date + datetime.timedelta(days=x+1),
            # 'Doses_admin': ,
            # 'Stage_One_Doses': , these are cumulative so will be calculated later
            # 'Stage_Two_Doses': ,
            
            # 'New_Doses_admin': fake.random_int(0,1000), # Will be a sum of both stages
            
            'New_Stage_One_Doses': fake.random_int(state_data['New_Stage_One_Doses'].min(),
                                                   state_data['New_Stage_One_Doses'].std().round()),
            
            'New_Stage_Two_Doses': fake.random_int(state_data['New_Stage_Two_Doses'].min(),
                                                   state_data['New_Stage_Two_Doses'].std().round()),        
            # "average_temperature_celsius": fake.random_int(-5,5), # Will be the mean of min and max
            'minimum_temperature_celsius':random.uniform(state_data['minimum_temperature_celsius'].min(),
                                                          state_data['minimum_temperature_celsius'].max()),
            
            'maximum_temperature_celsius':random.uniform(state_data['maximum_temperature_celsius'].min(),
                                                          state_data['maximum_temperature_celsius'].max()),
            
            'rainfall_mm':random.uniform(state_data['rainfall_mm'].min(),
                                          state_data['rainfall_mm'].max()),
            
            'snowfall_mm':random.uniform(state_data['snowfall_mm'].min(),
                                          state_data['snowfall_mm'].max()),
            
            'dew_point':random.uniform(state_data['dew_point'].min(),
                                        state_data['dew_point'].max()),
            
            'relative_humidity':random.uniform(state_data['relative_humidity'].min(),
                                                state_data['relative_humidity'].max()),
            
        }
        
        for x in range(num)
        
        ]
    
    fake_data_df = pd.DataFrame(fake_data)
    
    fake_data_df['New_Doses_admin'] = fake_data_df.New_Stage_One_Doses \
        + fake_data_df.New_Stage_Two_Doses
    
    fake_data_df["average_temperature_celsius"] = fake_data_df[
        ['minimum_temperature_celsius','maximum_temperature_celsius']].mean(axis=1)
    
    fake_data_df[['Doses_admin','Stage_One_Doses','Stage_Two_Doses']] = 0
    
    last_row = state_data[state_data['date'] == state_data['date'].max()]
    
    
    
    fake_data_df['date'] = fake_data_df['date'].astype('datetime64[ns]')
    
    fake_data_df = fake_data_df.sort_values('date')
    
    fake_data_df[['Doses_admin','Stage_One_Doses','Stage_Two_Doses'
                  ]] = fake_data_df[['New_Doses_admin','New_Stage_One_Doses',
                                     'New_Stage_Two_Doses']].cumsum()
          
    # Adding the previous to cumulative data fro consistency
    fake_data_df[['Doses_admin','Stage_One_Doses','Stage_Two_Doses']] \
        +=  last_row[['Doses_admin','Stage_One_Doses','Stage_Two_Doses']].values
        
        
    # Calculating the 7 day moving average to smooth out the data
    fake_data_df["average_temperature_celsius"] = fake_data_df[
        "average_temperature_celsius"].rolling(window=7).mean()
                                     
    return fake_data_df

# %%
synthetic_df = synthetic(num = 90, seed = 0)


# %% Plotting synthetic data against real data to see if patterns are similar

for col in cols_to_keep:

    fig = plt.figure(dpi=600)
    sns.lineplot(data = state_data, x='date',y=col)
    
    sns.lineplot(data = synthetic_df, x='date',y=col)
    plt.show()

# %% plotting both continuously 
# to_plot = pd.concat([state_data,synthetic_df]).drop_duplicates('date').reset_index(drop=True)
# fig = plt.figure(dpi=600)
# sns.lineplot(data =to_plot , x='date',y='average_temperature_celsius')
# plt.show()

# %% 
X_test = synthetic_df.set_index('date')
X_test = X_test.drop(['Province_State', 'Country_Region'], axis=1)

X_test = X_test[['Doses_admin', 'New_Doses_admin', 'New_Stage_One_Doses',
             'New_Stage_Two_Doses', 'Stage_One_Doses', 'Stage_Two_Doses',
             'average_temperature_celsius', 'dew_point', 'maximum_temperature_celsius',
             'minimum_temperature_celsius', 'rainfall_mm', 'relative_humidity',
             'snowfall_mm']]
# %%
with open('model.pkl','rb') as file:
    model= pickle.load(file)
    
# %%
X_test = X_test.fillna(0)
Y_pred = model.predict(X_test)


# %% 

fig = plt.figure(dpi=600)

sns.lineplot(x=state_data.date, y=state_data.New_Confirmed)

sns.lineplot(x=X_test.index, y=Y_pred)
plt.show()