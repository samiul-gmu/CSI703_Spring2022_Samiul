import streamlit as st
#import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt



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
        
elif (option == 'Distributions and part-to-whole'):
    df = pd.read_excel('Assignment_Files/Data/forestfires.xlsx')
    df_sum = df.groupby(['month']).sum()
    df_pie_plot = df_sum[['wind', 'area']]
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    df_pie_plot = df_pie_plot.loc[months]
    x = df_pie_plot.index.tolist()
    y = df_pie_plot['area'].tolist()
    percent = [100*ey / sum(y) for ey in y]
    colors = ['lightcoral','lightskyblue','yellow','yellowgreen','grey','pink','blue','darkgreen','cyan','magenta','violet','gold']
    patches, texts = plt.pie(y, colors = colors, counterclock=False, startangle=-270, radius=1)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
    plt.title('Part-to-whole Distribution of\nForest Fire', loc='center',fontsize=12)
    
    plt.legend(patches, labels, title = 'Month', loc='center', bbox_to_anchor=(-0.1, 1.),
               fontsize=9)
    st.pyplot(plt)
elif (option == 'Geospatial'):
    pass
elif (option == 'Concepts and qualitative'):
    pass
    