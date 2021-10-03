# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import os
import glob

#seals and seals
# %%
#extracting all files from local directory for csse are merging them
extension = 'csv'
path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
allFilesInFolder = [i for i in glob.glob((path + '*.{}').format(extension))]

#test seals
# %%
print("The csv files ending with .csv are: ", allFilesInFolder)


# %%
combinedOfCsv = pd.concat([pd.read_csv(file).assign(date = file.replace(path,"").replace(".csv","")) for file in allFilesInFolder],ignore_index = True)


# %%
combinedOfCsv


# %%
combinedOfCsv['date'] = combinedOfCsv['date'].astype('datetime64[ns]') #MM-DD-YYYY


# %%
display(combinedOfCsv)
combinedOfCsv.info()


# %%
#comparing the merged dataset csse with the dataset CCI to check the differences between them 
datasetCCI = pd.read_csv(".\\CCI_C-19\\data_tables\\testing_data\\time_series_covid19_US.csv")
display(datasetCCI)
display(combinedOfCsv)


# %%
#there's currently a duplicate of columns in this dataset so we're going to remove the one with the most nans which has little to no data
print('The amount of missing data on Province_State column of CSSE is:', combinedOfCsv['Province_State'].isnull().sum())
print('The amount of missing data on Province/State column of CSSE is:', combinedOfCsv['Province/State'].isnull().sum())
print("")
print('The amount of missing data on Country_Region column of CSSE is:', combinedOfCsv['Country_Region'].isnull().sum())
print('The amount of missing data on Country/Region column of CSSE is:', combinedOfCsv['Country/Region'].isnull().sum())
print("")
print('The amount of missing data on Last_Update column of CSSE is:', combinedOfCsv['Last_Update'].isnull().sum())
print('The amount of missing data on Last Update column of CSSE is:', combinedOfCsv['Last Update'].isnull().sum())
print("")
print('The amount of missing data on Latitude column of CSSE is:', combinedOfCsv['Latitude'].isnull().sum())
print('The amount of missing data on Lat column of CSSE is:', combinedOfCsv['Lat'].isnull().sum())
print("")
print('The amount of missing data on Longitude column of CSSE is:', combinedOfCsv['Longitude'].isnull().sum())
print('The amount of missing data on Long_ column of CSSE is:', combinedOfCsv['Long_'].isnull().sum())
print("")
print('The amount of missing data on Incident_Rate column of CSSE is:', combinedOfCsv['Incident_Rate'].isnull().sum())
print('The amount of missing data on Incidence_Rate column of CSSE is:', combinedOfCsv['Incidence_Rate'].isnull().sum())
print("")
print('The amount of missing data on Case_Fatality_Ratio column of CSSE is:', combinedOfCsv['Case_Fatality_Ratio'].isnull().sum())
print('The amount of missing data on Case-Fatality_Ratio column of CSSE is:', combinedOfCsv['Case-Fatality_Ratio'].isnull().sum())


# %%
#drop the duplicate columns that have the most nans 
combinedOfCsv.drop(['Province/State', 'Country/Region','Last Update', 'Latitude','Longitude','Incidence_Rate','Case-Fatality_Ratio'], axis=1, inplace=True)


# %%
#show CSSE dataset without the changes
combinedOfCsv


# %%
#df['n'].replace({'a': 'x', 'b': 'y', 'c': 'w', 'd': 'z'})
#df['col_name'] = df['col_name'].str.replace('G', '1')


# %%
#checking if any of the data frames if theres any similarities in the states columns of both datasets
#combinedOfCsv['Province_State'].isin(datasetCCI['state'])
combinedOfCsv[combinedOfCsv['Province_State'].isin(datasetCCI['state'].values)]


# %%
#merging both datasets and dropping duplicates to see any differences
df_diff = pd.concat([combinedOfCsv,datasetCCI]).drop_duplicates(keep=False)


# %%
display(df_diff)


# %%
#Checking each state from this datasets and checking that the states are from US
#statesCCI = datasetCCI['state'].drop_duplicates()
#statesCCI_array = statesCCI.tolist()
#print(sorted(statesCCI_array))


# %%
#Checking each state from this datasets and checking that the states are worldwide
#statesCSSE = combinedOfCsv['Province_State'].drop_duplicates()
#statesCSSE.tolist()


# %%
#now we're going to try to rename the names of some states of the us in acronym version so that the two datasets have a similarity 
combinedOfCsv['Province_State'].replace({'Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'American Samoa': 'AS', 
                                                     'Arizona': 'AZ', 'Colorado': 'CO', 'Connecticut': 'CT', 'District of Columbia': 'DC', 
                                                     'Delaware': 'DE', 'Florida': 'FL','Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Iowa': 'IA', 
                                                     'Idaho': 'ID', 'Illinois': 'IL','Indiana': 'IN', 
                                                     'Kentucky': 'KY', 'Louisiana': 'LA', 'Massachusetts': 'MA', 'Maryland': 'MD', 
                                                     'Maine': 'ME', 'Michigan': 'MI','Minnesota': 'MN', 'Missouri': 'MO', 'Northern Mariana Islands': 'MP', 
                                                     'Mississippi': 'MS', 'Montana': 'MT','North Carolina': 'NC', 'North Dakota': 'ND', 'Nebraska': 'NE', 
                                                     'New Hampshire': 'NH', 'New Jersey': 'NJ','New Mexico': 'NM', 'Nevada': 'NV', 'New York': 'NY', 
                                                     'Ohio': 'OH', 'Oklahoma': 'OK','Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 
                                                     'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 
                                                     'Texas': 'TX', 'Utah': 'UT', 'Virginia': 'VA', 'Virgin Islands': 'VI', 
                                                     'Vermont': 'VT', 'Washington': 'WA', 'Wisconsin': 'WI', 'West Virginia': 'WV', 
                                                     'Wyoming': 'WY', 'California': 'CA', 'Kansas':'KS'}, inplace = True)


# %%
#Checking to see that the acronym of the us states are working
#statesCSSE = combinedOfCsv['Province_State']
#statesCSSE.tolist()


# %%
combinedOfCsv[combinedOfCsv['Province_State'].isin(datasetCCI['state'].values)]


# %%



