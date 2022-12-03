import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(
     page_title="Soft Ferrites",
     page_icon=":sunglasses",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

image_ferrite = Image.open('softferrite.png')
# three columns for titles and logo
coltitle1, coltitle2, coltitle3 = st.columns(3)
# first column: title and subtitle
with coltitle1:
    st.title('Data from my PhD')
    st.header('Soft ferrites')
# second column: empty
# third column: logo
with coltitle3:
    st.image(image_ferrite)

st.markdown('---')

with st.sidebar:
    selected_ferrite = st.selectbox(
        'Please select a material',
        ('N87', 'N95', 'N97', 'N49', 'PC200',
        '3C96', '3C95', '3F36', '3F4', '3F46',
        'ML27D', 'ML95S', 'ML91S')
    )

st.sidebar.text('Found bugs?')
st.sidebar.text('Email to yudixiaojd@outlook.com')

st.subheader('Specify magnetizing frequency and temperature')
st.write('You selected:',selected_ferrite)

# make frequency list according to selected material
if (selected_ferrite == 'N87' or selected_ferrite == 'N95' or 
selected_ferrite == 'N97' or selected_ferrite == 'ML27D'):
    frequency_list = [100, 300, 500]
elif selected_ferrite == 'N49':
    frequency_list = [100, 300, 500, 1000]
elif selected_ferrite == 'PC200':
    frequency_list = [300, 500, 1000, 2000]
elif selected_ferrite == '3C96':
    frequency_list = [100, 150, 300, 500]
elif selected_ferrite == '3C95':
    frequency_list = [10, 100, 300, 500]
elif (selected_ferrite == '3F36' or selected_ferrite == 'ML95S'):
    frequency_list = [300, 500, 1000]
elif (selected_ferrite == '3F4' or selected_ferrite == '3F46' or 
selected_ferrite == 'ML91S'):
    frequency_list = [100, 500, 1000, 2000, 3000]


colcondition1, colcondition2, colcondition3  = st.columns(3)
# first column: magnetizing frequency
with colcondition1:
    selected_frequency = st.selectbox(
        'Magnetizing frequency in kHz',
        (frequency_list)
    )
# second column: empty
# third column: Temperature 
with colcondition3:
    selected_temperature = st.slider(
        'Temperature in degree Celsius', 25, 150, 25,25
    )

st.markdown('---')

# Output area

# load data
# name of csv file containing BH data
BH_filename = 'BH_data/' + selected_ferrite + '_' + str(selected_frequency) + \
    'kHz_' + str(selected_temperature) + 'degC.csv'

df = pd.read_csv(BH_filename, header = None)
df.columns = ['H (A/m)', 'B (T)']

fig_BH, ax = plt.subplots()
ax.plot(df['H (A/m)'],df['B (T)'],'g-')
ax.set_xlabel('H (A/m)')
ax.set_ylabel('B (T)')
ax.grid(visible = bool, which = 'both', axis = 'both')
#plt.show()

st.subheader('Here is the data')
colout1, colout2 = st.columns(2)
# first column: B-H curve
with colout1:
    st.text('BH curve')
    st.pyplot(fig_BH)

with colout2:
    st.download_button(
        label = 'Download data as CSV',
        data = df.to_csv().encode('utf-8'),
        file_name = selected_ferrite + '_' + str(selected_frequency) + \
        'kHz_' + str(selected_temperature) + 'degC.csv',
        mime = 'text/csv',
    )
    
