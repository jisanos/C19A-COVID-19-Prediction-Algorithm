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
cases_cleaned_categorizable = pd.read_csv(".\\cases_cleaned_categorizable.csv")
cases_cleaned_categorizable_Without_Date_Filter = pd.read_csv(".\\cases_cleaned_categorizable.csv")
#%%
#using the latest data instead of all the data
cases_cleaned_categorizable['date']= pd.to_datetime(cases_cleaned_categorizable['date'])
cases_cleaned_categorizable= cases_cleaned_categorizable[cases_cleaned_categorizable["date"] == cases_cleaned_categorizable['date'].max()]
# %%
#check the info of the dataset to check for any problems
print(cases_cleaned_categorizable.info())
# %%
#Filtering cases cleaned categorizable for only province state uses
ProvinceUsesOnly = cases_cleaned_categorizable[cases_cleaned_categorizable['Country_Region'].notna() & 
              cases_cleaned_categorizable['Province_State'].notna() &
              cases_cleaned_categorizable['Admin2'].isna()]

#taking out the unknown
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Province_State'] != 'Unknown']
ProvinceUsesOnly = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
ProvinceUsesOnly_Correlation =  ProvinceUsesOnly[ProvinceUsesOnly['Deaths'] < 100000]
# %%
# group by province state but in order of the highest death cases
#group_CSSE = ProvinceUsesOnly.sort_values(['New_Deaths','Province_State','Country_Region'],ascending=False).reset_index()
group_CSSE = ProvinceUsesOnly_Correlation[['Province_State','Deaths','Confirmed']]

# making a joint plot of provincestate
sns.jointplot(data=group_CSSE, x="Confirmed", y="Deaths", kind="reg")
plt.suptitle("Province state regarding the correlation of confirmed cases and death cases")
# %%
# bar plot regarding the top 5 death cases when it comes to province state
#group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].groupby('Province_State').max().reset_index().sort_values('Deaths',ascending=False)
group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
#sns.set(rc = {'figure.figsize':(15,15)})
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('Top 5 province states with most deaths')
plt.show()

# %%
# group by country region
group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 death cases by Province State", bbox={'facecolor':'0.8', 'pad':5})

# %%

# group by province state but in order of the highest confirmed cases
group_CSSE = ProvinceUsesOnly[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('Top 5 province states with most confirmed')
plt.show()

# %%
# group by country region
group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 death cases by Province State", bbox={'facecolor':'0.8', 'pad':5})

# %%
# group by country region
group_CSSE = ProvinceUsesOnly[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(11, 11),autopct='%1.1f%%',legend=None)
plt.title("Top 10 confirmed cases by Province State", bbox={'facecolor':'0.8', 'pad':5})

# %%

'''
#Filtering cases cleaned categorizable for only province state uses
ProvinceUsesOnly_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].notna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]

ProvinceUsesOnly_without_date_filter = ProvinceUsesOnly_without_date_filter[
    ProvinceUsesOnly_without_date_filter['Province_State'] != 'Unknown']
ProvinceUsesOnly_without_date_filter = ProvinceUsesOnly_without_date_filter[
    ProvinceUsesOnly_without_date_filter['Country_Region'] != 'Unknown']

ProvinceUsesOnly_without_date_filter =  ProvinceUsesOnly_without_date_filter[
    ProvinceUsesOnly_without_date_filter['New_Deaths'] < 30]

'''
# %%
'''
# group by province state but in order of the highest death cases
group_CSSE = ProvinceUsesOnly_without_date_filter[['Province_State','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = ProvinceUsesOnly_without_date_filter[['Province_State','New_Deaths']].groupby(
    'Province_State').max().reset_index().sort_values('New_Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin) '''
# %%

# %%

#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = cases_cleaned_categorizable[cases_cleaned_categorizable['Country_Region'].notna() & 
              cases_cleaned_categorizable['Province_State'].isna() &
              cases_cleaned_categorizable['Admin2'].isna()]
#taking out the unknown
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Province_State'] != 'Unknown']
CountryUsesOnly = CountryUsesOnly[CountryUsesOnly['Country_Region'] != 'Unknown']

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Top 5 country regions with most deaths')
plt.show()
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 death cases by country region", bbox={'facecolor':'0.8', 'pad':5})
# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(10, 10),autopct='%1.1f%%',legend=None)
plt.title("Confirmed cases by country region", bbox={'facecolor':'0.8', 'pad':5})

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Confirmed', data = group_CSSE.head(5)).set_title('Top 5 country regions with most cases')
plt.show()

# %%
#Filtering cases cleaned categorizable for only province state uses but for US states
ProvinceUsesOnlyForUs = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] == 'US']

# %%
#US states most deaths only
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title(
    'Top 5 US States with most deaths')
plt.show()

# %%
#US states most deaths only
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('Top 5 US States with most confirmed cases')
plt.show()

# %%
# group by country region
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 US confirmed cases by Province State", bbox={'facecolor':'0.8', 'pad':5})


# %%
# group by country region
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Province_State')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title("Top 10 US death cases by Province State", bbox={'facecolor':'0.8', 'pad':5})

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
