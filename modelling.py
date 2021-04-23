# this python file consists of all the functions required by the main python file to function

# the main python file - epidemicModelling.py

# @st.cache has been used in most of the functions to optimise performance by enhancing function executions and is extremely useful when dealing with data loading from the web and manipulation of large datasets - Refer https://docs.streamlit.io/en/0.80.0/caching.html

###### NECESSARY IMPORTS ######
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import time
from population import Population_Data # importing population data

# assigning class to a variable
global population_data
population_data = Population_Data

class Modelling: 

    # function defined for sidebar menu animation
    @staticmethod
    @st.cache(show_spinner = False)
    def sidebar_lottie(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None

        return r.json()

    # function defined for main intro page animation
    @staticmethod
    @st.cache(show_spinner = False)
    def intro_lottie(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None

        return r.json()

    ###### DATA CLEANING ######
    # information about the datasets have been provided in the main python file


    # function defined for cleaning the dataset - cases_country.csv
    # FIRST DATA FRAME(COUNTRY DATA)
    @staticmethod
    #@st.cache(show_spinner = False, ttl = 60)
    def country_clean():
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv'
        country_content = requests.get(url).content
        country_data = pd.read_csv(io.StringIO(country_content.decode('utf-8')))
        country_data = country_data.rename(columns={'Country_Region': 'Country', 'Long_': 'lon', 'Lat': 'lat'})
        country_data = country_data[(country_data.Country != 'Diamond Princess') & (country_data.Country != 'MS Zaandam')]
        country_data = country_data.reset_index(drop=True)
        country_data['Population'] = population_data.population_list()
        country_data[['lon', 'lat']] = country_data[['lon', 'lat']].apply(pd.to_numeric)
        country_data = country_data.fillna(0)
        country_data['Country'] = country_data['Country'].replace('Korea, South', 'Korea (South)')
        country_data['Country'] = country_data['Country'].replace('Taiwan*', 'Taiwan')
        country_data['Country'] = country_data['Country'].replace('US', 'United States')

        return country_data

    # function defined for cleaning the dataset - time_series_covid19_confirmed_global.csv
    # SECOND DATA FRAME(INFECTED POPULATION DATA)
    @staticmethod
    #@st.cache(show_spinner = False, ttl = 60)
    def infected_clean():
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        infected_content = requests.get(url).content
        infected_data = pd.read_csv(io.StringIO(infected_content.decode('utf-8')))
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
    @staticmethod
    #@st.cache(show_spinner = False, ttl = 60)
    def recovered_clean():
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
        recovered_content = requests.get(url).content
        recovered_data = pd.read_csv(io.StringIO(recovered_content.decode('utf-8')))
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
    @staticmethod
    #@st.cache(show_spinner = False, ttl = 60)
    def deceased_clean():
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        deceased_content = requests.get(url).content
        deceased_data = pd.read_csv(io.StringIO(deceased_content.decode('utf-8')))
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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
    @st.cache
    def pop_value(p):
        y = (p/1000) + 0.2

        return y

    # function defined to calculate the basic reproduction ratio
    @staticmethod
    @st.cache
    def brr(contact, recovery):
        ratio = contact / recovery

        return ratio

    # function defined to calculate the effective contact rate by providing a fixed 5 percent transmission rate times the number of contacts
    @staticmethod
    @st.cache
    def eff_contact(eff):
        rate = (5/100) * eff

        return rate




