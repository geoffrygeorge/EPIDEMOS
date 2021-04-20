###### EPIDEMOS - EPIDEMIC MODELLING APPLICATION CREATED USING STREAMLIT ######

# set Word Wrap to 'On' to view the script easily
 
# streamlit enables rapid prototyping of custom web applications for datascience including but not limited to incorporating machine learning models

# using command prompt or terminal run "streamlit run epidemicModelling.py" from the same directory 

# all the required streamlit commands are referred from the official documentation - https://docs.streamlit.io/en/stable/

# NECESSARY IMPORTS 
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None # see below
import numpy as np
import time
from scipy.integrate import odeint
from streamlit_lottie import st_lottie # see below
import plotly.express as px # see below
import pydeck as pdk
import matplotlib
matplotlib.use("agg") # see below
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg 
_lock = RendererAgg.lock # see below
from modelling import Modelling # importing all functions

# assigning class to a variable
model_func = Modelling

###### IMPORTANT INFORMATION ######

# lottie animations are taken from https://lottiefiles.com/ - Refer https://pypi.org/project/streamlit-lottie/

# https://matplotlib.org/stable/tutorials/introductory/usage.html - the documentation recommends to use a non-interactive "Agg" backend which is a thread-safe backend - Refer https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads 

# https://docs.streamlit.io/en/stable/deploy_streamlit_app.html - according to the documentation, it is recommended to use the class-level lock in the backend "Agg" due to the limited multi-threading support in matplotlib, this is also useful deploying the application. Refer https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server (old documentation), Also Refer - https://matplotlib.org/stable/faq/howto_faq.html (new documentation)

# there are sections in this source code where "unsafe_allow_html = True" has been used. By default, HTML tags will be treated as pure text in streamlit but this can be unlocked by introducing the command stated above therefore allowing custom HTML and CSS scripts. Refer https://docs.streamlit.io/en/stable/api.html#display-text

# equations of various models are produced using TeX functions. Refer - https://katex.org/docs/supported.html

# all model based plots are generated using matplotlib and various axes were added accordingly to suit the final plot of each model - Refer https://matplotlib.org/

# all covid-19 dashboard based plots, except for the world map, are generated using plotly express - Refer https://plotly.com/python/bar-charts/

# emojis are used as icons in the application(only streamlit supported emojis will work) - Refer https://emojipedia.org/

# datasets are used from the github data repository for the 2019 Novel Coronavirus provided by Johns Hopkins University Center for Systems Science and Engineering(https://systems.jhu.edu/). The datasets used are not stored locally but rather taken directly from the repository's raw site(all the raw sites which holds the csv files are used in the 'modelling.py' python file wherein all the datasets have been explored and cleaned for optimum use with the application) which holds all the csv files therefore all automated updates for the data are directly reflected in the application itself as the source code is written to be suited to the regular automated updates - Refer https://github.com/CSSEGISandData/COVID-19/tree/web-data and https://github.com/CSSEGISandData/COVID-19

# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html?highlight=chained_assignment - according to the documentation provided by pandas, chained assignment is not recommended but for this application chained assignment has been used to work efficiently and reduce additional code, '.loc' property is used to access labels in specific dataframes and then assigned to respective variables in the same line, for example in lines such as 350 and similar. The execution is flawless and the application is working as desired but pandas was not able to recognize this and threw 'SettingWithCopyWarning' in the terminal. Therefore in order to suppress this warning, the option is defined above after importing pandas.


###### SCRIPT BEGINS FOLLOWING NECESSARY IMPORTS ######

# INITIAL PAGE LAYOUT SETTINGS
st.set_page_config(
        page_title = "EPIDEMOS - An Epidemic Modelling Application",
        page_icon = ":globe_with_meridians:",
        initial_sidebar_state = "collapsed",
        layout = "centered"
        )


# lottie animation for the sidebar menu
with st.sidebar.beta_container():

    lottie_url = "https://assets3.lottiefiles.com/packages/lf20_lywlupuu.json"
    lottie_sidebar = model_func.sidebar_lottie(lottie_url)
    st_lottie(lottie_sidebar, height = 60)


st.sidebar.title("NAVIGATION")

# defining various pages in the application
main_menu = ['INTRO', 'SIR MODEL', 'SIR-D MODEL', 'SEIR MODEL', 'SEIR MODEL(MITIGATION)', 'COVID-19 DASHBOARD']

with st.beta_container():

    menu = st.sidebar.selectbox('Go to', main_menu) 





#### INTRO ####
if menu == "INTRO":

        st.markdown("""

        <style>
        .big-font {
            text-align: center;
            padding-top: 20px;
            font-size:80px;
            font-family: "Times New Roman", Times, serif;
        }
        </style>
        """, unsafe_allow_html = True)

        st.markdown('<p class="big-font">EPIDEMOS</p>', unsafe_allow_html = True)
        st.markdown("<p style = 'text-align: center'>AN INTERACTIVE APPLICATION FOR MODELLING EPIDEMICS</p>", unsafe_allow_html = True)

        with st.beta_container():

            # lottie animation for the main intro page
            lottie_url = "https://assets3.lottiefiles.com/packages/lf20_CXxysN.json"
            lottie_corona = model_func.intro_lottie(lottie_url)
            st_lottie(lottie_corona)





#### SIR MODEL ####
elif menu == "SIR MODEL":
    
    st.title('SIR MODEL')
    st.subheader('(S)usceptible - (I)nfected - (R)ecovered')

    # about SIR model
    sir_help = st.beta_expander('About SIR Model ❓')

    with sir_help:

        # tex functions are used to formulate equations for the respective model
        st.markdown("<p style = 'text-align: justify'>The SIR model is a simple mathematical description of the spread of a disease in a population. It is a deterministic compartment model for the spread of an infectious disease. </p>", unsafe_allow_html = True)

        st.markdown('In this model, a population of ***N*** individuals are divided into three "compartments" which may vary as a function of time, ***t***:')

        st.markdown('♦️ **Susceptible, S(t):** The subpopulation that is susceptible but not yet infected with the disease.')
        
        st.markdown('♦️ **Infectious, I(t):** The subpopulation that has become infective.')

        st.markdown('♦️ **Recovered, R(t):** The subpopulation that has recovered from infection and presumed to be no longer susceptible to the disease.')

        st.markdown('The compartment model can be diagrammed as follows:')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.latex(r'''\Large Susceptible \enspace \underrightarrow {\large \frac {\beta\it S\it I}{\it N}}\enspace \Large Infectious \enspace \underrightarrow{\large \gamma\it I} \enspace Recovered''')

        st.markdown("<p></p>", unsafe_allow_html = True)
        
        st.markdown('The rate processes are modelled as follows:')

        st.markdown(r'▪️ ${\Large \frac {\beta\it S\it I}{\it N}}$ is the rate at which the susceptible population encounters the infected population resulting in transmission of the disease.')

        st.markdown(r'▪️ ${\large \gamma\it I}$ is the rate at which the infected population recovers and becomes resistant to further infection.')

        st.markdown("<p style = 'text-align: justify'>A model for the spread of an infectious disease in a uniform population is given by the deterministic SIR equations.</p>" , unsafe_allow_html = True)
        
        st.latex(r'''\large {\frac {\it dS}{\it dt} = - \frac{\beta\it S\it I}{\it N}}''')

        st.latex(r'''\large {\frac {\it dI}{\it dt} = \frac{\beta\it S\it I}{\it N} - \gamma\it I}''')

        st.latex(r'''\large {\frac {\it dR}{\it dt} = \gamma\it I}''')

        st.markdown('Furthermore, we can define as follows:')

        st.latex(r'''\large {\it s = \frac {\it S}{\it N} \qquad \it i = \frac {\it I}{\it N} \qquad \it r = \frac {\it R}{\it N}}''')

        st.markdown('After substitution, this results in a system of three equations:')

        st.latex(r'''\large {\frac {\it ds}{\it dt} = - \beta\it s\it i}''')

        st.latex(r'''\large {\frac {\it di}{\it dt} = \beta\it s\it i - \gamma\it i}''')

        st.latex(r'''\large {\frac {\it dr}{\it dt} = \gamma\it i}''')

    # setting up controls for the SIR model
    with st.sidebar.beta_container():

        st.title('PARAMETER CONTROLS')

        pop = st.number_input('Total Population Value',
                                min_value = 1000,
                                step = 1000,
                                key = 'sir_p')

        sir_info = st.beta_expander('Note ✒️')

        with sir_info:

            st.markdown('⚠️Population values entered below must be less than the value of total population entered')

        infec = st.number_input('Infected Population Value',
                                min_value = 1,
                                value = 1, 
                                step = 1,
                                key = 'sir_i')
        
        if infec >= pop:
            with st.spinner('The infected population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        recov = st.number_input('Recovered Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'sir_r')
        
        if recov >= pop:
            with st.spinner('The recovered population values cannot be greater than or equal to the total population'):
                time.sleep(4)
        
        sir_slider = st.beta_expander('Note ✒️')

        with sir_slider:

            st.markdown(r'The controls below provide accessibility to the important parameters: number of days, beta($\beta$) and gamma($\gamma$)')

            st.markdown('▶ Number of days describes the time period')

            st.markdown(r'▶ beta($\beta$) denotes the effective contact rate of the disease, that is, number of contacts per day')

            st.markdown(r'▶ gamma($\gamma$) denotes the mean recovery rate in a given period of time, that is, mean period of time')

        day_value = st.slider('Number of days',
                                min_value = 100,
                                max_value = 730,
                                value = 150,
                                step = 10,
                                help='2 years in total',
                                key='sir')        
   

        eff_con = st.slider('Contact Rate(beta)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 4, 
                                step = 1,
                                help='Select the number of contacts(per day)',
                                key='sir')

        # beta
        contact_rate = model_func.eff_contact(eff_con)

        rec = st.slider('Recovery Rate(gamma)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 10, 
                                step = 1,
                                help='Select the number of days(mean recovery rate = 1/number of days',
                                key='sir')

        # gamma
        recovery_rate = 1/rec


        # total population
        total_pop = pop
        # number of infected people initialised
        infected = infec
        # number of recovered people initialised
        recovered = recov
        # people apart from the infected and recovered
        susceptible = total_pop - infected - recovered
        # grid of time points (in days)
        t = np.linspace(0, day_value, day_value)
        # list of days
        days = range(0, day_value)


        # calculating the basic reproduction ratio of SIR model
        sir_r = st.beta_expander('Basic Reproduction Ratio')

        with sir_r:
            
            st.markdown(r'$\it R_{0} = \Large {\frac {\beta}{\gamma}}$, is the "Basic Reproduction Number" that describes the transmissability or contagiousness of an infectious disease')

            st.markdown(u'▶ If R\u2080 > 1, the infectious population will increase')

            st.markdown(u'▶ If R\u2080 = 1, then transmission of the disease may occur but will be confined in a group of susceptible people or a particular location following a rate of consistency, meaning the disease is at an endemic stage')

            st.markdown(u'▶ If R\u2080 < 1, the infectious population will decrease')

            r_sir = model_func.brr(contact_rate,recovery_rate)
            st.info(u"The R\u2080 value of the current SIR Model is, {:.2f}".format(r_sir))

    
        # calculation of differential equations
        ret = odeint(model_func.sir_model,
                    [susceptible, infected, recovered], days,
                    args = (total_pop, contact_rate, recovery_rate))
        S, I, R = ret.T

        # plotting the results 
        value = model_func.pop_value(pop)

        with _lock:
            sir_fig = Figure()
            ax = sir_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
            ax.plot(t, S/1000, 'k', alpha=1, lw=2, ls='-', label='Susceptible')
            ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls=':', label='Infected')
            ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered')
            ax.set_title(label='SIR PLOT', loc='center', pad=15.0, fontsize=25)
            ax.set_xlabel('Time in days')
            ax.set_ylabel('Population in 1000s')
            ax.set_ylim(0,value)
            ax.minorticks_on()
            ax.tick_params(axis='x', which='minor')
            ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
            sir_fig.patch.set_facecolor('w')
            sir_fig.patch.set_alpha(0.7)
            ax.patch.set_edgecolor('black')
            ax.patch.set_linewidth(0.7) 
            legend = ax.legend()
            legend.get_frame().set_alpha(1.0)

    if infec < pop and recov < pop and infec + recov < pop:
        
        st.pyplot(sir_fig, clear_figure = True)

    else:

        st.error('ERROR: CANNOT DISPLAY PLOT(CHECK INFECTED AND RECOVERED POPULATION VALUES)')
    

    # covid-19 statistics comparison
    st.sidebar.markdown("<p></p>", unsafe_allow_html = True)
    container = st.sidebar.beta_container()

    container.header('COVID-19 STATISTICS COMPARISON')
    rw = container.checkbox('View 🔍', key = 'sir_cb')

    if rw:
        st.header('SIR Model Data v/s Covid-19 Data')
         
        sir_rw_help = st.beta_expander('About Covid-19 Statistics Comparison ❔')

        with sir_rw_help:

            st.markdown("<p style = 'text-align: justify'>The SIR MODEL generated plot above is based on the complete access provided to the end-user and changes according to the parameters entered or changed by the user. Comparing the covid-19 statistical data with the model generated data would provide with an interesting insight concerning theoretical and actual values.</p>", unsafe_allow_html = True)

            st.markdown("<p style = 'text-align: justify'>The plot shown below consists of model generated Infected data and its corresponding covid-19 data and a similar approach is done for the Recovered data.</p>", unsafe_allow_html = True)

        # calling the respective functions containing the final datasets and storing the returned data to respective variables  
        country_clean = model_func.country_clean()
        infected_clean = model_func.infected_clean()
        recovered_clean = model_func.recovered_clean()
        
        # creating a selectbox to choose the desired country
        country_list = container.selectbox('Choose country', country_clean['Country'].unique(), index = 180)
        population = int(country_clean["Population"].loc[country_clean["Country"] == country_list])
        st.sidebar.write('▶ The population of',country_list,'= {:,}'.format(population))

        # initial infected value for the SIR model
        infected_df = infected_clean.loc[infected_clean["Country"] == country_list]
        initial_infected = int(infected_clean["1/22/20"].loc[infected_clean["Country"] == country_list])
        initial_infected += 1 #SIR model must have infected value initialised to atleast 1
        infected_df.drop(['Country'], axis = 1, inplace = True)

        # initial recovered value for the SIR model
        recovered_df = recovered_clean.loc[recovered_clean["Country"] == country_list]
        initial_recovered = int(recovered_clean["1/22/20"].loc[recovered_clean["Country"] == country_list])
        recovered_df.drop(['Country'], axis = 1, inplace = True)

        # the number of columns are taken as day values as the datasets consists of automated daily data starting from 1/22/2020 till today as columns(automated update)
        if (len(infected_df.columns) >= len(recovered_df.columns)):
            
            day_value = len(infected_df.columns)

        st.sidebar.write('▶ The total number of days(based on actual data) = ',day_value)
        
        # the respective dataframes are transposed followed by the conversion to numpy data to be plotted later
        infected_tr = infected_df.transpose()
        recovered_tr = recovered_df.transpose()

        infected_tr = infected_tr.to_numpy()
        recovered_tr = recovered_tr.to_numpy()
    
        # setting up necessary controls
        with st.sidebar.beta_container():

            st.subheader('CONTROLS')

            eff_con = st.slider('Contact Rate(beta)', 
                                    min_value = 1, 
                                    max_value = 20,
                                    value = 5, 
                                    step = 1,
                                    help='Select the number of contacts(per day)',
                                    key = 'sir_rw1')

            # beta
            contact_rate = model_func.eff_contact(eff_con)

            rec = st.slider('Recovery Rate(gamma)', 
                                    min_value = 1, 
                                    max_value = 20,
                                    value = 5, 
                                    step = 1,
                                    help='Select the number of days(mean recovery rate = 1/number of days',
                                    key = 'sir_rw2')

            # gamma
            recovery_rate = 1/rec

            # People apart from the infected and recovered
            susceptible = population - initial_infected - initial_recovered
            # Grid of time points (in days)
            t = np.linspace(0, day_value, day_value)
            # List of days
            days = range(0, day_value)

        
            # calculation of differential equations
            ret = odeint(model_func.sir_model,
                        [susceptible, initial_infected, initial_recovered], days,
                        args = (population, contact_rate, recovery_rate))
            S, I, R = ret.T
        
            
            # plotting the results
            value = model_func.pop_value(population)

            with _lock:
                sir_rw_fig = Figure()
                ax = sir_rw_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
                ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls='--', label='Infected(Model)')
                ax.plot(t, infected_tr/1000, 'm', alpha=1, lw=3, ls='-', label='Infected(Covid-19 Data)')

                ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered(Model)')
                ax.plot(t, recovered_tr/1000, 'g', alpha=1, lw=3, ls='-', label='Recovered(Covid-19 Data)')

                ax.set_title(label='COMPARISON PLOT', loc='center', pad=15.0, fontsize=25)
                ax.set_xlabel('Time in days')
                ax.set_ylabel('Population in 1000s')
                ax.set_ylim(0,value)
                ax.minorticks_on()
                ax.tick_params(axis='x', which='minor')
                ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
                sir_rw_fig.patch.set_facecolor('w')
                sir_rw_fig.patch.set_alpha(0.7)
                legend = ax.legend()
                legend.get_frame().set_alpha(1.0)
                ax.spines['bottom'].set_visible(False)

        with st.beta_container():

            st.pyplot(sir_rw_fig, clear_figure = True)

        data_frame_sir = st.beta_expander('View Covid-19 Statistical Data 📊')

        with data_frame_sir:
            st.subheader('Country Population Data')
            st.write(country_clean)
            st.subheader('Infected Population Data')
            st.write(infected_clean)
            st.subheader('Recovered Population Data')
            st.write(recovered_clean)            





#### SIRD MODEL ####
elif menu == "SIR-D MODEL":
    
    st.title('SIR-D MODEL')
    st.subheader('(S)usceptible - (I)nfected - (R)ecovered - (D)eceased')

    # about SIRD model
    sird_help = st.beta_expander('About SIR-D Model ❓')

    with sird_help:

        # tex functions are used to formulate equations for the respective model
        st.markdown("<p style = 'text-align: justify'>This SIR model will have an additional compartment called 'Deceased' which will denote the population that was not able to survive the epidemic. </p>", unsafe_allow_html = True)

        st.markdown('In this model, a population of ***N*** individuals are divided into four "compartments" which may vary as a function of time, ***t***:')

        st.markdown('♦️ **Susceptible, S(t):** The subpopulation that is susceptible but not yet infected with the disease.')
        
        st.markdown('♦️ **Infectious, I(t):** The subpopulation that has become infective.')

        st.markdown('♦️ **Recovered, R(t):** The subpopulation that has recovered from infection and presumed to be no longer susceptible to the disease.')

        st.markdown('♦️ **Deceased, D(t):** The subpopulation that has not recovered from infection and presumed to be deceased.')

        st.markdown('The compartment model can be diagrammed as follows:')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.latex(r'''\Large Susceptible \enspace \underrightarrow {\large \frac {\beta\it S\it I}{\it N}}\enspace \Large Infectious \enspace \underrightarrow{\large \gamma\it I} \enspace Recovered \enspace \underrightarrow{\large \sigma\it I} \enspace Deceased''')

        st.markdown("<p></p>", unsafe_allow_html = True)
        
        st.markdown('The rate processes are modelled as follows:')

        st.markdown(r'▪️ ${\Large \frac {\beta\it S\it I}{\it N}}$ is the rate at which the susceptible population encounters the infected population resulting in transmission of the disease.')

        st.markdown(r'▪️ ${\large \gamma\it I}$ is the rate at which the infected population recovers and becomes resistant to further infection.')

        st.markdown(r'▪️ ${\large \sigma\it I}$ is the rate at which the infected population is not able to reach the recovered stage and are deceased.')

        st.markdown("<p style = 'text-align: justify'>A model for the spread of an infectious disease in a uniform population is given by the deterministic SIR-D equations.</p>" , unsafe_allow_html = True)
        
        st.latex(r'''\large {\frac {\it dS}{\it dt} = - \frac{\beta\it S\it I}{\it N}}''')

        st.latex(r'''\large {\frac {\it dI}{\it dt} = \frac{\beta\it S\it I}{\it N} - \gamma\it I}''')

        st.latex(r'''\large {\frac {\it dR}{\it dt} = \gamma\it I}''')

        st.latex(r'''\large {\frac {\it dD}{\it dt} = \sigma\it I}''')

        st.markdown('Furthermore, we can define as follows:')

        st.latex(r'''\large {\it s = \frac {\it S}{\it N} \qquad \it i = \frac {\it I}{\it N} \qquad \it r = \frac {\it R}{\it N} \qquad \it d = \frac {\it D}{\it N}} ''')

        st.markdown('After substitution, this results in a system of four equations:')

        st.latex(r'''\large {\frac {\it ds}{\it dt} = - \beta\it s\it i}''')

        st.latex(r'''\large {\frac {\it di}{\it dt} = \beta\it s\it i - \gamma\it i}''')

        st.latex(r'''\large {\frac {\it dr}{\it dt} = \gamma\it i}''')

        st.latex(r'''\large {\frac {\it dd}{\it dt} = \sigma\it i}''')

    # setting up controls for the SIR-D model
    with st.sidebar.beta_container():

        st.title('PARAMETER CONTROLS')


        pop = st.number_input('Total Population Value',
                                min_value = 1000,
                                step = 1000,
                                key = 'sird_p')

        sird_info = st.beta_expander('Note ✒️')

        with sird_info:

            st.markdown('⚠️Population values entered below must be less than the value of total population entered')

        infec = st.number_input('Infected Population Value',
                                min_value = 1,
                                value = 1, 
                                step = 1,
                                key = 'sird_i')
        
        if infec >= pop:
            with st.spinner('The infected population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        recov = st.number_input('Recovered Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'sird_r')
        
        if recov >= pop:
            with st.spinner('The recovered population values cannot be greater than or equal to the total population'):
                time.sleep(4)
        
        deceas = st.number_input('Deceased Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'sird_d')
        
        if deceas >= pop:
            with st.spinner('The deceased population values cannot be greater than or equal to the total population'):
                time.sleep(4)
        
        sird_slider = st.beta_expander('Note ✒️')

        with sird_slider:

            st.markdown(r'The controls below provide accessibility to the important parameters: number of days, beta($\beta$) and gamma($\gamma$)')

            st.markdown('▶ Number of days describes the time period')

            st.markdown(r'▶ beta($\beta$) denotes the effective contact rate of the disease, that is, number of contacts per day')

            st.markdown(r'▶ gamma($\gamma$) denotes the mean recovery rate in a given period of time, that is, mean period of time')

            st.markdown(r'▶ sigma($\sigma$) denotes the mean deceased rate in a given period of time, that is, mean period of time')


        day_value = st.slider('Number of days',
                                min_value = 100,
                                max_value = 730,
                                value = 150,
                                step = 10,
                                help='2 years in total',
                                key='sird')        
   

        eff_con = st.slider('Contact Rate(beta)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 10, 
                                step = 1,
                                help='Select the number of contacts(per day)',
                                key='sird')

        # beta
        contact_rate = model_func.eff_contact(eff_con)

        rec = st.slider('Recovery Rate(gamma)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 6, 
                                step = 1,
                                help='Select the number of days(mean recovery rate = 1/number of days',
                                key='sird')

        # gamma
        recovery_rate = 1/rec

        dec = st.slider('Deceased Rate(sigma)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 10, 
                                step = 1,
                                help='Select the number of days(mean deceased rate = 1/number of days',
                                key='sird')

        # sigma
        deceased_rate = 1/dec


        # notal population
        total_pop = pop
        # number of infected people initialised
        infected = infec
        # nmber of recovered people initialised
        recovered = recov
        # number of deceased people initialised
        deceased = deceas
        # people apart from the infected and recovered
        susceptible = total_pop - infected - recovered - deceased
        # grid of time points (in days)
        t = np.linspace(0, day_value, day_value)
        # list of days
        days = range(0, day_value)


        # calculating the basic reproduction ratio of SIRD model
        sird_r = st.beta_expander('Basic Reproduction Ratio')

        with sird_r:
            
            st.markdown(r'$\it R_{0} = \Large {\frac {\beta}{\gamma}}$, is the "Basic Reproduction Number" that describes the transmissability or contagiousness of an infectious disease')

            st.markdown(u'▶ If R\u2080 > 1, the infectious population will increase')

            st.markdown(u'▶ If R\u2080 = 1, then transmission of the disease may occur but will be confined in a group of susceptible people or a particular location following a rate of consistency, meaning the disease is at an endemic stage')

            st.markdown(u'▶ If R\u2080 < 1, the infectious population will decrease')

            r_sird = model_func.brr(contact_rate,recovery_rate)
            st.info(u"The R\u2080 value of the current SIR-D Model is, {:.2f}".format(r_sird))
    
        # calculation of differential equations
        ret = odeint(model_func.sird_model,
                    [susceptible, infected, recovered, deceased], days,
                    args = (total_pop, contact_rate, recovery_rate, deceased_rate))
        S, I, R, D = ret.T

        # plotting the results  
        value = model_func.pop_value(pop)

        with _lock:
            sird_fig = Figure()
            ax = sird_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
            ax.plot(t, S/1000, 'k', alpha=1, lw=2, ls='-', label='Susceptible')
            ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls=':', label='Infected')
            ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered')
            ax.plot(t, D/1000, '#9A7B4F', alpha=1, lw=2, ls='-.', label='Deceased')
            ax.set_title(label='SIR-D PLOT', loc='center', pad=15.0, fontsize=25)
            ax.set_xlabel('Time in days')
            ax.set_ylabel('Population in 1000s')
            ax.set_ylim(0,value)
            ax.minorticks_on()
            ax.tick_params(axis='x', which='minor')
            ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
            sird_fig.patch.set_facecolor('w')
            sird_fig.patch.set_alpha(0.7)
            ax.patch.set_edgecolor('black')
            ax.patch.set_linewidth(0.7) 
            legend = ax.legend()
            legend.get_frame().set_alpha(1.0)

    if infec < pop and recov < pop and deceas < pop and infec + recov + deceas < pop:
        
        st.pyplot(sird_fig, clear_figure = True)

    else:

        st.error('ERROR: CANNOT DISPLAY PLOT(CHECK INFECTED AND RECOVERED POPULATION VALUES)')


    # covid-19 statistics comparison
    st.sidebar.markdown("<p></p>", unsafe_allow_html = True)
    container = st.sidebar.beta_container()

    container.header('COVID-19 STATISTICS COMPARISON')
    rw = container.checkbox('View 🔍', key = 'sird_cb')

    if rw:
        st.header('SIR-D Model Data v/s Covid-19 Data')

        sird_rw_help = st.beta_expander('About Covid-19 Statistics Comparison ❔')

        with sird_rw_help:

            st.markdown("<p style = 'text-align: justify'>The SIR-D MODEL generated plot above is based on the complete access provided to the end-user and changes according to the parameters entered or changed by the user. Comparing the covid-19 statistical data with the model generated data would provide with an interesting insight concerning theoretical and actual values.</p>", unsafe_allow_html = True)

            st.markdown("<p style = 'text-align: justify'>The plot shown below consists of model generated Infected data and its corresponding covid-19 data and a similar approach is done for the Recovered data and the Deceased data.</p>", unsafe_allow_html = True)

        # calling the respective functions containing the final datasets and storing the returned data to respective variables  
        country_clean = model_func.country_clean()
        infected_clean = model_func.infected_clean()
        recovered_clean = model_func.recovered_clean()
        deceased_clean = model_func.deceased_clean()
        
        # creating a selectbox to choose the desired country
        country_list = container.selectbox('Choose country', country_clean['Country'].unique(), index = 180)
        population = int(country_clean["Population"].loc[country_clean["Country"] == country_list])
        st.sidebar.write('▶ The population of',country_list,'= {:,}'.format(population))

        # initial infected value for the SIR-D model
        infected_df = infected_clean.loc[infected_clean["Country"] == country_list]
        initial_infected = int(infected_clean["1/22/20"].loc[infected_clean["Country"] == country_list])
        initial_infected += 1 #SIR-D model must have infected value initialised to atleast 1
        infected_df.drop(['Country'], axis = 1, inplace = True)

        # initial recovered value for the SIR-D model
        recovered_df = recovered_clean.loc[recovered_clean["Country"] == country_list]
        initial_recovered = int(recovered_clean["1/22/20"].loc[recovered_clean["Country"] == country_list])
        recovered_df.drop(['Country'], axis = 1, inplace = True)

        #initial deceased value for the SIR-D model
        deceased_df = deceased_clean.loc[deceased_clean["Country"] == country_list]
        initial_deceased = int(deceased_clean["1/22/20"].loc[deceased_clean["Country"] == country_list])
        deceased_df.drop(['Country'], axis = 1, inplace = True)

        # the number of columns are taken as day values as the datasets consists of automated daily data starting from 1/22/2020 till today as columns(automated update)
        if (len(infected_df.columns) >= len(deceased_df.columns)):
            
            day_value = len(infected_df.columns)

        st.sidebar.write('▶ The total number of days(based on actual data) = ',day_value)

        # the respective dataframes are transposed followed by the conversion to numpy data to be plotted later
        infected_tr = infected_df.transpose()
        recovered_tr = recovered_df.transpose()
        deceased_tr = deceased_df.transpose()

        infected_tr = infected_tr.to_numpy()
        recovered_tr = recovered_tr.to_numpy()
        deceased_tr = deceased_tr.to_numpy()

        # setting up necessary controls
        with st.sidebar.beta_container():

            st.subheader('CONTROLS')

            eff_con = st.slider('Contact Rate(beta)', 
                                    min_value = 1, 
                                    max_value = 20,
                                    value = 10, 
                                    step = 1,
                                    help='Select the number of contacts(per day)',
                                    key = 'sird_rw1')

            # beta
            contact_rate = model_func.eff_contact(eff_con)

            rec = st.slider('Recovery Rate(gamma)', 
                                    min_value = 1, 
                                    max_value = 20,
                                    value = 5, 
                                    step = 1,
                                    help = 'Select the number of days(mean recovery rate = 1/number of days',
                                    key = 'sird_rw2')

            # gamma
            recovery_rate = 1/rec

            dec = st.slider('Deceased Rate(sigma)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 8, 
                                step = 1,
                                help = 'Select the number of days(mean deceased rate = 1/number of days',
                                key = 'sird_rw3')

            # sigma
            deceased_rate = 1/dec


            # People apart from the infected and recovered
            susceptible = population - initial_infected - initial_recovered - initial_deceased
            # Grid of time points (in days)
            t = np.linspace(0, day_value, day_value)
            # List of days
            days = range(0, day_value)

        
            # Use differential equations magic with our population
            ret = odeint(model_func.sird_model,
                        [susceptible, initial_infected, initial_recovered, initial_deceased], days,
                        args = (population, contact_rate, recovery_rate, deceased_rate))
            S, I, R, D = ret.T
        
            
            # plotting the results
            value = model_func.pop_value(population)

            with _lock:
                sird_rw_fig = Figure()
                ax = sird_rw_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
                ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls='--', label='Infected(Model)')
                ax.plot(t, infected_tr/1000, 'm', alpha=1, lw=3, ls='-', label='Infected(Covid-19 Data)')

                ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered(Model)')
                ax.plot(t, recovered_tr/1000, 'g', alpha=1, lw=3, ls='-', label='Recovered(Covid-19 Data)')

                ax.plot(t, D/1000, '#9A7B4F', alpha=1, lw=2, ls='--', label='Deceased(Model)')
                ax.plot(t, deceased_tr/1000, 'b', alpha=1, lw=3, ls='-', label='Deceased(Covid-19 Data)')

                ax.set_title(label='COMPARISON PLOT', loc='center', pad=15.0, fontsize=25)
                ax.set_xlabel('Time in days')
                ax.set_ylabel('Population in 1000s')
                ax.set_ylim(0,value)
                ax.minorticks_on()
                ax.tick_params(axis='x', which='minor')
                ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
                sird_rw_fig.patch.set_facecolor('w')
                sird_rw_fig.patch.set_alpha(0.7)
                legend = ax.legend()
                legend.get_frame().set_alpha(1.0)
                ax.spines['bottom'].set_visible(False)

        with st.beta_container():

            st.pyplot(sird_rw_fig, clear_figure = True)

        data_frame_sird = st.beta_expander('View Covid-19 Statistical Data 📊')

        with data_frame_sird:
            st.subheader('Country Population Data')
            st.write(country_clean)
            st.subheader('Infected Population Data')
            st.write(infected_clean)
            st.subheader('Recovered Population Data')
            st.write(recovered_clean)
            st.subheader('Deceased Population Data')
            st.write(deceased_clean)          





#### SEIR MODEL ####
elif menu == "SEIR MODEL":

    st.title('SEIR MODEL')

    st.subheader('(S)usceptible - (E)xposed - (I)nfected - (R)ecovered)')

    # about SEIR model
    seir_help = st.beta_expander('About SEIR Model ❓')

    with seir_help:
        
        # tex functions are used to formulate equations for the respective model
        st.markdown("<p style = 'text-align: justify'>The SEIR model extends the SIR model by adding an additional population compartment containing those individuals who have been exposed to the virus but are not yet infective.</p>", unsafe_allow_html = True)

        st.markdown('In this model, a population of ***N*** individuals are divided into four "compartments" which may vary as a function of time, ***t***:')

        st.markdown('♦️ **Susceptible, S(t):** The subpopulation that is susceptible but not yet infected with the disease.')
        
        st.markdown('♦️ **Exposed, E(t):** The subpopulation that has been exposed to the disease but not yet infective.')

        st.markdown('♦️ **Infectious, I(t):** The subpopulation that has become infective.')

        st.markdown('♦️ **Recovered, R(t):** The subpopulation that has recovered from infection and presumed to be no longer susceptible to the disease.')

        st.markdown('The compartment model can be diagrammed as follows:')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.latex(r'''\Large Susceptible \enspace \underrightarrow {\large \frac {\beta\it S\it I}{\it N}} \enspace \Large Exposed \enspace \underrightarrow{\large \alpha\it E} \enspace \Large Infectious \enspace \underrightarrow{\large \gamma\it I} \enspace Recovered''')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.markdown('The rate processes are modelled as follows:')

        st.markdown(r'▪️ ${\Large \frac {\beta\it S\it I}{\it N}}$ is the rate at which the susceptible population encounters the infected population resulting in transmission of the disease.')

        st.markdown(r'▪️ ${\large \alpha\it E}$ is the rate at which the exposed population becomes infective.')

        st.markdown(r'▪️ ${\large \gamma\it I}$ is the rate at which the infected population recovers and becomes resistant to further infection.')

        st.markdown("<p style = 'text-align: justify'>A model for the spread of an infectious disease in a uniform population is given by the deterministic SEIR equations.</p>" , unsafe_allow_html = True)

        st.latex(r'''\large {\frac {\it dS}{\it dt} = - \frac{\beta\it S\it I}{\it N}}''')

        st.latex(r'''\large {\frac {\it dE}{\it dt} = \frac{\beta\it S\it I}{\it N} - \frac {\alpha \it E}{\it N}}''')

        st.latex(r'''\large {\frac {\it dI}{\it dt} = \frac {\alpha \it E}{\it N} - \gamma\it I}''')

        st.latex(r'''\large {\frac {\it dR}{\it dt} = \gamma\it I}''')
        
        st.markdown('Furthermore, we can define as follows:')

        st.latex(r'''\large {\it s = \frac {\it S}{\it N} \qquad \it e = \frac {\it E}{\it N} \qquad \it i = \frac {\it I}{\it N} \qquad \it r = \frac {\it R}{\it N}}''')

        st.markdown('After substitution, this results in a system of four equations:')

        st.latex(r'''\large {\frac {\it ds}{\it dt} = - \beta\it s\it i}''')

        st.latex(r'''\large {\frac {\it de}{\it dt} = \beta\it s\it i - \alpha \it e}''')

        st.latex(r'''\large {\frac {\it di}{\it dt} = \alpha \it e - \gamma\it i}''')

        st.latex(r'''\large {\frac {\it dr}{\it dt} = \gamma\it i}''')

    # setting up controls for the SEIR model
    with st.sidebar.beta_container():

        st.title('PARAMETER CONTROLS')

        pop = st.number_input('Total Population Value',
                                min_value = 1000,
                                step = 1000,
                                key = 'seir_p')

        seir_info = st.beta_expander('Note ✒️')

        with seir_info:

            st.markdown('⚠️Population values entered below must be less than the value of total population entered')

        expos = st.number_input('Exposed Population Value',
                                min_value = 1,
                                value = 1, 
                                step = 1,
                                key = 'seir_e')

        if expos >= pop:
            with st.spinner('The exposed population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        infec = st.number_input('Infected Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'seir_i')

        if infec >= pop:
            with st.spinner('The infected population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        recov = st.number_input('Recovered Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'seir_r')

        if recov >= pop:
            with st.spinner('The recovered population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        seir_slider = st.beta_expander('Note ✒️')

        with seir_slider:

            st.markdown(r'The controls below provide accessibility to the important parameters: number of days, alpha($\alpha$), beta($\beta$) and gamma($\gamma$)')

            st.markdown('▶ Number of days describes the time period')

            st.markdown(r'▶ alpha($\alpha$) denotes the mean exposed rate in a given period of time, that is, mean period of time')

            st.markdown(r'▶ beta($\beta$) denotes the effective contact rate of the disease, that is, number of contacts per day')

            st.markdown(r'▶ gamma($\gamma$) denotes the mean recovery rate in a given period of time, that is, mean period of time')

        day_value = st.slider('Number of days',
                                min_value = 100,
                                max_value = 730,
                                value = 150,
                                step = 10,
                                help = '2 years in total',
                                key='seir')
      
      
        exp_incu = st.slider('Expose Rate(alpha)', 
                                min_value = 1, 
                                max_value = 10,
                                value = 3, 
                                step = 1,
                                help = 'Select the number of days(mean expose rate = 1/number of days',
                                key='seir')
        # alpha
        expose_rate = 1/exp_incu
      
        eff_con = st.slider('Contact Rate(beta)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 10, 
                                step = 1,
                                help = 'Select the number of contacts(per day)',
                                key='seir')
        # beta
        contact_rate = model_func.eff_contact(eff_con)

        rec_infect = st.slider('Recovery Rate(gamma)', 
                                min_value = 1, 
                                max_value = 10,
                                value = 5, 
                                step = 1,
                                help = 'Select the number of days(mean recovery rate = 1/number of days',
                                key='seir')

        # gammma 
        recovery_rate = 1/rec_infect


        # total population
        total_pop = pop
        # number of exposed people initialised
        exposed = expos
        # number of infected people initialised
        infected = infec
        # number of recovered people initialised
        recovered = recov
        # people apart from the infected and recovered
        susceptible = total_pop - exposed - infected - recovered
        # grid of time points (in days)
        t = np.linspace(0, day_value, day_value)
        # list of days
        days = range(0, day_value)

        # calculating the basic reproduction ratio of SEIR model
        seir_r = st.beta_expander('Basic Reproduction Ratio')

        with seir_r:
            
            st.markdown(r'$\it R_{0} = \Large {\frac {\beta}{\gamma}}$, is the "Basic Reproduction Number" that describes the transmissability or contagiousness of an infectious disease')
            
            st.markdown(u'▶ If R\u2080 > 1, the infectious population will increase')

            st.markdown(u'▶ If R\u2080 = 1, then transmission of the disease may occur but will be confined in a group of susceptible people or a particular location following a rate of consistency, meaning the disease is at an endemic stage')

            st.markdown(u'▶ If R\u2080 < 1, the infectious population will decrease')

            r_seir = model_func.brr(contact_rate,recovery_rate)
            st.info(u"The R\u2080 value of the current SEIR Model is, {:.2f}".format(r_seir))

        # calculation of differertial equations
        ret = odeint(model_func.seir_model,
                    [susceptible, exposed, infected, recovered], days,
                    args = (total_pop, expose_rate, contact_rate, recovery_rate))
        S, E, I, R = ret.T

        # plotting the results
        value = model_func.pop_value(pop)

        with _lock:
            seir_fig = Figure()
            ax = seir_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
            ax.plot(t, S/1000, 'k', alpha=1, lw=2, ls='-', label='Susceptible')
            ax.plot(t, E/1000, '#FFCC00', alpha=1, lw=2, ls='-.', label='Exposed')
            ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls=':', label='Infected')
            ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered')
            ax.set_title(label='SEIR PLOT', loc='center', pad=15.0, fontsize=25)
            ax.set_xlabel('Time in days')
            ax.set_ylabel('Population in 1000s')
            ax.set_ylim(0,value)
            ax.minorticks_on()
            ax.tick_params(axis='x', which='minor')
            ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
            seir_fig.patch.set_facecolor('w')
            seir_fig.patch.set_alpha(0.7)
            ax.patch.set_edgecolor('black')
            ax.patch.set_linewidth(0.7) 
            legend = ax.legend()
            legend.get_frame().set_alpha(1.0)


    if expos < pop and infec < pop and recov < pop and expos + infec + recov < pop:

        st.pyplot(seir_fig, clear_figure = True)

    else:

        st.error('ERROR: CANNOT DISPLAY PLOT(CHECK INFECTED AND RECOVERED POPULATION VALUES)')





#### SEIR MODEL WITH MITIGATION CONTROL ####
elif menu == "SEIR MODEL(MITIGATION)":

    st.title('SEIR MODEL(MITIGATION)')

    st.subheader('(S)usceptible - (E)xposed - (I)nfected - (R)ecovered) with Mitigation Control')

    # about SEIR model with mitigation control
    seirm_help = st.beta_expander('About SEIR Model with Mitigation Control ❓')

    with seirm_help:
        
        # tex functions are used to formulate equations for the respective model
        st.markdown("<p style = 'text-align: justify'>This SEIR model will have a mitigation control parameter 'u' indicating the effectiveness of mitigation measures and efforts that had been undertaken to contain the disease.  u = 0  corresponds to no control,  u = 1  corresponds to perfect isolation of infective individuals. The purpose of this model is to explore how a social distancing strategy affects the outcome of an epidemic.</p>", unsafe_allow_html = True)

        st.markdown('In this model, a population of ***N*** individuals are divided into four "compartments" which may vary as a function of time, ***t***:')

        st.markdown('♦️ **Susceptible, S(t):** The subpopulation that is susceptible but not yet infected with the disease.')
        
        st.markdown('♦️ **Exposed, E(t):** The subpopulation that has been exposed to the disease but not yet infective.')

        st.markdown('♦️ **Infectious, I(t):** The subpopulation that has become infective.')

        st.markdown('♦️ **Recovered, R(t):** The subpopulation that has recovered from infection and presumed to be no longer susceptible to the disease.')

        st.markdown('The compartment model can be diagrammed as follows:')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.latex(r'''\Large Susceptible \enspace \underrightarrow {\large \frac {(1-u)\beta\it S\it I}{\it N}} \enspace \Large Exposed \enspace \underrightarrow{\large \alpha\it E} \enspace \Large Infectious \enspace \underrightarrow{\large \gamma\it I} \enspace Recovered''')

        st.markdown("<p></p>", unsafe_allow_html = True)

        st.markdown('The rate processes are modelled as follows:')

        st.markdown(r'▪️ ${\Large \frac {(1-\it u)\beta\it S\it I}{\it N}}$ is the rate at which the susceptible population encounters the infected population resulting in transmission of the disease. $\it u$ describes the effectiveness of any public health interventions to control the transmission of the disease. $\it u = 0$ means no effective public health interventions, $\it u = 1$ means the total elimination of disease transmission.')

        st.markdown(r'▪️ ${\large \alpha\it E}$ is the rate at which the exposed population becomes infective.')

        st.markdown(r'▪️ ${\large \gamma\it I}$ is the rate at which the infected population recovers and becomes resistant to further infection.')

        st.markdown("<p style = 'text-align: justify'>A model for the spread of an infectious disease in a uniform population is given by the deterministic SEIR equations with a mitigation control parameter.</p>" , unsafe_allow_html = True)

        st.latex(r'''\large {\frac {\it dS}{\it dt} = - \frac{(1- \it u)\beta\it S\it I}{\it N}}''')

        st.latex(r'''\large {\frac {\it dE}{\it dt} = \frac{(1- \it u)\beta\it S\it I}{\it N} - \frac {\alpha \it E}{\it N}}''')

        st.latex(r'''\large {\frac {\it dI}{\it dt} = \frac {\alpha \it E}{\it N} - \gamma\it I}''')

        st.latex(r'''\large {\frac {\it dR}{\it dt} = \gamma\it I}''')
        
        st.markdown('Furthermore, we can define as follows:')

        st.latex(r'''\large {\it s = \frac {\it S}{\it N} \qquad \it e = \frac {\it E}{\it N} \qquad \it i = \frac {\it I}{\it N} \qquad \it r = \frac {\it R}{\it N}}''')

        st.markdown('After substitution, this results in a system of four equations:')

        st.latex(r'''\large {\frac {\it ds}{\it dt} = - (1- \it u) \beta\it s\it i}''')

        st.latex(r'''\large {\frac {\it de}{\it dt} = (1- \it u) \beta\it s\it i - \alpha \it e}''')

        st.latex(r'''\large {\frac {\it di}{\it dt} = \alpha \it e - \gamma\it i}''')

        st.latex(r'''\large {\frac {\it dr}{\it dt} = \gamma\it i}''')

    # setting up controls for the SEIR model with mitigation
    with st.sidebar.beta_container():

        st.title('PARAMETER CONTROLS')

        pop = st.number_input('Total Population Value',
                                min_value = 1000,
                                step = 1000,
                                key = 'seir_p')

        seirm_info = st.beta_expander('Note ✒️')

        with seirm_info:

            st.markdown('⚠️Population values entered below must be less than the value of total population entered')

        expos = st.number_input('Exposed Population Value',
                                min_value = 1,
                                value = 1, 
                                step = 1,
                                key = 'seir_e')

        if expos >= pop:
            with st.spinner('The exposed population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        infec = st.number_input('Infected Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'seir_i')

        if infec >= pop:
            with st.spinner('The infected population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        recov = st.number_input('Recovered Population Value',
                                min_value = 0,
                                value = 0, 
                                step = 1,
                                key = 'seir_r')

        if recov >= pop:
            with st.spinner('The recovered population values cannot be greater than or equal to the total population'):
                time.sleep(4)

        seirm_slider = st.beta_expander('Note ✒️')

        with seirm_slider:

            st.markdown(r'The controls below provide accessibilty to the important parameters: number of days, alpha($\alpha$), beta($\beta$) and gamma($\gamma$)')

            st.markdown(r'▶ Mitigation Control($\it u$) denotes the effectiveness of control measures applied')
            
            st.markdown('▶ Number of days describes the time period')

            st.markdown(r'▶ alpha($\alpha$) denotes the mean exposed rate in a given period of time, that is, mean period of time')

            st.markdown(r'▶ beta($\beta$) denotes the effective contact rate of the disease, that is, number of contacts per day')

            st.markdown(r'▶ gamma($\gamma$) denotes the mean recovery rate in a given period of time, that is, mean period of time')

        m_control = st.slider('Mitigation Control',
                                min_value = 0.0,
                                max_value = 1.0,
                                value = 0.0,
                                step = 0.1,
                                help = 'Select the effectiveness of mitigation measures',
                                key='seir_m')
      

        day_value = st.slider('Number of days',
                                min_value = 100,
                                max_value = 730,
                                value = 150,
                                step = 10,
                                help = '2 years in total',
                                key='seir_m')
      
      
        exp_incu = st.slider('Expose Rate(alpha)', 
                                min_value = 1, 
                                max_value = 10,
                                value = 3, 
                                step = 1,
                                help = 'Select the number of days(mean exposed rate = 1/number of days',
                                key='seir_m')
        # alpha
        expose_rate = 1/exp_incu
      
        eff_con = st.slider('Contact Rate(beta)', 
                                min_value = 1, 
                                max_value = 20,
                                value = 10, 
                                step = 1,
                                help = 'Select the number of contacts(per day)',
                                key='seir_m')
        # beta
        contact_rate = model_func.eff_contact(eff_con)

        rec_infect = st.slider('Recovery Rate(gamma)', 
                                min_value = 1, 
                                max_value = 10,
                                value = 5, 
                                step = 1,
                                help = 'Select the number of days(mean recovery rate = 1/number of days',
                                key='seir_m')

        # gammma 
        recovery_rate = 1/rec_infect


        # total population
        total_pop = pop
        # number of exposed people initialised
        exposed = expos
        # number of infected people initialised
        infected = infec
        # number of recovered people initialised
        recovered = recov
        # people apart from the infected and recovered
        susceptible = total_pop - exposed - infected - recovered
        # grid of time points (in days)
        t = np.linspace(0, day_value, day_value)
        # list of days
        days = range(0, day_value)

        # differential equations
        seirm_r = st.beta_expander('Basic Reproduction Ratio')

        with seirm_r:
            
            st.markdown(r'$\it R_{0} = \Large {\frac {\beta}{\gamma}}$, is the "Basic Reproduction Number" that describes the transmissability or contagiousness of an infectious disease')

            st.markdown(u'▶ If R\u2080 > 1, the infectious population will increase')

            st.markdown(u'▶ If R\u2080 = 1, then transmission of the disease may occur but will be confined in a group of susceptible people or a particular location following a rate of consistency, meaning the disease is at an endemic stage')

            st.markdown(u'▶ If R\u2080 < 1, the infectious population will decrease')
            
            r_seirm = model_func.brr(contact_rate,recovery_rate)
            st.info(u"The R\u2080 value of the current SEIR Model(Mitigation) is, {:.2f}".format(r_seirm))

        # Use differential equations magic with our population
        ret = odeint(model_func.seirm_model,
                    [susceptible, exposed, infected, recovered], days,
                    args = (m_control, total_pop, expose_rate, contact_rate, recovery_rate))
        S, E, I, R = ret.T

        # plotting the results   
        value = model_func.pop_value(pop)

        with _lock:
            seirm_fig = Figure()
            ax = seirm_fig.add_subplot(1,1,1, facecolor='w', axisbelow=True)
            ax.plot(t, S/1000, 'k', alpha=1, lw=2, ls='-', label='Susceptible')
            ax.plot(t, E/1000, '#FFCC00', alpha=1, lw=2, ls='-.', label='Exposed')
            ax.plot(t, I/1000, '#FF0000', alpha=1, lw=2, ls=':', label='Infected')
            ax.plot(t, R/1000, 'c', alpha=1, lw=2, ls='--', label='Recovered')
            ax.set_title(label='SEIR(MITIGATION) PLOT', loc='center', pad=15.0, fontsize=25)
            ax.set_xlabel('Time in days')
            ax.set_ylabel('Population in 1000s')
            ax.set_ylim(0,value)
            ax.minorticks_on()
            ax.tick_params(axis='x', which='minor')
            ax.grid(b=True, which='major', c='k', lw=0.2, ls='-')
            seirm_fig.patch.set_facecolor('w')
            seirm_fig.patch.set_alpha(0.7)
            ax.patch.set_edgecolor('black')
            ax.patch.set_linewidth(0.7) 
            legend = ax.legend()
            legend.get_frame().set_alpha(1.0)


    if expos < pop and infec < pop and recov < pop and expos + infec + recov < pop:

        st.pyplot(seirm_fig, clear_figure = True)

    else:

        st.error('ERROR: CANNOT DISPLAY PLOT(CHECK INFECTED AND RECOVERED POPULATION VALUES)')





#### COVID-19 DASHBOARD ####
if menu == 'COVID-19 DASHBOARD':
    container = st.sidebar.beta_container()

    container.title('CONTROLS')

    with st.beta_container():

        st.title('COVID-19 DASHBOARD')

        st.markdown('This dashboard provides information concerning the global scale at which Covid-19 had spread.')

        st.header('Covid-19 Map View')
        
        map_data = model_func.country_clean()
        st.map(map_data, zoom = 1)
        
        # calling the respective functions containing the final datasets and storing the returned data to respective variables  
        country_data = model_func.country_clean()
        sorted_infected_country = country_data.sort_values('Confirmed', ascending = False)
        sorted_recovered_country = country_data.sort_values('Recovered', ascending = False)
        sorted_deceased_country = country_data.sort_values('Deaths', ascending = False)

        country_value = len(country_data)

        st.header('Covid-19 World Count')
        total_infected = int(country_data['Confirmed'].sum())
        total_recovered = int(country_data['Recovered'].sum())
        total_deaths = int(country_data['Deaths'].sum())

        st.warning('TOTAL INFECTED POPULATION COUNT:    {:,}'.format(total_infected))
        st.success('TOTAL RECOVERED POPULATION COUNT:    {:,}'.format(total_recovered))
        st.error('TOTAL DECEASED POPULATION COUNT:    {:,}'.format(total_deaths))

        # setting up controls for the dashboard
        infected_count = container.slider('Number of Countries(Infected Population)', 
                            min_value = 1, 
                            max_value = country_value,
                            value = 10, 
                            step = 1,
                            help = 'Select the number of countries(Infected Population')

        recovered_count = container.slider('Number of Countries(Recovered Population)', 
                            min_value = 1, 
                            max_value = country_value,
                            value = 10, 
                            step = 1,
                            help = 'Select the number of countries(Recovered Population')

        deceased_count = container.slider('Number of Countries(Deceased Population)', 
                            min_value = 1, 
                            max_value = country_value,
                            value = 10, 
                            step = 1,
                            help = 'Select the number of countries(Deceased Population')

        # plotting the results
        st.header('TOP COUNTRIES - INFECTED POPULATION')
        infected_fig = px.bar(sorted_infected_country.head(infected_count), 
                            x = 'Country', y = 'Confirmed',
                            hover_data = ['Country', 'Confirmed'], 
                            color = 'Confirmed',
                            labels = {'Confirmed':'Infected Count'}, 
                            height = 500)
    
        st.plotly_chart(infected_fig, use_container_width = True)

        st.header('TOP COUNTRIES - RECOVERED POPULATION')
        recovered_fig = px.bar(sorted_recovered_country.head(recovered_count), 
                            x = 'Country', y = 'Recovered',
                            hover_data = ['Country', 'Recovered'], 
                            color = 'Recovered', 
                            labels = {'Recovered':'Recovered Count'},
                            height = 500)
    
        st.plotly_chart(recovered_fig, use_container_width = True)

        st.header('TOP COUNTRIES - DECEASED POPULATION')
        deceased_fig = px.bar(sorted_deceased_country.head(deceased_count), 
                            x = 'Country', y = 'Deaths',
                            hover_data = ['Country', 'Deaths'], 
                            color = 'Deaths', 
                            labels = {'Deaths':'Deceased Count'},
                            height = 500)
    
        st.plotly_chart(deceased_fig, use_container_width = True)