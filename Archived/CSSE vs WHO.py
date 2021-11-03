# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt



# %%
#extracting all files from local directory for WHO

path = "/Users/LuisGa/Documents/GitHub/C19A-COVID-19-Prediction-Algorithm-CAPSTONE/CSSE_C-19/csse_covid_19_data"
all_filenames_WHO = [i for i in glob.glob('*.{}'.format("csv"))]

WHO = pd.read_csv('.\\CSSE_C-19\\who_covid_19_situation_reports\\who_covid_19_sit_rep_time_series\\who_covid_19_sit_rep_time_series.csv')


# %%
#Changing Dataframe column names to Dates and Cases from WHO DF
dfWHO = pd.DataFrame(WHO)

dfWHO_new = pd.melt(dfWHO,col_level = 0, id_vars=['Province/States', 'Country/Region','WHO region', 'WHO region label'])

dfWHO_New = dfWHO_new.rename(columns = {'variable': 'Dates', 'value':'Cases'})

WHO_CASES = dfWHO_New.reindex(columns = ['Dates','Province/States','Country/Region','WHO region','WHO region label','Cases'])



# %%
#extracting all files from local directory for CSSE

path = "./CSSE_C-19/csse_covid_19_data/csse_covid_19_time_series/"
extension_CSSE = 'csv'
all_filenames_CSSE = [i for i in glob.glob(path + '*.{}'.format(extension_CSSE))]




# %%
#Choosing only the global .csv files
output = []
for i in all_filenames_CSSE:
    if 'global' in i.lower():
        output.append(i)


# %%
#separating the Confirmed, death and recovered cases files for further filtering
csv_output0 = pd.read_csv(output[0])
csv_output1 = pd.read_csv(output[1])
csv_output2 = pd.read_csv(output[2])


# %%
#melting all CSVs files from CSSE
df0 = pd.DataFrame(csv_output0)

df0_new = pd.melt(df0,col_level = 0, id_vars=['Province/State', 'Country/Region', 'Lat','Long'])

df0_New = df0_new.rename(columns = {'variable': 'Dates','value':'ConfirmedCases'})

ConfirmedCases = df0_New.reindex(columns = ['Dates','Province/State','Country/Region','Lat','Long','ConfirmedCases'])
#print(ConfirmedCases)
######################################################################################################
df1 = pd.DataFrame(csv_output1)

df1_new = pd.melt(df1,col_level = 0, id_vars=['Province/State', 'Country/Region', 'Lat','Long'])

df1_New = df1_new.rename(columns = {'variable': 'Dates','value':'DeathCases'})

DeathCases = df1_New.reindex(columns = ['Dates','Province/State','Country/Region','Lat','Long','DeathCases'])
#print(DeathCases)
#######################################################################################################
df2 = pd.DataFrame(csv_output2)

df2_new = pd.melt(df2,col_level = 0, id_vars=['Province/State', 'Country/Region', 'Lat','Long'])

df2_New = df2_new.rename(columns = {'variable': 'Dates','value':'RecoveredCases'})

RecoveredCases = df2_New.reindex(columns = ['Dates','Province/State','Country/Region','Lat','Long','RecoveredCases'])
#print(RecoveredCases)


# %%
#Differences between the dataframes from the Confirmed, Death and recovered cases from CSSE

df_merge1 = pd.merge(ConfirmedCases,DeathCases, how = "right", on = ["Dates","Country/Region","Province/State","Lat","Long"])

df_merge2 = pd.merge(df_merge1,RecoveredCases,how = "right", on = ["Dates","Country/Region","Province/State","Lat","Long"] )

#print(df_merge2)


# %%
#Renaming Columns for better understanding
WHO_CASES = WHO_CASES.rename(columns={"Province/States":"Province/State", "Cases":"WHO Confirmed Cases"})
#WHO_CASES


# %%
Merged_Confirmed_df = pd.merge(WHO_CASES,df_merge2,how = "right", on = ["Dates","Country/Region","Province/State"])
#Merged_Confirmed_df


# %%
#Looking for data between CSSE and WHO which are the same in both
Confirmed_Equal = Merged_Confirmed_df[Merged_Confirmed_df["WHO Confirmed Cases"] == Merged_Confirmed_df["ConfirmedCases"]]


# %%
#Looking for differences between both CSSE and WHO data
Confirmed_diff = Merged_Confirmed_df[(Merged_Confirmed_df["WHO Confirmed Cases"] != Merged_Confirmed_df["ConfirmedCases"]) & (Merged_Confirmed_df["WHO Confirmed Cases"].notna())]

#print(Merged_Confirmed_df)

# %%
#Filtered by countries/regions for better visualization on graphs
sum_test = Merged_Confirmed_df[["Country/Region","ConfirmedCases","DeathCases","RecoveredCases"]].groupby("Country/Region").sum().reset_index()

#%%
#Looking for Mean Value of all Confirmed Cases and Graph

Merged_Confirmed_df['Mean'] = Merged_Confirmed_df[['WHO Confirmed Cases', 'ConfirmedCases']].mean(axis=1)

#Graphing filtered data by Country/Region
sns.barplot(x='Country/Region', y='ConfirmedCases', data = sum_test.iloc[42:50]).set_title('Confirmed Cases')
plt.show()


# %%



