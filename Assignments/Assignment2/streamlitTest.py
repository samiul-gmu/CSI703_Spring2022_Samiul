import streamlit as st
name = st.text_input('Name', '')
g_num = st.text_input('G-Number', '')
st.write('Hello', name, '-', g_num)