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
# opening up the file that isn't 
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

# %%
# group by province state but in order of the highest death cases
#group_CSSE = ProvinceUsesOnly.sort_values(['New_Deaths','Province_State','Country_Region'],ascending=False).reset_index()
group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
# %%
# making a joint plot of provincestate
sns.jointplot(data=group_CSSE, x="Confirmed", y="Deaths", kind="reg")
plt.suptitle("Province state regarding the correlation of confirmed cases and death cases")
# %%
# bar plot regarding the top 5 death cases when it comes to province state
#group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].groupby('Province_State').max().reset_index().sort_values('Deaths',ascending=False)
group_CSSE = ProvinceUsesOnly[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more deaths')
plt.show()
# %%

# group by province state but in order of the highest confirmed cases
group_CSSE = ProvinceUsesOnly[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Confirmed', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()

# %%
#Filtering cases cleaned categorizable for only province state uses
ProvinceUsesOnly_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].notna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]

ProvinceUsesOnly_without_date_filter =  ProvinceUsesOnly_without_date_filter[ProvinceUsesOnly_without_date_filter['New_Deaths'] < 30]
# %%
# group by province state but in order of the highest death cases
#group_CSSE = ProvinceUsesOnly.sort_values(['New_Deaths','Province_State','Country_Region'],ascending=False).reset_index()
group_CSSE = ProvinceUsesOnly_without_date_filter[['Province_State','New_Deaths']].sort_values('New_Deaths',ascending=False)
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = ProvinceUsesOnly_without_date_filter[['Province_State','New_Deaths']].groupby('Province_State').max().reset_index().sort_values('New_Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin)
# %%

# %%

#Filtering cases cleaned categorizable for only country region uses
CountryUsesOnly = cases_cleaned_categorizable[cases_cleaned_categorizable['Country_Region'].notna() & 
              cases_cleaned_categorizable['Province_State'].isna() &
              cases_cleaned_categorizable['Admin2'].isna()]

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(5).plot.pie(y='Deaths', figsize=(9, 9),autopct='%1.1f%%')

# %%
# group by country region
group_CSSE = CountryUsesOnly[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Regions with more deaths')
plt.show()

# %%
#Filtering cases cleaned categorizable for only province state uses but for US states
ProvinceUsesOnlyForUs = ProvinceUsesOnly[ProvinceUsesOnly['Country_Region'] == 'US']

# %%
#US states most deaths only
group_CSSE = ProvinceUsesOnlyForUs[['Province_State','Deaths']].sort_values('Deaths',ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Deaths', data = group_CSSE.head(5)).set_title('States with more confirmed')
plt.show()


