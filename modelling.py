# this python file consists of all the functions required by the main python file to function

# the main python file - epidemicModelling.py

# @st.cache has been used in most of the functions to optimise performance by enhancing function executions and is extremely useful when dealing with data loading from the web and manipulation of large datasets - Refer https://docs.streamlit.io/en/0.80.0/caching.html

###### NECESSARY IMPORTS ######
import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

# function defined for sidebar menu animation
@st.cache(show_spinner=False)
def sidebar_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.json()

# function defined for main intro page animation
@st.cache(show_spinner=False)
def intro_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.json()

###### DATA CLEANING ######
# information about the datasets have been provided in the main python file


# function defined for cleaning the dataset - cases_country.csv
# FIRST DATA FRAME(COUNTRY DATA)
@st.cache(show_spinner=False)
def country_clean():
    path = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv'
    country_data = pd.read_csv(path)
    country_data = country_data.rename(columns={'Country_Region': 'Country', 'Long_': 'lon', 'Lat': 'lat'})
    country_data = country_data[(country_data.Country != 'Diamond Princess') & (country_data.Country != 'MS Zaandam')]
    country_data = country_data.reset_index(drop=True)
    country_data['Population']=population_list()
    country_data[['lon', 'lat']] = country_data[['lon', 'lat']].apply(pd.to_numeric)
    country_data = country_data.fillna(0)
    country_data['Country'] = country_data['Country'].replace('Korea, South', 'Korea (South)')
    country_data['Country'] = country_data['Country'].replace('Taiwan*', 'Taiwan')
    country_data['Country'] = country_data['Country'].replace('US', 'United States')

    return country_data

# function defined for cleaning the dataset - time_series_covid19_confirmed_global.csv
# SECOND DATA FRAME(INFECTED POPULATION DATA)
@st.cache(show_spinner=False)
def infected_clean():
    path = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    infected_data = pd.read_csv(path)
    infected_data = infected_data.rename(columns={'Country/Region': 'Country'})
    infected_data = infected_data[(infected_data.Country != 'Diamond Princess') & (infected_data.Country != 'MS Zaandam')]
    infected_data = infected_data.reset_index(drop=True)
    infected_data = infected_data.drop(['Province/State','Lat', 'Long'], axis=1)
    infected_data['Country'] = infected_data['Country'].replace('Taiwan*', 'Taiwan')
    infected_data['Country'] = infected_data['Country'].replace('Korea, South', 'Korea (South)')
    infected_data['Country'] = infected_data['Country'].replace('US', 'United States')
    infected_data = infected_data.groupby(['Country']).sum().reset_index()

    return infected_data

# function defined for cleaning the dataset - time_series_covid19_recovered_global.csv
# THIRD DATA FRAME(RECOVERED POPULATION DATA)
@st.cache(show_spinner=False)
def recovered_clean():
    path = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    recovered_data = pd.read_csv(path)
    recovered_data = recovered_data.rename(columns={'Country/Region': 'Country'})
    recovered_data = recovered_data[(recovered_data.Country != 'Diamond Princess') & (recovered_data.Country != 'MS Zaandam')]
    recovered_data = recovered_data.reset_index(drop=True)
    recovered_data = recovered_data.drop(['Province/State','Lat', 'Long'], axis=1)
    recovered_data['Country'] = recovered_data['Country'].replace('Taiwan*', 'Taiwan')
    recovered_data['Country'] = recovered_data['Country'].replace('Korea, South', 'Korea (South)')
    recovered_data['Country'] = recovered_data['Country'].replace('US', 'United States')
    recovered_data = recovered_data.groupby(['Country']).sum().reset_index()

    return recovered_data

# function defined for cleaning the dataset - time_series_covid19_deaths_global.csv
# FOURTH DATA FRAME(DECEASED POPULATION DATA)
@st.cache(show_spinner=False)
def deceased_clean():
    path = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    deceased_data = pd.read_csv(path)
    deceased_data = deceased_data.rename(columns={'Country/Region': 'Country'})
    deceased_data = deceased_data[(deceased_data.Country != 'Diamond Princess') & (deceased_data.Country != 'MS Zaandam')]
    deceased_data = deceased_data.reset_index(drop=True)
    deceased_data = deceased_data.drop(['Province/State','Lat', 'Long'], axis=1)
    deceased_data['Country'] = deceased_data['Country'].replace('Taiwan*', 'Taiwan')
    deceased_data['Country'] = deceased_data['Country'].replace('Korea, South', 'Korea (South)')
    deceased_data['Country'] = deceased_data['Country'].replace('US', 'United States')
    deceased_data = deceased_data.groupby(['Country']).sum().reset_index()

    return deceased_data

###### MODEL FUNCTIONS ######

# the sir model function is referred from the given site and has been modified for this application and three additional models were designed by keeping the defined sir model function as a foundational model - Refer https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/

# function defined for the SIR model differential equations
@st.cache
def sir_model(state, t, N, beta, gamma):
    S, I, R = state
    # change in S population over time
    dSdt = -beta * S * I / N
    # change in I population over time
    dIdt = beta * S * I / N - gamma * I
    # change in R population over time
    dRdt = gamma * I

    return dSdt, dIdt, dRdt

# function defined for the SIRD model differential equations
@st.cache
def sird_model(state, t, N, beta, gamma, sigma):
    S, I, R, D = state
    # change in S population over time
    dSdt = -beta * S * I / N
    # change in I population over time
    dIdt = beta * S * I / N - (gamma + sigma) * I
    # change in R population over time
    dRdt = gamma * I
    # change in D population over time
    dDdt = sigma * I

    return dSdt, dIdt, dRdt, dDdt

# function defined for the SEIR model differential equations
@st.cache
def seir_model(state, t, N, alpha, beta, gamma):
    S, E, I, R = state
    # change in S population over time
    dSdt = -beta * S * I / N
    # change in E population over Time
    dEdt = beta * S * I / N - alpha * E
    # change in I population over time
    dIdt = alpha * E - gamma * I
    # change in R population over time
    dRdt = gamma * I

    return dSdt, dEdt, dIdt, dRdt

# function defined for the SEIR model(mitigation) differential equations
@st.cache
def seirm_model(state, t, u, N, alpha, beta, gamma):
    S, E, I, R = state
    # a mitigation factor 'u' is introduced and has been discussed in the main python file
    # change in S population over time
    dSdt = -(1-u) * beta * S * I / N
    # change in E population over Time
    dEdt = (1-u) * beta * S * I / N - alpha * E
    # change in I population over time
    dIdt = alpha * E - gamma * I
    # change in R population over time
    dRdt = gamma * I

    return dSdt, dEdt, dIdt, dRdt

# function defined to calculate the model generated plot's 'y' values based on the population values therfore the graph adjusts to the population values entered
@st.cache
def pop_value(p):
    y = (p/1000) + 0.2

    return y

# function defined to calculate the basic reproduction ratio
@st.cache
def brr(contact, recovery):
    ratio = contact / recovery

    return ratio

# function defined to calculate the effective contact rate by providing a fixed 5 percent transmission rate times the number of contacts
@st.cache
def eff_contact(eff):
    rate = (5/100) * eff

    return rate

# population data is taken from the following site and has been manually entered and later added to the country data frame through following defined function - Refer https://www.worldometers.info/world-population/population-by-country/ 
@st.cache
def population_list():
    population = {38928346: "Afghanistan",2877797:"Albania",43851044:"Algeria",77265:"Andorra",32866272:"Angola",97929:"Antigua and Barbuda",45195774:"Argentina",2963243:"Armenia", 25499884:"Australia",9006398:"Austria",10139177:"Azerbaijan",393244:"Bahamas",1701575:"Bahrain",164689383:"Bangladesh",287375:"Barbados",9449323:"Belarus",11589623:"Belgium",397628:"Belize",12123200:"Benin",771608:"Bhutan",11673021:"Bolivia",3280819:"Bosnia and Herzegovina",2351627:"Botswana",212559417:"Brazil",437479:"Brunei",6948445:"Bulgaria",20903273:"Burkina Faso",54409800:"Burma",1189784:"Burundi",555987:"Cabo Verde",16718965:"Cambodia",26545863:"Cameroon",37742154:"Canada",4829767:"Central African Republic",16425864:"Chad",19116201:"Chile",1439323776:"China",50882891:"Colombia",869601:"Comoros",5380508:"Congo (Brazzaville)",86790567:"Congo (Kinshasa)",5094118:"Costa Rica",26378274:"Cote d'Ivoire",4105267:"Croatia",11326616:"Cuba",1207359:"Cyprus",10708981:"Czechia",5792202:"Denmark",988000:"Djibouti",71986:"Dominica",10847910:"Dominican Republic",17643054:"Ecuador",102334404:"Egypt",6486205:"El Salvador",1402985:"Equatorial Guinea",3546421:"Eritrea",1326535:"Estonia",1160164:"Eswatini",114963588:"Ethiopia",896445:"Fiji",5540720:"Finland",65273511:"France",2225734:"Gabon",2416668:"Gambia",3989167:"Georgia",83783942:"Germany",31072940:"Ghana",10423054:"Greece",112523:"Grenada",17915568:"Guatemala",13132795:"Guinea",1968001:"Guinea-Bissau",786552:"Guyana",11402528:"Haiti",801:"Holy See",9904607:"Honduras",9660351:"Hungary",341243:"Iceland",1380004385:"India",273523615:"Indonesia",83992949:"Iran",40222493:"Iraq",4937786:"Ireland",8655535:"Israel",60461826:"Italy",2961167:"Jamaica",126476461:"Japan",10203134:"Jordan",18776707:"Kazakhstan",53771296:"Kenya",51269185:"Korea, South",1767881:"Kosovo",4270571:"Kuwait",6524195:"Kyrgyzstan",7275560:"Laos",1886198:"Latvia",6825445:"Lebanon",2142249:"Lesotho",5057681:"Liberia",6871292:"Libya",38128:"Liechtenstein",2722289:"Lithuania",625978:"Luxembourg",27691018:"Madagascar",19129952:"Malawi",32365999:"Malaysia",540544:"Maldives",20250833:"Mali",441543:"Malta",59190:"Marshall Islands",4649658:"Mauritania",1271768:"Mauritius",128932753:"Mexico",548914:"Micronesia",4033963:"Moldova",39242:"Monaco",3278290:"Mongolia",628066:"Montenegro",36910560:"Morocco",31255435:"Mozambique",2540905:"Namibia",29136808:"Nepal",17134872:"Netherlands",4822233:"New Zealand",6624554:"Nicaragua",24206644:"Niger",206139589:"Nigeria",2083374:"North Macedonia",5421241:"Norway",5106626:"Oman",220892340:"Pakistan",4314767:"Panama",8947024:"Papua New Guinea",7132538:"Paraguay",32971854:"Peru",109581078:"Philippines",37846611:"Poland",10196709:"Portugal",2881053:"Qatar",19237691:"Romania",145934462:"Russia",12952218:"Rwanda",53199:"Saint Kitts and Nevis",183627:"Saint Lucia",110940:"Saint Vincent and the Grenadines",198414:"Samoa",33931:"San Marino",219159:"Sao Tome and Principe",34813871:"Saudi Arabia",16743927:"Senegal",8737371:"Serbia",98347:"Seychelles",7976983:"Sierra Leone",5850342:"Singapore",5459642:"Slovakia",2078938:"Slovenia",686884:"Solomon Islands",15893222:"Somalia",59308690:"South Africa",11193725:"South Sudan",46754778:"Spain",21413249:"Sri Lanka",43849260:"Sudan",586632:"Suriname",10099265:"Sweden",8654622:"Switzerland",17500658:"Syria",23816775:"Taiwan*",9537645:"Tajikistan",59734218:"Tanzania",69799978:"Thailand",1318445:"Timor-Leste",8278724:"Togo",1399488:"Trinidad and Tobago",11818619:"Tunisia",84339067:"Turkey",331002651:"US",45741007:"Uganda",43733762:"Ukraine",9890402:"United Arab Emirates",67886011:"United Kingdom",3473730:"Uruguay",33469203:"Uzbekistan",30145:"Vanuatu",28435940:"Venezuela",97338579:"Vietnam",5101414:"West Bank and Gaza",29825964:"Yemen",18383955:"Zambia",14862924:"Zimbabwe"}

    return population


