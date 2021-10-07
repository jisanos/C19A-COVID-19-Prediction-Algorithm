# C19A (CIPA) COVID-19 Prediction Algorithm (CAPSTONE Project)

Repository for CIPA Capstone project


## Import all of the data to the top level directory (this project's dir)

Cases and Deaths:

`git clone https://github.com/CSSEGISandData/COVID-19.git "./CSSE_C-19"`

Vaccinations, Testing:

`git clone https://github.com/govex/COVID-19.git "./CCI_C-19"`

Alternate branch of CCI containing US State Level Policy Tracker:

`git clone -b govex_data https://github.com/govex/COVID-19.git "./CCI_C-19_Policies"`

## Dictionary
CSSE: Johns Hopkins Center for Systems Science and Engineering

CCI: Johns Hopkins Centers for Civic Impact

WHO: World Health Organization

# Paths of datasets being used

csse_covid_19_daily_reports.py
`.\\CSSE_C-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\`

`.\\CCI_C-19\\data_tables\\testing_data\\time_series_covid19_US.csv`

CSSE vs WHO.py

`.\\CSSE_C-19\\who_covid_19_situation_reports\\who_covid_19_sit_rep_time_series\\who_covid_19_sit_rep_time_series.csv`

`./CSSE_C-19/csse_covid_19_data/csse_covid_19_time_series/`


policies_analysis.py

`.\\CCI_C-19_Policies\\data_tables\\policy_data\\table_data\\Current\\`

