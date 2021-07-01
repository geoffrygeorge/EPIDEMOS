# population data is taken from the following site - Refer https://www.worldometers.info/world-population/population-by-country/ 
    
###### NECESSARY IMPORTS ######
import requests
import pandas as pd
import streamlit as st

class Population_Data:

    @staticmethod
    @st.cache(show_spinner = False)
    def population_list():
 
        url = 'https://www.worldometers.info/world-population/population-by-country/'
        page = requests.get(url)
        #s = page.status_code
        tables = pd.read_html(page.text)
        country_population_data = tables[0]
        country_population_data.drop(['#'], axis = 1, inplace = True)
        country_population_data.drop(country_population_data.loc[:, 'Yearly Change': 'World Share'].columns, axis = 1, inplace = True)
        country_population_data = country_population_data.rename(columns={'Country (or dependency)': 'Country', 'Population (2020)': 'Population'})

        # adding unnecessary countries
        country_list = [
            'American Samoa', 
            'Anguilla', 
            'Aruba', 
            'Bermuda', 
            'British Virgin Islands', 
            'Caribbean Netherlands', 
            'Cayman Islands', 
            'Channel Islands', 
            'Cook Islands', 
            'Curaçao', 
            'DR Congo', 
            'Faeroe Islands', 
            'Falkland Islands', 
            'French Guiana', 
            'French Polynesia', 
            'Gibraltar', 
            'Greenland', 
            'Guadeloupe', 
            'Guam', 
            'Hong Kong', 
            'Isle of Man', 
            'Macao', 
            'Martinique', 
            'Mayotte', 
            'Montserrat', 
            'Myanmar', 
            'Nauru', 
            'New Caledonia', 
            'Niue', 
            'North Korea', 
            'Northern Mariana Islands', 
            'Puerto Rico', 
            'Réunion', 
            'Saint Barthelemy', 
            'Saint Helena', 
            'Saint Martin', 
            'Saint Pierre & Miquelon', 
            'Sint Maarten', 
            'Tokelau', 
            'Tonga', 
            'Turkmenistan', 
            'Turks and Caicos', 
            'Tuvalu', 
            'U.S. Virgin Islands', 
            'Wallis & Futuna', 
            'Western Sahara'
            ]     

        # loop to remove the above mentioned countries
        i = 0
        while i < len(country_list):
            country_population_data = country_population_data[(country_population_data.Country != country_list[i])]
            i += 1

        # renaming countries
        country_population_data["Country"] = country_population_data["Country"].replace(
            {"Côte d'Ivoire" : "Cote d'Ivoire", 
            "South Korea" : "Korea (South)", 
            "State of Palestine" : "West Bank and Gaza",
            "St. Vincent & Grenadines" : "Saint Vincent and the Grenadines",
            "US" : "United States",
            "Congo" : "Congo (Brazzaville)",
            "Czech Republic (Czechia)" : "Czechia",
            "Saint Kitts & Nevis" : "Saint Kitts and Nevis",
            "Sao Tome & Principe" : "Sao Tome and Principe"}
            )

        # adding missing countries
        dict = {'Country': ['Burma', 'Kosovo', 'Congo (Kinshasa)'],
                'Population': [54409800, 1767881, 86790567]
                }

        new_countries = pd.DataFrame(dict)
        country_population_data = pd.concat([country_population_data, new_countries], ignore_index = True)
        country_population_data.sort_values(by = ['Country'], inplace=True)
        country_population_data = country_population_data.reset_index(drop=True)

        # selecting only population values
        country_population_data = country_population_data['Population']

        return country_population_data
