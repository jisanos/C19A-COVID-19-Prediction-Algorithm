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
import altair as alt
import data_imports
#set the plot's theme to something more beautiful
sns.set()

# %%
# opening up the dataset
cases_df = pd.read_csv(".\\cases_cleaned_categorizable.csv")
cases_cleaned_categorizable_Without_Date_Filter = pd.read_csv(".\\cases_cleaned_categorizable.csv")
world_pop = data_imports.world_pop_by_country()

# %% Renaming world population country column
world_pop = world_pop.rename(columns={'Country Name':'Country_Region', "2018":"Population"})
#%%
cases_df['date']= pd.to_datetime(cases_df['date'])

# Boolean containing only latest values. To be used for filtering
latest_date = (cases_df["date"] == cases_df['date'].max())
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
# %%Filtering cases cleaned categorizable for only country region
country_cases_df = cases_df[cases_df['Country_Region'].notna() & 
                            cases_df['Province_State'].isna() &
                            cases_df['Admin2'].isna()]
#taking out the unknown
country_cases_df = country_cases_df[country_cases_df['Province_State'] != 'Unknown']
country_cases_df = country_cases_df[country_cases_df['Country_Region'] != 'Unknown']

# Adding country population
country_cases_df = country_cases_df.merge(world_pop, on='Country_Region')
#%% Global Countries Bubble chart
#Top results for death cases in countries
country_cases_df = country_cases_df.sort_values(['Confirmed','Deaths'], ascending=False)

latest_date = (country_cases_df["date"] == country_cases_df['date'].max())

n_countries = 7

top_countries = country_cases_df[latest_date].head(n_countries)

#Other countries

other_countries = country_cases_df[latest_date].tail(-n_countries)

other_countries[['Deaths','Confirmed','Population']] = other_countries[[
    'Deaths','Confirmed','Population']].mean()

other_countries['Country_Region'] = 'Other Countries'

other_countries = other_countries.head(1)

to_plot = pd.concat([top_countries, other_countries])

plt.figure(figsize=(14, 6), dpi = 800) 

sns.scatterplot(data=to_plot, x="Deaths", y="Confirmed", alpha=0.7, size='Population',
                hue='Country_Region',sizes=(100,6000), legend=False)


for i, txt in enumerate(to_plot.Country_Region):
    plt.annotate(txt,(to_plot.Deaths.iat[i],to_plot.Confirmed.iat[i]))


#Title and labels
plt.title('Confirmed vs Death Bubble Chart (Global)')
plt.xlabel('Deaths')
plt.ylabel('Confirmed')
plt.show()

# %% Circle Chart Global Countries

Top_10 = country_cases_df[country_cases_df.Country_Region.isin(top_countries['Country_Region'].unique())]

chart = alt.Chart(Top_10).mark_circle().encode(
        x= 'date',
        y= 'Country_Region',
        color = 'Country_Region',
        size = alt.Size('New_Confirmed',
                        scale = alt.Scale(range=[0,1000]),
                        legend=alt.Legend(title='Daily new cases'))
        ).properties(
            width=800,
            height=300
        )
chart.show()
# %% Global State Deaths Barplot

latest_date = (province_cases_df["date"] == province_cases_df['date'].max())

to_plot = province_cases_df[latest_date].sort_values('Deaths',ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Deaths', data = to_plot.head(10)).set_title("States with most deaths (Global)")

plt.xlabel('State')
plt.ylabel('Deaths')
plt.show()

# %% Pie chart of global state deaths

# group_CSSE = province_cases_df[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Province_State')
# group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title("Top 10 number of deaths per state", bbox={'facecolor':'0.8', 'pad':5})
# plt.show()

# %% Global State Cases Barplot

to_plot = province_cases_df[latest_date].sort_values('Confirmed',ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Confirmed', data = to_plot.head(10)).set_title("States with most cases (Global)")

plt.xlabel('State')
plt.ylabel('Confirmed')
plt.show()
# %% state pie chart of global state cases
# group by country region
# group_CSSE = province_cases_df[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# group_CSSE = group_CSSE.set_index('Province_State')
# group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(11, 11),autopct='%1.1f%%',legend=None)
# plt.title("Top 10 number of confirmed cases per state", bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
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
# group by country region
group_CSSE = country_cases_df[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#a bar plot to show the top 5 deaths of countries
sns.barplot(x='Country_Region', y='Deaths', data = group_CSSE.head(5)).set_title('Top 5 number of deaths per country')
plt.show()
# %%
# group by country region
group_CSSE = country_cases_df[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of deaths per country', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
# group by country region
group_CSSE = country_cases_df[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

#plot a pie chart regarding the top 5 deaths of countries
group_CSSE = group_CSSE.set_index('Country_Region')
group_CSSE.head(10).plot.pie(y='Confirmed', figsize=(10, 10),autopct='%1.1f%%',legend=None)
plt.title('Top 10 number of confirmed cases per country', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
# %%
# group by country region
group_CSSE = country_cases_df[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

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
country_cases_df_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
#taking out the unknowns
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Province_State'] != 'Unknown']
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['New_Deaths'] < 1000]

country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] == 'US']
# %%
# group by province state but in order of the highest death cases
group_CSSE = country_cases_df_without_date_filter[['Province_State','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = country_cases_df_without_date_filter[['Province_State','Deaths']].groupby(
    'Province_State').max().reset_index().sort_values('Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin)
plt.title('Top 5 number of deaths per US states')
plt.show()
# %%
#taking out the unknowns
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Province_State'] != 'Unknown']
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['New_Confirmed'] < 1000]

country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] == 'US']
# %%
# group by province state but in order of the highest death cases
group_CSSE = country_cases_df_without_date_filter[['Province_State','New_Confirmed']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = country_cases_df_without_date_filter[['Province_State','Confirmed']].groupby(
    'Province_State').max().reset_index().sort_values('Confirmed',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Confirmed', data = filteringViolin)
plt.title('Top 5 number of confirmed cases per US states')
plt.show()
# %%
#Filtering cases cleaned categorizable for only province state uses
country_cases_df_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
    cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
    & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
              cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
#taking out the unknowns
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Province_State'] != 'Unknown']
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['New_Deaths'] < 1000]
# %%
# group by province state but in order of the highest death cases
group_CSSE = country_cases_df_without_date_filter[['Country_Region','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = country_cases_df_without_date_filter[['Country_Region','Deaths']].groupby(
    'Country_Region').max().reset_index().sort_values('Deaths',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
sns.violinplot(x='Country_Region', y='New_Deaths', data = filteringViolin)
plt.title('Top 5 number of deaths per country')
plt.show()
# %%
#taking out the unknowns
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Province_State'] != 'Unknown']
country_cases_df_without_date_filter = country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
#taking out unnecesaary values for a better viewing of the plot
country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
    country_cases_df_without_date_filter['New_Confirmed'] < 1000]

# %%
# group by province state but in order of the highest death cases
group_CSSE = country_cases_df_without_date_filter[['Country_Region','New_Confirmed']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = country_cases_df_without_date_filter[['Country_Region','Confirmed']].groupby(
    'Country_Region').max().reset_index().sort_values('Confirmed',ascending=False)
filteringViolin = group_CSSE[group_CSSE['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
sns.violinplot(x='Country_Region', y='New_Confirmed', data = filteringViolin)
plt.title('Top 5 number of confirmed cases per country')
plt.show()