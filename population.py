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

        # removing unnecessary countries
        country_population_data = country_population_data[(country_population_data.Country != 'American Samoa') 
        & (country_population_data.Country != 'Anguilla') 
        & (country_population_data.Country != 'Aruba') 
        & (country_population_data.Country != 'Bermuda') 
        & (country_population_data.Country != 'British Virgin Islands') 
        & (country_population_data.Country != 'Caribbean Netherlands') 
        & (country_population_data.Country != 'Cayman Islands') 
        & (country_population_data.Country != 'Channel Islands')
        & (country_population_data.Country != 'Cook Islands') 
        & (country_population_data.Country != 'Curaçao') 
        & (country_population_data.Country != 'DR Congo') 
        & (country_population_data.Country != 'Faeroe Islands') 
        & (country_population_data.Country != 'Falkland Islands') 
        & (country_population_data.Country != 'French Guiana')
        & (country_population_data.Country != 'French Polynesia') 
        & (country_population_data.Country != 'Gibraltar') 
        & (country_population_data.Country != 'Greenland') 
        & (country_population_data.Country != 'Guadeloupe') 
        & (country_population_data.Country != 'Guam') 
        & (country_population_data.Country != 'Hong Kong') 
        & (country_population_data.Country != 'Isle of Man') 
        & (country_population_data.Country != 'Macao') 
        & (country_population_data.Country != 'Martinique') 
        & (country_population_data.Country != 'Mayotte') 
        & (country_population_data.Country != 'Montserrat') 
        & (country_population_data.Country != 'Myanmar') 
        & (country_population_data.Country != 'Nauru') 
        & (country_population_data.Country != 'New Caledonia') 
        & (country_population_data.Country != 'Niue') 
        & (country_population_data.Country != 'North Korea') 
        & (country_population_data.Country != 'Northern Mariana Islands') 
        & (country_population_data.Country != 'Puerto Rico') 
        & (country_population_data.Country != 'Réunion') 
        & (country_population_data.Country != 'Saint Barthelemy') 
        & (country_population_data.Country != 'Saint Helena') 
        & (country_population_data.Country != 'Saint Martin') 
        & (country_population_data.Country != 'Saint Pierre & Miquelon') 
        & (country_population_data.Country != 'Sint Maarten') 
        & (country_population_data.Country != 'Tokelau')
        & (country_population_data.Country != 'Tonga')
        & (country_population_data.Country != 'Turkmenistan')
        & (country_population_data.Country != 'Turks and Caicos')
        & (country_population_data.Country != 'Tuvalu')
        & (country_population_data.Country != 'U.S. Virgin Islands')
        & (country_population_data.Country != 'Wallis & Futuna')
        & (country_population_data.Country != 'Western Sahara')]

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
