import streamlit as st
import streamlit.components.v1 as components
import datetime

st.set_page_config(layout = 'wide')
c1, c2 = st.columns(2)


with c1:
    option = st.selectbox(
     'Select the map you want to see:',
     #('Daily Confirmed Cases', 'Daily Deaths', 'Aggregated Confirmed Cases', 'Aggregated Deaths'))
     ('Daily Confirmed Cases', 'Daily Deaths'))

with c2:
    #d = st.date_input(
    # "Select a date:",
    # datetime.date(2020, 1, 22))
    d = st.slider(
     "When do you start?",
    datetime.date(2020, 1, 22),
    datetime.date(2020, 3, 29),
    datetime.date(2020, 1, 22),
     format="MM/DD/YY")
    #st.write("Start time:", d)

start = datetime.date(2020, 1, 22)
end = datetime.date(2020, 3, 29)
if (d>=start and d<=end):
    date = str(d.month)+"_"+str(d.day)+"_"+str(d.year)
    if(option=='Daily Confirmed Cases'):
        filepath = "FinalProject/HTML/CONFIRMED/c"+date+".html"
        htmlFile = open(filepath, 'r', encoding='utf-8')
    elif(option=='Daily Deaths'):
        filepath = "FinalProject/HTML/DEATHS/d"+date+".html"
        htmlFile = open(filepath, 'r', encoding='utf-8')
    source_code = htmlFile.read()
    components.html(source_code, height = 650)
else:
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">Data is not available for the date you selected!</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Selected a data between '+str(start)+' and '+str(end)+' to proceed!</p>', unsafe_allow_html=True)
    
