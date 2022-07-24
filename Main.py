from matplotlib.pyplot import text
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(
     page_title="YudiPhDdata",
     page_icon=":sunglasses",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

st.sidebar.text('Found bugs?')
st.sidebar.text('Email to yudixiaojd@outlook.com')

image_logo = Image.open('logo.jpeg')
# three columns for titles and logo
coltitle1, coltitle2, coltitle3 = st.columns(3)
# first column: title and subtitle
with coltitle1:
    st.title('Data from my PhD')
    st.header('-Yudi Xiao')
# second column: empty
# third column: logo
with coltitle3:
    st.image(image_logo)

st.markdown('---')

# Introduction of PEdata
st.subheader('Me')
st.text('My name is Yudi Xiao. I had my PhD about high-temperature power electronics in 2018-2022 at Technical University of Denmark.')

st.subheader('This website')
st.text('This website was made to share some of the data generated from my PhD.')

st.subheader('the data')
st.text('BH curves of a few commercially available soft ferrite materials (see below) measured at various magnetizing frequency and temperture.')
st.image(Image.open('ferrite_all.png'))

st.text('Output characteristics, threshold voltage, 3rd quadrant characteristics, leakage currents, and junction capacitances of')
st.text('a few commercially available SiC power MOSFETs (see below) measured at various temperture.')
st.image(Image.open('MOSFET_all.png'))

st.subheader('How to use')
st.text('All data is visualized and is available for downloading.')

st.subheader('Useful links')
urlthesis = 'https://drive.google.com/file/d/1lRpnf4uy2Sw90Qrk62dPxeoq-VJwS_Mv/view?usp=sharing'
st.write('Link to my PhD thesis (%s)' % urlthesis)

st.markdown('---')