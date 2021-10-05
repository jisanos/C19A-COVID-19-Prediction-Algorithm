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

# %%
print("The csv files ending with .csv are: ", allFilesInFolder)


# %%
combinedOfCsvCSSE = pd.concat([pd.read_csv(file).assign(date = file.replace(path,"").replace(".csv","")) for file in allFilesInFolder],ignore_index = True)


# %%
print(combinedOfCsvCSSE)


# %%
combinedOfCsvCSSE['date'] = combinedOfCsvCSSE['date'].astype('datetime64[ns]') #MM-DD-YYYY


# %%
print(combinedOfCsvCSSE)
combinedOfCsvCSSE.info()


# %%
#comparing the merged dataset csse with the dataset CCI to check the differences between them 
datasetCCI = pd.read_csv(".\\CCI_C-19\\data_tables\\testing_data\\time_series_covid19_US.csv")
print(datasetCCI)
print(combinedOfCsvCSSE)


# %%
#there's currently a duplicate of columns in this dataset so we're going to remove the one with the most nans which has little to no data
print('The amount of missing data on Province_State column of CSSE is:', combinedOfCsvCSSE['Province_State'].isnull().sum())
print('The amount of missing data on Province/State column of CSSE is:', combinedOfCsvCSSE['Province/State'].isnull().sum())
print("")
print('The amount of missing data on Country_Region column of CSSE is:', combinedOfCsvCSSE['Country_Region'].isnull().sum())
print('The amount of missing data on Country/Region column of CSSE is:', combinedOfCsvCSSE['Country/Region'].isnull().sum())
print("")
print('The amount of missing data on Last_Update column of CSSE is:', combinedOfCsvCSSE['Last_Update'].isnull().sum())
print('The amount of missing data on Last Update column of CSSE is:', combinedOfCsvCSSE['Last Update'].isnull().sum())
print("")
print('The amount of missing data on Latitude column of CSSE is:', combinedOfCsvCSSE['Latitude'].isnull().sum())
print('The amount of missing data on Lat column of CSSE is:', combinedOfCsvCSSE['Lat'].isnull().sum())
print("")
print('The amount of missing data on Longitude column of CSSE is:', combinedOfCsvCSSE['Longitude'].isnull().sum())
print('The amount of missing data on Long_ column of CSSE is:', combinedOfCsvCSSE['Long_'].isnull().sum())
print("")
print('The amount of missing data on Incident_Rate column of CSSE is:', combinedOfCsvCSSE['Incident_Rate'].isnull().sum())
print('The amount of missing data on Incidence_Rate column of CSSE is:', combinedOfCsvCSSE['Incidence_Rate'].isnull().sum())
print("")
print('The amount of missing data on Case_Fatality_Ratio column of CSSE is:', combinedOfCsvCSSE['Case_Fatality_Ratio'].isnull().sum())
print('The amount of missing data on Case-Fatality_Ratio column of CSSE is:', combinedOfCsvCSSE['Case-Fatality_Ratio'].isnull().sum())


# %%
#drop the duplicate columns that have the most nans 
combinedOfCsvCSSE.drop(['Province/State', 'Country/Region','Last Update', 'Latitude','Longitude','Incidence_Rate','Case-Fatality_Ratio'], axis=1, inplace=True)


# %%
#show CSSE dataset with the changes
print(combinedOfCsvCSSE)


# %%
group_CSSE = combinedOfCsvCSSE[['Province_State','Deaths']].groupby('Province_State').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Deaths',color='red',title = 'States with more deaths',rot=0)
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more deaths')
plt.show()
print(group_CSSE.head(5))
#print(group_CSSE.sort_values("Deaths",ascending=False))
# %%
group_CSSE = combinedOfCsvCSSE[['Province_State','Confirmed']].groupby('Province_State').sum().reset_index().sort_values("Confirmed",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Confirmed',color='red',title = 'States with more confirmed',rot=0)
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()
print(group_CSSE.head(5))

# %%
group_CSSE = combinedOfCsvCSSE[['Province_State','Recovered']].groupby('Province_State').sum().reset_index().sort_values("Recovered",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Province_State',y='Recovered',color='red',title = 'States with more Recovered',rot=0)
sns.barplot(x='Province_State', y='Recovered', data = group_CSSE.head(5)).set_title('States with more recovered')
plt.show()
print(group_CSSE.head(5))


# %%
group_CSSE = combinedOfCsvCSSE[['Country_Region','Deaths']].groupby('Country_Region').sum().reset_index().sort_values("Deaths",ascending=False)
#group_CSSE.head(5).plot(kind='bar',x='Country_Region',y='Deaths',color='red',title = 'Regions with more deaths',rot=0)
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()
print(group_CSSE.head(5))

# %%
group_CSSE = combinedOfCsvCSSE[['Country_Region','Deaths']].groupby('Country_Region')
#sns.scatterplot(x='Confirmed', y='Deaths', data = group_CSSE.head(5), hue="Country_Region", palette="viridis", edgecolors="black", alpha=0.5, sizes=(10, 1000)).set_title('Regions with more deaths')
#plt.show()

# %%
#checking if any of the data frames if theres any similarities in the states columns of both datasets
#combinedOfCsv['Province_State'].isin(datasetCCI['state'])
print(combinedOfCsvCSSE[combinedOfCsvCSSE['Province_State'].isin(datasetCCI['state'].values)])

# %%
#merging both datasets and dropping duplicates to see any differences
df_diff = pd.concat([combinedOfCsvCSSE,datasetCCI]).drop_duplicates(keep=False)


# %%
print(df_diff)


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
combinedOfCsvCSSE['Province_State'].replace({'Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'American Samoa': 'AS', 
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
#Now checking the similarities of the dates of the two datasets 
similarities_of_CSSE_and_CCI = combinedOfCsvCSSE[combinedOfCsvCSSE['Province_State'].isin(datasetCCI['state'].values)]
print(similarities_of_CSSE_and_CCI)
# %%

