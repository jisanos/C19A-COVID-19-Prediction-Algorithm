# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#adding libraries needed
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns

#set the plot's theme to something more beautiful
sns.set()
# %%
#extracting all files from local directory for csse are merging them
extension = 'csv'
path = ".\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
allFilesInFolder = [i for i in glob.glob((path + '*.{}').format(extension))]

csse_covid_19_daily_reports = pd.concat([pd.read_csv(file).assign(date = file.replace(
    path,"").replace(".csv","")) for file in allFilesInFolder],
    ignore_index = True)


# %%

# Changing date to datetime
csse_covid_19_daily_reports['date'] = csse_covid_19_daily_reports['date'].astype(
    'datetime64[ns]') #MM-DD-YYYY


# %%
print(csse_covid_19_daily_reports)
csse_covid_19_daily_reports.info()


# %%
#comparing the merged dataset csse with the dataset CCI to check the
# differences between them 
time_series_covid19_US = pd.read_csv(
    ".\\CCI_C-19\\data_tables\\testing_data\\time_series_covid19_US.csv")
print(time_series_covid19_US)
print(csse_covid_19_daily_reports)

# %%

# Checking what columns they have in common

print([element for element in list(csse_covid_19_daily_reports.columns) if element in 
       list(time_series_covid19_US.columns)])

# They only have the 'date' column in common. There are others that might be
# related but are not named equally.

# %%

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

# %%
# Renaming the abbreviated values in state column for easier comparing between
# the two datasets

time_series_covid19_US['state'].replace(abbreviations_to_us_states, inplace = True)

# %%

# Renaming 

# %%

# Comparing their csse_covid_19_daily_reports 'Confirmed' column with the time_series_covid19_US
# 'cases_conf_probable

#print(time_series_covid19_US.set_index('state').join(csse_covid_19_daily_reports.set_index('Province_State')))


# %%
#there's currently a duplicate of columns in this dataset so we're going to remove the one with the most nans which has little to no data
print('The amount of missing data on Province_State column of CSSE is:', csse_covid_19_daily_reports['Province_State'].isnull().sum())
print('The amount of missing data on Province/State column of CSSE is:', csse_covid_19_daily_reports['Province/State'].isnull().sum())
print("")
print('The amount of missing data on Country_Region column of CSSE is:', csse_covid_19_daily_reports['Country_Region'].isnull().sum())
print('The amount of missing data on Country/Region column of CSSE is:', csse_covid_19_daily_reports['Country/Region'].isnull().sum())
print("")
print('The amount of missing data on Last_Update column of CSSE is:', csse_covid_19_daily_reports['Last_Update'].isnull().sum())
print('The amount of missing data on Last Update column of CSSE is:', csse_covid_19_daily_reports['Last Update'].isnull().sum())
print("")
print('The amount of missing data on Latitude column of CSSE is:', csse_covid_19_daily_reports['Latitude'].isnull().sum())
print('The amount of missing data on Lat column of CSSE is:', csse_covid_19_daily_reports['Lat'].isnull().sum())
print("")
print('The amount of missing data on Longitude column of CSSE is:', csse_covid_19_daily_reports['Longitude'].isnull().sum())
print('The amount of missing data on Long_ column of CSSE is:', csse_covid_19_daily_reports['Long_'].isnull().sum())
print("")
print('The amount of missing data on Incident_Rate column of CSSE is:', csse_covid_19_daily_reports['Incident_Rate'].isnull().sum())
print('The amount of missing data on Incidence_Rate column of CSSE is:', csse_covid_19_daily_reports['Incidence_Rate'].isnull().sum())
print("")
print('The amount of missing data on Case_Fatality_Ratio column of CSSE is:', csse_covid_19_daily_reports['Case_Fatality_Ratio'].isnull().sum())
print('The amount of missing data on Case-Fatality_Ratio column of CSSE is:', csse_covid_19_daily_reports['Case-Fatality_Ratio'].isnull().sum())


# %%
#drop the duplicate columns that have the most nans 
csse_covid_19_daily_reports.drop(['Province/State', 'Country/Region','Last Update', 'Latitude','Longitude','Incidence_Rate','Case-Fatality_Ratio'], axis=1, inplace=True)


# %%
#show CSSE dataset with the changes
print(csse_covid_19_daily_reports)

# %%
#checking all the province states of the dataset to see if there's any bad data
print(csse_covid_19_daily_reports[['Province_State','Recovered']].groupby('Province_State').sum().index.values)
group_CSSE = csse_covid_19_daily_reports[['Province_State','Recovered']]
print(group_CSSE[group_CSSE['Province_State'] == 'Unknown'])
print(group_CSSE[group_CSSE['Province_State'] == 'Recovered'])

# %%
#Removing that unkown and recovered rows which are invalid data in our dataset and then checking to see if it's gone with our coding
csse_covid_19_daily_reports.drop(csse_covid_19_daily_reports.index[csse_covid_19_daily_reports['Province_State'] == 'Unknown'], inplace = True)
csse_covid_19_daily_reports.drop(csse_covid_19_daily_reports.index[csse_covid_19_daily_reports['Province_State'] == 'Recovered'], inplace = True)
print(csse_covid_19_daily_reports[['Province_State','Recovered']].groupby('Province_State').sum().index.values)
print(group_CSSE[group_CSSE['Province_State'] == 'Unknown'])
print(group_CSSE[group_CSSE['Province_State'] == 'Recovered'])
# %%
group_CSSE = csse_covid_19_daily_reports[['Province_State','Deaths']].groupby('Province_State').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Deaths',color='red',title = 'States with more deaths',rot=0)
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more deaths')
plt.show()
print(group_CSSE.head(5))
#print(group_CSSE.sort_values("Deaths",ascending=False))
# %%
group_CSSE = csse_covid_19_daily_reports[['Province_State','Confirmed']].groupby('Province_State').sum().reset_index().sort_values("Confirmed",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Confirmed',color='red',title = 'States with more confirmed',rot=0)
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()
print(group_CSSE.head(5))

# %%
group_CSSE = csse_covid_19_daily_reports[['Province_State','Recovered']].groupby('Province_State').sum().reset_index().sort_values("Recovered",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Recovered',color='red',title = 'States with more Recovered',rot=0)
sns.barplot(x='Province_State', y='Recovered', data = group_CSSE.head(5)).set_title('States with more recovered')
plt.show()
print(group_CSSE.head(5))

# %%
group_CSSE = csse_covid_19_daily_reports[['Country_Region','Deaths']].groupby('Country_Region').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Country_Region',y='Deaths',color='red',title = 'Regions with more deaths',rot=0)
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()
print(group_CSSE.head(5))

# %%
#group_CSSE = csse_covid_19_daily_reports[['Country_Region','Case_Fatality_Ratio']].groupby('Country_Region').sum()
#sns.scatterplot(x='Confirmed', y='Deaths', data = group_CSSE.head(5), hue="Country_Region", palette="viridis", edgecolors="black", alpha=0.5, sizes=(10, 1000)).set_title('Regions with more deaths')
#plt.show()

# %%
#checking if any of the data frames if theres any similarities in the states columns of both datasets
#combinedOfCsv['Province_State'].isin(time_series_covid19_US['state'])
print(csse_covid_19_daily_reports[csse_covid_19_daily_reports['Province_State'].isin(time_series_covid19_US['state'].values)])

# %%
#merging both datasets and dropping duplicates to see any differences
df_diff = pd.concat([csse_covid_19_daily_reports,time_series_covid19_US]).drop_duplicates(keep=False)


# %%
print(df_diff)


# %%
#Checking each state from this datasets and checking that the states are from US
#statesCCI = time_series_covid19_US['state'].drop_duplicates()
#statesCCI_array = statesCCI.tolist()
#print(sorted(statesCCI_array))


# %%
#Checking each state from this datasets and checking that the states are worldwide
#statesCSSE = combinedOfCsv['Province_State'].drop_duplicates()
#statesCSSE.tolist()



# %%
#now we're going to try to rename the names of some states of the us in acronym version so that the two datasets have a similarity 
csse_covid_19_daily_reports['Province_State'].replace(us_states_abbreviations, inplace = True)


# %%
#Checking to see that the acronym of the us states are working
#statesCSSE = combinedOfCsv['Province_State']
#statesCSSE.tolist()

# %%
#Now checking the similarities of the dates of the two datasets 
similarities_of_CSSE_and_CCI = csse_covid_19_daily_reports[csse_covid_19_daily_reports['Province_State'].isin(time_series_covid19_US['state'].values)]
print(similarities_of_CSSE_and_CCI)
# %%

