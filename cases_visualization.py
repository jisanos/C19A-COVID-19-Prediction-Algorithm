# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 15:28:41 2021

@author: rayni
"""

# %%
#adding libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#set the plot's theme to something more beautiful
sns.set()

# %%
# opening up the dataset
cases_df = pd.read_csv(".\\cases_cleaned_categorizable.csv")
cases_cleaned_categorizable_Without_Date_Filter = pd.read_csv(".\\cases_cleaned_categorizable.csv")
#%%
#using the latest data (most recent date) instead of all the data
cases_df['date']= pd.to_datetime(cases_df['date'])
cases_df= cases_df[cases_df["date"] == cases_df['date'].max()]
# %%
#check the info of the dataset to check for any problems
print(cases_df.info())
# %%
#Filtering cases cleaned categorizable for only province state uses
province_cases_df = cases_df[cases_df['Country_Region'].notna() & 
                             cases_df['Province_State'].notna() &
                             cases_df['Admin2'].isna()]

#taking out the unknown
province_cases_df = province_cases_df[province_cases_df['Province_State'] != 'Unknown']
province_cases_df = province_cases_df[province_cases_df['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
# province_cases_df_Correlation =  province_cases_df[(province_cases_df['Deaths'] < 5000)]

#%%Bubble chart
#Top 10 results for death cases in countries

Top_10 = Last_day.nlargest(10,'Deaths')

print(Top_10)

#Other countries

Other_Countries = Last_day.nsmallest(3978,'Deaths')

Other_Countries.head()

Other_Countries['Other_Countries'] = Other_Countries['Deaths'].mean()

#Others['Country Region'] = 'Other Countries'
#%% 
#plotting bubble plot based on data

#reason the y axis has exponential value on top is because the number is too big so 7 is actually 7M

sns.scatterplot(data=Top_10, x="Deaths", y="Confirmed", size=200, legend=False, sizes=(20, 2000))

sns.scatterplot(data=Other_Countries, x="Other_Countries", y="Other_Countries", size=200, legend=False, sizes=(20, 2000))

x,y= Top_10['Deaths'],Top_10['Confirmed']

for i, txt in enumerate(Top_10.Country_Region):
    plt.annotate(txt,(Top_10.Deaths.iat[i],Top_10.Confirmed.iat[i]))

#Other Countries labels
for i, txt in enumerate(Other_Countries.Country_Region):
    plt.annotate('Other Countries',(Other_Countries.Other_Countries.iat[i],Other_Countries.Other_Countries.iat[i]))
#%%

#Title and labels
plt.title('Top 10 Country/Regions(Deaths) Bubble Chart')
plt.xlabel('Deaths')
plt.ylabel('Confirmed')


# %%
# bar plot regarding the top 5 death cases when it comes to province state
#group_CSSE = province_cases_df[['Province_State','Deaths']].groupby('Province_State').max().reset_index().sort_values('Deaths',ascending=False)
group_CSSE = province_cases_df[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
#sns.set(rc = {'figure.figsize':(15,15)})
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title("Top 5 number of deaths per state")
plt.show()

# %%
# group by country region
group_CSSE = province_cases_df[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 number of deaths per state", bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# number of deaths per country
# %%

# group by province state but in order of the highest confirmed cases
group_CSSE = province_cases_df[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title("Top 5 number of confirmed cases per state")
plt.show()

# %%
# group by country region
group_CSSE = province_cases_df[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(11, 11),autopct='%1.1f%%',legend=None)
plt.title("Top 10 number of confirmed cases per state", bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%

'''
#Filtering cases cleaned categorizable for only province state uses
province_cases_df_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].notna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]

province_cases_df_without_date_filter = province_cases_df_without_date_filter[
    province_cases_df_without_date_filter['Province_State'] != 'Unknown']
province_cases_df_without_date_filter = province_cases_df_without_date_filter[
    province_cases_df_without_date_filter['Country_Region'] != 'Unknown']

province_cases_df_without_date_filter =  province_cases_df_without_date_filter[
    province_cases_df_without_date_filter['New_Deaths'] < 30]

'''
# %%
'''
# group by province state but in order of the highest death cases
group_CSSE = province_cases_df_without_date_filter[['Province_State','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = province_cases_df_without_date_filter[['Province_State','New_Deaths']].groupby(
    'Province_State').max().reset_index().sort_values('New_Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin) '''
# %%

# %%

#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = cases_df[cases_df['Country_Region'].notna() & 
              cases_df['Province_State'].isna() &
              cases_df['Admin2'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Top 5 number of deaths per country')
plt.show()
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of deaths per country', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(10, 10),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of confirmed cases per country', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Confirmed', data = group_CSSE.head(5)).set_title('Top 10 number of confirmed cases per country')
plt.show()

# %%
#Filtering cases cleaned categorizable for only province state uses but for US states
province_cases_dfForUs = province_cases_df[province_cases_df['Country_Region'] == 'US']

# %%
#US states most deaths only
group_CSSE = province_cases_dfForUs[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title(
    'Top 5 number of deaths per US states')
plt.show()

# %%
#US states most deaths only
group_CSSE = province_cases_dfForUs[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('Top 5 number of confirmed cases per US states')
plt.show()

# %%
# group by country region
group_CSSE = province_cases_dfForUs[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of confirmed cases per US states', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
#US states most deaths only
group_CSSE = province_cases_dfForUs[['Province_State','Active']].sort_values('Active',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Active', data = group_CSSE.head(5)).set_title('Top 5 number of active cases per US states')
plt.show()

# %%
# group by country region
group_CSSE = province_cases_dfForUs[['Province_State','Active']].sort_values('Active',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Active', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of active cases per US states', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
# group by country region
group_CSSE = province_cases_dfForUs[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of deaths per US states', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
#Filtering cases cleaned categorizable for only province state uses
CountryUsesOnly_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
#taking out the unknowns
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Province_State'] != 'Unknown']
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
CountryUsesOnly_without_date_filter =  CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['New_Deaths'] < 1000]

CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] == 'US']
# %%
# group by province state but in order of the highest death cases
group_CSSE = CountryUsesOnly_without_date_filter[['Province_State','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = CountryUsesOnly_without_date_filter[['Province_State','Deaths']].groupby(
    'Province_State').max().reset_index().sort_values('Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin)
plt.title('Top 5 number of deaths per US states')
plt.show()
# %%
#taking out the unknowns
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Province_State'] != 'Unknown']
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
CountryUsesOnly_without_date_filter =  CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['New_Confirmed'] < 1000]

CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] == 'US']
# %%
# group by province state but in order of the highest death cases
group_CSSE = CountryUsesOnly_without_date_filter[['Province_State','New_Confirmed']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = CountryUsesOnly_without_date_filter[['Province_State','Confirmed']].groupby(
    'Province_State').max().reset_index().sort_values('Confirmed',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Confirmed', data = filteringViolin)
plt.title('Top 5 number of confirmed cases per US states')
plt.show()
# %%
#Filtering cases cleaned categorizable for only province state uses
CountryUsesOnly_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
#taking out the unknowns
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Province_State'] != 'Unknown']
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
CountryUsesOnly_without_date_filter =  CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['New_Deaths'] < 1000]
# %%
# group by province state but in order of the highest death cases
group_CSSE = CountryUsesOnly_without_date_filter[['Country_Region','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = CountryUsesOnly_without_date_filter[['Country_Region','Deaths']].groupby(
    'Country_Region').max().reset_index().sort_values('Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
sns.violinplot(x='Country_Region', y='New_Deaths', data = filteringViolin)
plt.title('Top 5 number of deaths per country')
plt.show()
# %%
#taking out the unknowns
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Province_State'] != 'Unknown']
CountryUsesOnly_without_date_filter = CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
CountryUsesOnly_without_date_filter =  CountryUsesOnly_without_date_filter[
    CountryUsesOnly_without_date_filter['New_Confirmed'] < 1000]

# %%
# group by province state but in order of the highest death cases
group_CSSE = CountryUsesOnly_without_date_filter[['Country_Region','New_Confirmed']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = CountryUsesOnly_without_date_filter[['Country_Region','Confirmed']].groupby(
    'Country_Region').max().reset_index().sort_values('Confirmed',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
sns.violinplot(x='Country_Region', y='New_Confirmed', data = filteringViolin)
plt.title('Top 5 number of confirmed cases per country')
plt.show()