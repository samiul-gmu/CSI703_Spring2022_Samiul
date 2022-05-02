import streamlit as st
#import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px


st.set_page_config(layout = 'wide')

option = st.selectbox(
     'Select the map you want to see:',
     #('Daily Confirmed Cases', 'Daily Deaths', 'Aggregated Confirmed Cases', 'Aggregated Deaths'))
     ('Correlation, comparisons, and trends', 'Distributions and part-to-whole', 'Geospatial', 'Concepts and qualitative'))

if (option == 'Correlation, comparisons, and trends'):
    # Take input from the excel file and load it to a dataframe
    df = pd.read_excel('Assignment_Files/Data/forestfires.xlsx')
    
    # Convert the month column from string to int
    df["month"].replace({"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}, inplace=True)
    df["month"] = df["month"].astype(int)
    
    
    var = st.multiselect(
     "Select variable(s):",
     ['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area'],
     ['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area'])
    
    if(len(var)==0):
        st.write('Select variable(s) to proceed!')
    else:
        preVar = ['X', 'Y', 'month', 'day']
        df = df[preVar+var]

        # Plot a pair plot color-coded by months to see if they show any relation
        fig = px.parallel_coordinates(df, color="month",
                                     color_continuous_scale=px.colors.diverging.Tealrose,
                                     color_continuous_midpoint=6, width=1500, height=800,
                                      title="Relations between weather/dryness variables while grouping them by month")
        st.plotly_chart(fig)