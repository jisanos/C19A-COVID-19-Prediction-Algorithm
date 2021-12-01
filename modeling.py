# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 19:25:37 2021

Script will serve to test and model various algos.

@author: jis
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import (RandomForestRegressor,RandomForestClassifier, 
                              BaggingClassifier, AdaBoostClassifier,
                              GradientBoostingRegressor)
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.svm import SVR
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             mean_absolute_percentage_error,
                             r2_score)
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pickle
# %% Importing csv and separating between state only and country only

us_df = pd.read_csv('.\\merged_US.csv', index_col=0)

us_df['date']= us_df['date'].astype('datetime64[ns]')

state_filter = us_df['Province_State'].notna()

us_state = us_df[state_filter].copy()

us_country = us_df[np.logical_not(state_filter)].copy()

# %% Selecting only All and nan vaxx types for the moment

vax_filter = ((us_state['Vaccine_Type'] == 'All') | us_state['Vaccine_Type'].isna())

us_state_all_vax = us_state[vax_filter].copy()

vax_filter = ((us_country['Vaccine_Type'] == 'All') | us_country['Vaccine_Type'].isna())

us_country_all_vax = us_country[vax_filter].copy()

# %% Functions for plotting train predictions and test predictions
def train_plotter(name, prediction, X_train, y_train):
    fig, ax = plt.subplots(figsize=(12,5), dpi = 600)
    
    
    sns.lineplot(x = X_train.index.values, y = y_train.values, color = 'red', label='Real (Train)', ax=ax)
    sns.lineplot(x = X_train.index, y = prediction, color = 'blue', ax=ax, label = 'Fit')
        

    plt.legend()
    plt.title(name)
    plt.show()                
    
def test_plotter(name, prediction, X_test, y_test, RMSE, R2, MAPE):
    fig, ax = plt.subplots(figsize=(12,5), dpi = 600)
    
    
    sns.lineplot(x=X_test.index, y=y_test.values, color = 'red', label='Real (Test)', ax=ax)
    sns.lineplot(x=X_test.index, y=prediction, color = 'blue', ax=ax, label = 'Predicted (Fit)')
    ax.text(.7,.7,'RMSE: ' + str(RMSE), transform=ax.transAxes)
    ax.text(.7,.65,'R2 Score: ' + str(R2), transform=ax.transAxes)
    ax.text(.7,.6,'MAPE: ' + str(MAPE), transform=ax.transAxes)
  
    
    plt.ylabel('Daily Cases')
    plt.xlabel('Date (YYYY-MM)')
    plt.legend()
    plt.title(name)
    plt.show()

# %% Functions for modeling and testing various algorithms
def model_tester(model, train_df, test_df, state, title, extra_cols_drop = []):
    

    
    
    train_df = train_df.sort_values('date').set_index('date')
    test_df = test_df.sort_values('date').set_index('date')
    

    
    # Declaring default columns to drop
    cols_to_drop = ['Country_Region','Province_State','Lat','Long_','Confirmed',
                    'Deaths','Recovered', 'Active','New_Confirmed','New_Deaths',
                    'New_Recovered','Vaccine_Type','policy','word_count','date',
                    'Case_Fatality_Ratio','Incident_Rate']
    
    # Removing extra cols if any
    if len(extra_cols_drop) > 0:
        cols_to_drop.extend(extra_cols_drop)
    
    # Selecting training cols, by dropping the ones we dont need
    train_cols = np.setdiff1d(train_df.columns.values, cols_to_drop)
    
    # scaler = MinMaxScaler()
    
    # train_df[train_cols] = scaler.fit_transform(train_df[train_cols])
    # test_df[train_cols] = scaler.fit_transform(test_df[train_cols])
    
    # scaler = StandardScaler()
    # train_df[train_cols] = scaler.fit_transform(train_df[train_cols])
    # test_df[train_cols] = scaler.fit_transform(test_df[train_cols])
    
    y_train = train_df['New_Confirmed']
    X_train = train_df[train_cols]
    
    y_test = test_df['New_Confirmed']
    X_test = test_df[train_cols]
    
    # print(train_cols)
    
    
    model.fit(X_train, y_train)
    
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # y_test_pred_df = pd.DataFrame(y_test_pred)
    
    
    # # Checking if cumulative data translates to good daily data
    # new_conf_pred = y_test_pred_df[0].sub(y_test_pred_df[0].shift().fillna(0)).abs()
    
    # test_plotter(state+" "+title, new_conf_pred, y_test, test_df['New_Confirmed'])
    
    RMSE = mean_squared_error(y_test, y_test_pred, squared = False)
    RMSE = round(RMSE, 4)
    R2 = r2_score(y_test, y_test_pred)
    R2 = round(R2, 4)
    MAPE = mean_absolute_percentage_error(y_test, y_test_pred)
    MAPE = round(MAPE, 4)
    
    train_plotter(state+" "+title, y_train_pred, X_train, y_train)
    test_plotter(state+" "+title, y_test_pred,X_test, y_test, RMSE, R2, MAPE)
    
    print()
    print(state+" "+title)
    print("Metrics on whole prediction:")
    print("RMSE: ",RMSE)
    print("R2 Score: ", R2)
    print('MAPE: ',MAPE)
    
   
    
    with open('model.pkl','wb') as file:
        pickle.dump(model, file)
        
    # X_test_with_vax = X_test[X_test['Doses_admin'] > 0] # Selecting only when vaccines started to be administered
    # lenght = -(len(y_test) - 25)
    
    # print("Metrics on only part prediction:")
    # print("Root Mean Sqrt Err: ",mean_squared_error(np.array(y_test)[lenght:], y_test_pred[lenght:], squared = False))
    # print("R2 Score: ", r2_score(np.array(y_test)[lenght:], y_test_pred[lenght:]))
    
# %% 

extra = ['Doses_alloc','Doses_shipped','New_Doses_alloc','New_Doses_shipped',
                 'New_Stage_One_Doses','New_Stage_Two_Doses','Doses_admin','New_Doses_admin',
                 'Stage_One_Doses','Stage_Two_Doses',
                 
                 'Restrict/Close','Opening (State)','Deferring to County',
                 'Testing','Education','Health/Medical','Emergency Level',
                 'Transportation','Budget','Social Distancing', 'Other','Vaccine','Opening (County)']

weather_cols = ['average_temperature_celsius',
                'minimum_temperature_celsius',
                'maximum_temperature_celsius',
                'rainfall_mm','snowfall_mm',
                'dew_point','relative_humidity']

#Dropping these improve predictions by a good amount
tfidf_cols = np.setdiff1d(us_state_all_vax.columns[25:], weather_cols).tolist()



extra_cols = ['Doses_alloc','Doses_shipped','New_Doses_alloc']


state = 'California'

# %% Train test data



# Selecting the state
data = us_state_all_vax[us_state_all_vax['Province_State'] == state].copy().fillna(0)

# Only data from after 2020-04-20
# Anythinf before this date carries little weight so not worth training with
data = data[data['date'] > '2020-04-20'].copy()

# Splitting into train test
train_df,test_df = train_test_split(data, test_size=0.3, train_size=0.7)





# %% Random Forest Regressor

rfr = RandomForestRegressor(n_estimators = 1000, criterion = "squared_error",
                            max_depth = 150, min_samples_split = 2,
                            min_samples_leaf = 1, min_weight_fraction_leaf = 0.00,
                            max_features= 'auto', max_leaf_nodes= None,
                            min_impurity_decrease = 0.0, bootstrap=True,
                            oob_score = True,n_jobs=10, random_state = None,
                            verbose = 1, warm_start = False, ccp_alpha = 0.0,
                            max_samples = None)

# Criterion: absolute_error performs better BUT takes way too long to process
# thus squared_error should be used as it deliveres near similar results.
# max_depth = 150 performs best with California. But might work better as None for
# other states
# min_samples_split = 2 Default performs best
# min_samples_leaf = 1 Doesnt seem to make much of a difference
# min_weight_fraction_leaf = 0.00 hinders prediction if modified
# max_features= 'auto' leave as auto for the moment
# max_leaf_nodes= None not worth changing
# min_impurity_decrease = 0.0 not much difference
# bootstrap=True modifying will hinder predictions
# oob_score = True not sure if it made a difference
# random_state = None worsened preds
# ccp_alpha = 0.0 does not change anything

model_tester(rfr, train_df,test_df, state,"Random Forest Regressor", extra_cols )



# %% Linear Regression
lr = LinearRegression()

model_tester(lr, train_df,test_df, state,"Linear Regression")



# %% KNeighbors Regressor

knr = KNeighborsRegressor(n_neighbors = 4, weights='distance',algorithm='auto',
                          leaf_size=30, p=1)

model_tester(knr, train_df,test_df, state,"KNeighbors Regressor",extra_cols)

# Dropping extra cols improves it

# %% Ridge Regression

ridge = Ridge(alpha=1.0, random_state=241)

model_tester(ridge, train_df,test_df, state,"Ridge Regression",tfidf_cols)


# %% Gradient Boosting Regressor
gbr = GradientBoostingRegressor(loss = 'absolute_error', learning_rate = 0.1,
                                n_estimators = 500, subsample = 1.0,
                                criterion = 'squared_error',
                                min_samples_split = 10,
                                min_samples_leaf = 1, min_weight_fraction_leaf= 0,
                                max_depth=6,min_impurity_decrease = 0.0,
                                init = None, random_state = 6,
                                max_features=None, alpha = 0.9,
                                verbose = 1, max_leaf_nodes=None,
                                warm_start= False, validation_fraction= 0.1,
                                n_iter_no_change=None, ccp_alpha = 0.0)
# Best score with n estimator=30000
# Min samples split 10 gave best results
# max_depth=6 gave best results
# random_state = 6 produced best results
model_tester(gbr, train_df,test_df, state,"Gradient Boosting Regressor")

