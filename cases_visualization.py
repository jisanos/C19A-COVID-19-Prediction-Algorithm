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
import calendar
import webbrowser
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.transform import dodge
alt.renderers.enable('altair_viewer')
#set the plot's theme to something more beautiful
sns.set()

# %%
# opening up the dataset
cases_df = pd.read_csv(".\\cases_cleaned_categorizable.csv")

world_pop = data_imports.world_pop_by_country()

# %% Renaming world population country column
world_pop = world_pop.rename(columns={'Country Name':'Country_Region',
                                      "2018":"Population"})
#%%
cases_df['date']= pd.to_datetime(cases_df['date'])


# %%
#check the info of the dataset to check for any problems
print(cases_df.info())
# %%
#Filtering cases cleaned categorizable for only province state uses
province_cases_df = cases_df[cases_df['Country_Region'].notna() & 
                             cases_df['Province_State'].notna() &
                             cases_df['Admin2'].isna()]

#taking out the unknown
province_cases_df = province_cases_df[province_cases_df[
    'Province_State'] != 'Unknown']
province_cases_df = province_cases_df[province_cases_df[
    'Country_Region'] != 'Unknown']
# %%Filtering cases cleaned categorizable for only country region
country_cases_df = cases_df[cases_df['Country_Region'].notna() & 
                            cases_df['Province_State'].isna() &
                            cases_df['Admin2'].isna()]
#taking out the unknown
country_cases_df = country_cases_df[country_cases_df[
    'Province_State'] != 'Unknown']
country_cases_df = country_cases_df[country_cases_df[
    'Country_Region'] != 'Unknown']

# Adding country population
country_cases_df = country_cases_df.merge(world_pop, on='Country_Region')
#%% Global Countries Bubble chart
# Selecting the 


agg_dic = {'Confirmed':'max','Deaths':'max','Population':'first'}

latest_values = country_cases_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Confirmed','Deaths'], ascending=False)

n_countries = 10

top_countries = latest_values.head(n_countries)

#Other countries

other_countries = latest_values.tail(-n_countries)

other_countries[['Deaths','Confirmed','Population']] = other_countries[[
    'Deaths','Confirmed','Population']].mean()

other_countries['Country_Region'] = 'Other Countries'

other_countries = other_countries.head(1)

to_plot = pd.concat([top_countries, other_countries])

plt.figure(figsize=(10, 10), dpi = 800) 

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

to_plot = country_cases_df[country_cases_df.Country_Region.isin(
    top_countries['Country_Region'].unique())]

chart = alt.Chart(to_plot).mark_circle().encode(
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
#chart.show()

chart.save('circle_chart.html')
webbrowser.open('circle_chart.html')

# %% Global State Deaths Barplot


agg_dic = {'Deaths':'max'}

to_plot = province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Deaths'], ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Deaths', data = to_plot.head(10)
            ).set_title("States with most deaths (Global)")

plt.xlabel('State')
plt.ylabel('Deaths')
plt.show()

# %% Pie chart of global state deaths

# to_plot = province_cases_df[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Province_State')
# to_plot.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title("Top 10 number of deaths per state", bbox={'facecolor':'0.8', 'pad':5})
# plt.show()

# %% Global State Cases Barplot
agg_dic = {'Confirmed':'max'}


to_plot = province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Confirmed'], ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Confirmed', data = to_plot.head(10)).set_title("States with most cases (Global)")

plt.xlabel('State')
plt.ylabel('Confirmed')
plt.show()
# %% state pie chart of global state cases
# group by country region
# to_plot = province_cases_df[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Province_State')
# to_plot.head(10).plot.pie(y='Confirmed', figsize=(11, 11),autopct='%1.1f%%',legend=None)
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
to_plot = province_cases_df_without_date_filter[['Province_State','New_Deaths']]
#plot a violin plot to see the confirmed and deaths of each province state as weight
#but with the (top 5 regarding the confirmed cases and deaths)
top5 = province_cases_df_without_date_filter[['Province_State','New_Deaths']].groupby(
    'Province_State').max().reset_index().sort_values('New_Deaths',ascending=False)
filteringViolin = to_plot[to_plot['Province_State'].isin(set(top5['Province_State'].head(4)))]
sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin) '''


# %% Country Level deaths

agg_dic = {'Deaths':'max'}

to_plot = province_cases_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Deaths'], ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Country_Region', y='Deaths', data = to_plot.head(10)).set_title('Deaths per Country')
plt.xlabel('Country')
plt.ylabel('Deaths')

plt.show()
# %% Pie chart of country level deaths
# group by country region
# to_plot = country_cases_df[['Country_Region','Deaths']].sort_values("Deaths",ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Country_Region')
# to_plot.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title('Top 10 number of deaths per country', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %%Pie chart of country level cases
# # group by country region
# to_plot = country_cases_df[['Country_Region','Confirmed']].sort_values("Confirmed",ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Country_Region')
# to_plot.head(10).plot.pie(y='Confirmed', figsize=(10, 10),autopct='%1.1f%%',legend=None)
# plt.title('Top 10 number of confirmed cases per country', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %%
# group by country region

agg_dic = {'Confirmed':'max'}

to_plot = province_cases_df.groupby(
    'Country_Region', as_index=False
    ).agg(agg_dic
          ).sort_values(['Confirmed'], ascending=False)

plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Country_Region', y='Confirmed', data = to_plot.head(10)).set_title('Cases per Country')
plt.xlabel('Country')
plt.ylabel('Confirmed')
plt.show()

# %% Filtering US states only
#Filtering cases cleaned categorizable for only province state uses but for US states
us_province_cases_df = province_cases_df[province_cases_df['Country_Region'] == 'US']

# %%
#US states most deaths only

agg_dic = {'Deaths':'max'}

to_plot = us_province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Deaths'], ascending=False)
          
          
plt.figure(figsize=(14, 6), dpi = 600) 
#bar plot regarding the top 5 total confirmed cases when it comes to province state
sns.barplot(x='Province_State', y='Deaths', data = to_plot.head(10)).set_title(
    'Deaths per State (US)')

plt.xlabel('State')
plt.ylabel('Deaths')

plt.show()

# %%
#US states most deaths only
agg_dic = {'Confirmed':'max'}
to_plot = us_province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Confirmed'], ascending=False)
#bar plot regarding the top 5 total confirmed cases when it comes to province state
plt.figure(figsize=(14, 6), dpi = 600) 
sns.barplot(x='Province_State', y='Confirmed', data = to_plot.head(10)).set_title('Cases per State (US)')
plt.xlabel('State')
plt.ylabel('Confirmed')
plt.show()

# %%
# # group by country region
# to_plot = us_province_cases_df[['Province_State','Confirmed']].sort_values('Confirmed',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Province_State')
# to_plot.head(10).plot.pie(y='Confirmed', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title('Top 10 number of confirmed cases per US states', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %%
# #US states most deaths only
# to_plot = us_province_cases_df[['Province_State','Active']].sort_values('Active',ascending=False)
# #bar plot regarding the top 5 total confirmed cases when it comes to province state
# sns.barplot(x='Province_State', y='Active', data = to_plot.head(5)).set_title('Top 5 number of active cases per US states')
# plt.show()

# %%
# group by country region
# to_plot = us_province_cases_df[['Province_State','Active']].sort_values('Active',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Province_State')
# to_plot.head(10).plot.pie(y='Active', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title('Top 10 number of active cases per US states', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %%
# group by country region
# to_plot = us_province_cases_df[['Province_State','Deaths']].sort_values('Deaths',ascending=False)

# #plot a pie chart regarding the top 5 deaths of countries
# to_plot = to_plot.set_index('Province_State')
# to_plot.head(10).plot.pie(y='Deaths', figsize=(12, 9),autopct='%1.1f%%',legend=None)
# plt.title('Top 10 number of deaths per US states', bbox={'facecolor':'0.8', 'pad':5})
# plt.show()
# %%
#Filtering cases cleaned categorizable for only province state uses
# country_cases_df_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
#     cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
#     & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
#               cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
# #taking out the unknowns
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Province_State'] != 'Unknown']
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
# #taking out unnecesaary values for a better viewing of the plot
# country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['New_Deaths'] < 1000]

# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] == 'US']
# %%
# # group by province state but in order of the highest death cases
# to_plot = country_cases_df_without_date_filter[['Province_State','New_Deaths']]
# #plot a violin plot to see the confirmed and deaths of each province state as weight
# #but with the (top 5 regarding the confirmed cases and deaths)
# top5 = country_cases_df_without_date_filter[['Province_State','Deaths']].groupby(
#     'Province_State').max().reset_index().sort_values('Deaths',ascending=False)
# filteringViolin = to_plot[to_plot['Province_State'].isin(set(top5['Province_State'].head(4)))]
# sns.violinplot(x='Province_State', y='New_Deaths', data = filteringViolin)
# plt.title('Top 5 number of deaths per US states')
# plt.show()
# %%
# #taking out the unknowns
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Province_State'] != 'Unknown']
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
# #taking out unnecesaary values for a better viewing of the plot
# country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['New_Confirmed'] < 1000]

# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] == 'US']
# %% Violingplot of new cases per state

agg_dic = {'Confirmed':'max'}

top_states = us_province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Confirmed'], ascending=False)

to_plot = us_province_cases_df[us_province_cases_df.Province_State.isin(
                top_states['Province_State'].unique()[:7])]



# filteringViolin = to_plot[to_plot['Province_State'].isin(set(top5['Province_State'].head(4)))]
plt.figure(figsize=(14, 6), dpi = 600) 
sns.violinplot(x='Province_State', y='New_Confirmed',
               data = to_plot[to_plot['New_Confirmed'] < 10000])

plt.title('Daily Cases Distribution (US)')
plt.xlabel('State')
plt.ylabel('New Cases')
plt.show()


# %% Violingplot of new deaths per state

agg_dic = {'Deaths':'max'}

top_states = us_province_cases_df.groupby(
    'Province_State', as_index=False
    ).agg(agg_dic
          ).sort_values(['Deaths'], ascending=False)

# Selecting on ly the top 7 states
to_plot = us_province_cases_df[us_province_cases_df.Province_State.isin(
                top_states['Province_State'].unique()[:7])]



# filteringViolin = to_plot[to_plot['Province_State'].isin(set(top5['Province_State'].head(4)))]
plt.figure(figsize=(14, 6), dpi = 600) 
sns.violinplot(x='Province_State', y='New_Deaths', data = to_plot[to_plot['New_Deaths'] < 50])

plt.title('Daily Deaths Distribution (US)')
plt.xlabel('State')
plt.ylabel('New Deaths')
plt.show()
# %%
# #Filtering cases cleaned categorizable for only province state uses
# country_cases_df_without_date_filter = cases_cleaned_categorizable_Without_Date_Filter[
#     cases_cleaned_categorizable_Without_Date_Filter['Country_Region'].notna() 
#     & cases_cleaned_categorizable_Without_Date_Filter['Province_State'].isna() &
#               cases_cleaned_categorizable_Without_Date_Filter['Admin2'].isna()]
# %%
# #taking out the unknowns
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Province_State'] != 'Unknown']
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
# #taking out unnecesaary values for a better viewing of the plot
# country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['New_Deaths'] < 1000]
# %%
# # group by province state but in order of the highest death cases
# to_plot = country_cases_df_without_date_filter[['Country_Region','New_Deaths']]
# #plot a violin plot to see the confirmed and deaths of each province state as weight
# #but with the (top 5 regarding the confirmed cases and deaths)
# top5 = country_cases_df_without_date_filter[['Country_Region','Deaths']].groupby(
#     'Country_Region').max().reset_index().sort_values('Deaths',ascending=False)
# filteringViolin = to_plot[to_plot['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
# sns.violinplot(x='Country_Region', y='New_Deaths', data = filteringViolin)
# plt.title('Top 5 number of deaths per country')
# plt.show()
# %%
# #taking out the unknowns
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Province_State'] != 'Unknown']
# country_cases_df_without_date_filter = country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['Country_Region'] != 'Unknown']
# #taking out unnecesaary values for a better viewing of the plot
# country_cases_df_without_date_filter =  country_cases_df_without_date_filter[
#     country_cases_df_without_date_filter['New_Confirmed'] < 1000]

# %%
# # group by province state but in order of the highest death cases
# to_plot = country_cases_df_without_date_filter[['Country_Region','New_Confirmed']]
# #plot a violin plot to see the confirmed and deaths of each province state as weight
# #but with the (top 5 regarding the confirmed cases and deaths)
# top5 = country_cases_df_without_date_filter[['Country_Region','Confirmed']].groupby(
#     'Country_Region').max().reset_index().sort_values('Confirmed',ascending=False)
# filteringViolin = to_plot[to_plot['Country_Region'].isin(set(top5['Country_Region'].head(4)))]
# sns.violinplot(x='Country_Region', y='New_Confirmed', data = filteringViolin)
# plt.title('Top 5 number of confirmed cases per country')
# plt.show()

# %% Prepairing heatmap

hm_df = country_cases_df
hm_df['date'] = pd.to_datetime(hm_df['date'], format='%Y/%m/%d')
hm_df.sort_values('date', inplace=True)

# creating columns of month,year seperately 
hm_df['month'] = hm_df['date'].dt.month
hm_df['year'] = hm_df['date'].dt.year
#change the number of months to name of months
hm_df['month'] = hm_df['month'].apply(lambda x: calendar.month_abbr[x])
# %% Grouping for confirmed cases

hm_confirmed_df = hm_df[['month','New_Confirmed','year']].groupby(
    ['month','year']).sum().reset_index()

# Pivoc the dataframe

hm_confirmed_df = hm_confirmed_df.pivot(index='month', columns='year',
                                        values='New_Confirmed')

#Ordering the months
months_ordered = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep',
                 'Oct', 'Nov', 'Dec']

hm_confirmed_df.index = pd.CategoricalIndex(hm_confirmed_df.index,
                                            categories=months_ordered,
                                            ordered=True)

hm_confirmed_df = hm_confirmed_df.sort_index()
#remove the dates that have no values since theyre future months of 2021
hm_confirmed_df = hm_confirmed_df.fillna(0)

#change the values to int
hm_confirmed_df = hm_confirmed_df.astype(int)

# %% Plotting global heatmap of monthly cases
plt.figure(figsize=(6, 6), dpi = 600) 
sns.heatmap(hm_confirmed_df, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)
# plt.figure(figsize=(14, 6), dpi = 600) 
plt.title('Monthly Confirmed Cases (Globally)')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()
# %%
total = hm_confirmed_df.loc[:,2020].sum() + hm_df.loc[:,2021].sum()
# %% Grouping for deaths

hm_deaths_df= hm_df[['month','New_Deaths','year']].groupby(
    ['month','year']).sum().reset_index()

hm_deaths_df = hm_deaths_df.pivot(index='month', columns='year',
                                  values='New_Deaths')

hm_deaths_df.index = pd.CategoricalIndex(hm_deaths_df.index,
                                            categories=months_ordered,
                                            ordered=True)

hm_deaths_df = hm_deaths_df.sort_index()

hm_deaths_df = hm_deaths_df.fillna(0)


hm_deaths_df = hm_deaths_df.astype(int)
# %% Plotting global heatmap of monthly deaths
plt.figure(figsize=(6, 6), dpi = 600) 
sns.heatmap(hm_deaths_df, fmt="d", annot=True, cmap='YlGnBu',linewidths=.5)
# plt.figure(figsize=(14, 6), dpi = 600) 
plt.title('Monthly Deaths (Globally)')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()

# %% 

# %% Grouping for confirmed cases
hm_confirmed_df = hm_df[['Country_Region','New_Confirmed','year']].groupby(
    ['Country_Region','year']).sum().reset_index()

# Pivoc the dataframe
hm_confirmed_df = hm_confirmed_df.pivot(index='Country_Region', columns='year',
                                        values='New_Confirmed')

hm_confirmed_df = hm_confirmed_df.sort_values([2020,2021], ascending=False)
hm_confirmed_df = hm_confirmed_df.reset_index()
hm_confirmed_df = hm_confirmed_df.head(6)
hm_confirmed_df.columns = hm_confirmed_df.columns.map(str)

data = hm_confirmed_df.to_dict('list')
source = ColumnDataSource(data = data)
# 100000000
output_file('vbar.html')
p = figure(x_range=hm_confirmed_df.Country_Region.tolist(),
           y_range=(0, 25000000), 
           title='Yearly Confirmed Cases (Globally)',
           height=350, toolbar_location=None, tools="")

p.vbar(x=dodge('Country_Region', -0.25, range=p.x_range), top='2020',
       source=source,
       width=0.2, color="#c9d9d3", legend_label='2020')

p.vbar(x=dodge('Country_Region',  0.0,  range=p.x_range), top='2021', 
       source=source,
       width=0.2, color="#718dbf", legend_label='2021')

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"
show(p)

# %% Grouping for confirmed cases
hm_confirmed_df = hm_df[['Country_Region','New_Deaths','year']].groupby(
    ['Country_Region','year']).sum().reset_index()

# Pivoc the dataframe
hm_confirmed_df = hm_confirmed_df.pivot(index='Country_Region', columns='year',
                                        values='New_Deaths')

hm_confirmed_df = hm_confirmed_df.sort_values([2020,2021], ascending=False)
hm_confirmed_df = hm_confirmed_df.reset_index()
hm_confirmed_df = hm_confirmed_df.head(6)
hm_confirmed_df.columns = hm_confirmed_df.columns.map(str)

data = hm_confirmed_df.to_dict('list')
source = ColumnDataSource(data = data)
# 100000000
output_file('vbar.html')
p = figure(x_range=hm_confirmed_df.Country_Region.tolist(),
           y_range=(0, 650000), 
           title='Yearly Deaths Cases (Globally)',
           height=350, toolbar_location=None, tools="")

p.vbar(x=dodge('Country_Region', -0.25, range=p.x_range), top='2020',
       source=source,
       width=0.2, color="#c9d9d3", legend_label='2020')

p.vbar(x=dodge('Country_Region',  0.0,  range=p.x_range), top='2021', 
       source=source,
       width=0.2, color="#718dbf", legend_label='2021')

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"
show(p)
# %% Grouping for confirmed cases

hm_confirmed_df = hm_df[['New_Confirmed','date']].groupby(
    ['date']).sum().reset_index()

hm_confirmed_df = hm_confirmed_df.sort_index()
#remove the dates that have no values since theyre future months of 2021
hm_confirmed_df = hm_confirmed_df.fillna(0)

#hm_confirmed_df['date'] = hm_confirmed_df.to_datetime(hm_confirmed_df['date'])
# Plotting line monthly cases
output_file("datetime.html")

# create a new plot with a datetime axis type
p = figure(width=800, height=250, x_axis_type="datetime",title = 'Monthly Confirmed Cases (Globally)')

p.line(hm_confirmed_df['date'], hm_confirmed_df['New_Confirmed'], color='navy', alpha=0.5)

show(p)

# %% Grouping for death cases

hm_confirmed_df = hm_df[['New_Deaths','date']].groupby(
    ['date']).sum().reset_index()

hm_confirmed_df = hm_confirmed_df.sort_index()
#remove the dates that have no values since theyre future months of 2021
hm_confirmed_df = hm_confirmed_df.fillna(0)

#hm_confirmed_df['date'] = hm_confirmed_df.to_datetime(hm_confirmed_df['date'])
# Plotting line monthly cases
output_file("datetime.html")

# create a new plot with a datetime axis type
p = figure(width=800, height=250, x_axis_type="datetime",title = 'Monthly Death Cases (Globally)')

p.line(hm_confirmed_df['date'], hm_confirmed_df['New_Deaths'], color='navy', alpha=0.5)

show(p)