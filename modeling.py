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
from sklearn.svm import SVC
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             mean_absolute_percentage_error)
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis



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
    fig, ax = plt.subplots(figsize=(18,8))
    
    
    sns.lineplot(x = X_train.index.values, y = y_train.values, color = 'red', label='Real (Train)', ax=ax)
    sns.lineplot(x = X_train.index, y = prediction, color = 'blue', ax=ax, label = 'Fit')
        

    plt.legend()
    plt.title(name)
    plt.show()                
    
def test_plotter(name, prediction, X_test, y_test):
    fig, ax = plt.subplots(figsize=(18,8))
    
    
    sns.lineplot(x=X_test.index, y=y_test.values, color = 'red', label='Real (Test)', ax=ax)
    sns.lineplot(x=X_test.index, y=prediction, color = 'blue', ax=ax, label = 'Predicted (Fit)')
    
  
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
    
    y_train = train_df['New_Confirmed']
    X_train = train_df[train_cols]
    
    y_test = test_df['New_Confirmed']
    X_test = test_df[train_cols]
    
    model.fit(X_train, y_train)
    
    
    
    train_plotter(state+" "+title, model.predict(X_train), X_train, y_train)
    
    test_plotter(state+" "+title, model.predict(X_test),X_test, y_test)
    print()
    print(state+" "+title)
    print("Metrics on whole prediction:")
    print("Root Mean Sqrt Err: ",mean_squared_error(y_test, model.predict(X_test), squared = False))
    #print("Mean Abs Err",mean_absolute_error(y_test, model.predict(X_test)))
    #print("Mean Abs % Err", mean_absolute_percentage_error(y_test, model.predict(X_test)))
    
    lenght = len(y_test)
    half = int(round(lenght / 2)) + 20
    print("Metrics on only half prediction (2021 - ...):")
    print("Root Mean Sqrt Err: ",mean_squared_error(np.array(y_test)[half:], model.predict(X_test)[half:], squared = False))
    #print("Mean Abs Err",mean_absolute_error(y_test[half:], model.predict(X_test)[half:]))
    #print("Mean Abs % Err", mean_absolute_percentage_error(y_test[half:], model.predict(X_test)[half:]))

# %% 

extra = ['Doses_alloc','Doses_shipped','New_Doses_alloc','New_Doses_shipped',
                 'New_Stage_One_Doses','New_Stage_Two_Doses','Doses_admin','New_Doses_admin',
                 'Stage_One_Doses','Stage_Two_Doses',
                 
                 'Restrict/Close','Opening (State)','Deferring to County',
                 'Testing','Education','Health/Medical','Emergency Level',
                 'Transportation','Budget','Social Distancing', 'Other','Vaccine','Opening (County)']

tfidf_cols = us_state_all_vax.columns[25:]

state = 'New York'

# %% Train test data



# Selecting the state
data = us_state_all_vax[us_state_all_vax['Province_State'] == state].copy().fillna(0)
# Splitting into train test
train_df,test_df = train_test_split(data, test_size=0.3, train_size=0.7)

# %% Random Forest Regressor

rfr = RandomForestRegressor(n_estimators = 1000)

model_tester(rfr, train_df,test_df, state,"Random Forest Regressor",tfidf_cols)



# %% Linear Regression
lr = LinearRegression()

model_tester(lr, train_df,test_df, state,"Linear Regression",tfidf_cols)

# %% Decision Tree Classifier

dtc = DecisionTreeClassifier()

model_tester(dtc, train_df,test_df, state,"Decision Tree Classifier",tfidf_cols)

# This one has a small tendency to improve with the TFIDF columns

# %% Support vector machine
svc = SVC()

model_tester(svc, train_df,test_df, state,"Support Vector Machine",tfidf_cols)



# %% Random Forest Classifier

# rfc = RandomForestClassifier(max_depth = 2)

# model_tester(rfc, train_df,test_df, state,"Random Forest Classifier")

# %% KNeighbors Regressor

# knr = KNeighborsRegressor(n_neighbors = 8)

# model_tester(knr, train_df,test_df, state,"KNeighbors Regressor",tfidf_cols)

# %% Ridge Regression

ridge = Ridge(alpha=1.0, random_state=241)

model_tester(ridge, train_df,test_df, state,"Ridge Regression",tfidf_cols)
# %% Naive Bayes GaussianNB

gnb = GaussianNB()

model_tester(gnb, train_df,test_df, state,"Naive Bayes GaussianNB",tfidf_cols)

# %% Extra Tree Classifier

etc = ExtraTreeClassifier()

model_tester(etc, train_df,test_df, state,"Extra Tree Classifier",tfidf_cols)
# %% Bagging Classifier

# bc = BaggingClassifier()

# model_tester(bc, train_df,test_df, state,"Bagging Classifier")
# %% Ada Boost Classifier

# abc = AdaBoostClassifier()

# model_tester(abc, train_df,test_df, state,"Ada Boost Classifier")

# %% Gradient Boosting Regressor
gbr = GradientBoostingRegressor()

model_tester(gbr, train_df,test_df, state,"Gradient Boosting Regressor",tfidf_cols)

