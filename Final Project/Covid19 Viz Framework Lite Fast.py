import streamlit as st
import streamlit.components.v1 as components
import datetime

st.set_page_config(layout = 'wide')
c1, c2 = st.columns(2)


with c1:
    option = st.selectbox(
     'Select the map you want to see:',
     ('Daily Confirmed Cases', 'Daily Deaths', 'Aggregated Confirmed Cases', 'Aggregated Deaths'))

with c2:
    d = st.date_input(
     "When's your birthday",
     datetime.date(2020, 3, 19))

start = datetime.date(2020, 1, 22)
end = datetime.date(2020, 3, 29)
if (d>=start and d<=end):
    date = str(d.month)+"_"+str(d.day)+"_"+str(d.year)
    if(option=='Daily Confirmed Cases'):
        filepath = "HTML/CONFIRMED/c"+date+".html"
        HtmlFile = open(filepath, 'r', encoding='utf-8')
    elif(option=='Daily Deaths'):
        HtmlFile = open("deaths.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 650)
else:
    #st.write('Data is not available for the date you selected!')
    #st.write('Selected a data between', start, 'and', end,' to proceed!')
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">Data is not available for the date you selected!</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Selected a data between '+str(start)+' and '+str(end)+' to proceed!</p>', unsafe_allow_html=True)