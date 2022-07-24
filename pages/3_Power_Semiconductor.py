import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(
     page_title="Power Semiconductor",
     page_icon=":sunglasses",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

image_powersemi = Image.open('powersemi.png')
# three columns for titles and logo
coltitle1, coltitle2 = st.columns(2)
# first column: title and subtitle
with coltitle1:
    st.title('Data from my PhD')
    st.header('Power semiconductor')
# second column: logo
with coltitle2:
    st.image(image_powersemi)

st.markdown('---')

with st.sidebar:
    selected_SiCMfr = st.selectbox(
        'Please select a manufacturer',
        ('Wolfspeed', 'GeneSiC', 'Infineon', 'Microchip', 'ONsemi')
    )

    if selected_SiCMfr == 'Wolfspeed':
        selected_SiCMOSFET = st.selectbox(
            'Please select a part',
            ('C2M0280120D','C2M0080120D','C2M0025120D',
            'C3M0350120D','C3M0075120D')
        )
    elif selected_SiCMfr == 'GeneSiC':
        selected_SiCMOSFET = st.selectbox(
            'Please select a part',
            ('G2R1000MT17D','G3R40MT12D')
        )
    elif selected_SiCMfr == 'Microchip':
        selected_SiCMOSFET = st.selectbox(
            'Please select a part',
            ('MSC040SMA120B','MSC025SMA120B')
        )
    elif selected_SiCMfr == 'ONsemi':
        selected_SiCMOSFET = st.selectbox(
            'Please select a part',
            ('NVHL020N120SC1','')
        )
    elif selected_SiCMfr == 'Infineon':
        selected_SiCMOSFET = st.selectbox(
            'Please select a part',
            ('IMW120R030M1HXKSA1','')
        )

st.sidebar.text('Found bugs?')
st.sidebar.text('Email to yudixiaojd@outlook.com')

st.subheader('Specify temperature')
st.write('You selected:',selected_SiCMOSFET,' from ',selected_SiCMfr)

colcondition1, colcondition2, colcondition3  = st.columns(3)
# first column: temperature
with colcondition1:
    selected_temperature = st.slider(
        'Temperature in degree Celsius', 25, 175, 25,25
    )
# second column: empty
# third column: empty

st.markdown('---')

st.subheader('Here is the data')

colout1, colout2, colout3 = st.columns(3)

# output characteristics, on-resistance
# load data
# name of csv file
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'Rds-Id.csv'

df_temp = pd.read_csv(filename, header = None, skiprows = 150, nrows = 2)
df_temp.columns = ['Temp1', 'Dimension', 'Temp2', 'Temp3', 'Temp4', 'Temp5', 'Temp6']
n_Id = df_temp['Dimension'][0]  # number of data points of drain-to-source current
n_Vgs = df_temp['Dimension'][1] # number of data points of gate voltage
n_row_total = n_Id * n_Vgs  # total number of data sets

df_out = pd.read_csv(filename, header = None, skiprows = 153, nrows = n_row_total)
df_out.columns = ['Name', 'Igate', 'Vgate', 'Vdrain', 'Idrain', 'Ta', 'Rds']

fig_out, ax_out = plt.subplots()
for i in range(n_Vgs):
    ax_out.plot(df_out['Vdrain'][i*n_Id:(i+1)*n_Id-1],df_out['Idrain'][i*n_Id:(i+1)*n_Id-1], 
    label = 'Vgs=' + str(round(df_out['Vgate'][i*n_Id])) + 'V')
ax_out.set_xlabel('Vds (V)')
ax_out.set_ylabel('Ids (A)')
ax_out.grid(visible = bool, which = 'both', axis = 'both')
plt.legend()
#plt.show()

with colout1:
    st.text('Output characteristics')
    st.pyplot(fig_out)
    st.download_button(
        label = 'Download data as CSV',
        data = df_out.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'output.csv',
        mime = 'text/csv',
    )

fig_Rds, ax_Rds = plt.subplots()
for i in range(n_Vgs):
    ax_Rds.plot(df_out['Idrain'][i*n_Id:(i+1)*n_Id-1], df_out['Rds'][i*n_Id:(i+1)*n_Id-1], 
    label = 'Vgs=' + str(round(df_out['Vgate'][i*n_Id])) + 'V')
ax_Rds.set_xlabel('Ids (A)')
ax_Rds.set_ylabel('Rds (ohm)')
ax_Rds.set_yscale('log')
ax_Rds.grid(visible = bool, which = 'both', axis = 'both')
plt.legend()

with colout2:
    st.text('Drain-to-source resistance')
    st.pyplot(fig_Rds)
    st.download_button(
        label = 'Download data as CSV',
        data = df_out.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'Rds.csv',
        mime = 'text/csv',
    )

# threshold voltage
# load data
# name of csv file
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'ID-VGS-Vds-3.csv'

df_Vth = pd.read_csv(filename, header = 257)
df_Vth.columns = ['Dataname','VGS', 'ID']

fig_Vth, ax_Vth = plt.subplots()
ax_Vth.plot(df_Vth['VGS'],df_Vth['ID'],'b-')
ax_Vth.set_xlabel('Vgs (V)')
ax_Vth.set_ylabel('Id (A)')
ax_Vth.grid(visible = bool, which = 'both', axis = 'both')
#plt.show()

with colout3:
    st.text('Threshold voltage')
    st.pyplot(fig_Vth)
    st.download_button(
        label = 'Download data as CSV',
        data = df_Vth.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'ID-VGS-Vds-3.csv',
        mime = 'text/csv',
    )


# third quadrant characteristics
# load data
# name of csv file
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'ID-VDS-3rd-VGS_10_20.csv'

# Vgs sweep
if (selected_SiCMOSFET == 'C3M0075120D' or selected_SiCMOSFET == 'C3M0350120D' or 
selected_SiCMOSFET == 'G3R40MT12D' or selected_SiCMOSFET == 'IMW120R030M1HXKSA1'):
    Vgs_3rd = np.arange(10.0, 15.0 + 1.25, 1.25)
else:
    Vgs_3rd = np.arange(15.0, 20.0 + 1.25, 1.25)

if (selected_SiCMOSFET == 'C2M0080120D' or selected_SiCMOSFET == 'C2M0280120D' or 
selected_SiCMOSFET == 'C3M0350120D' or selected_SiCMOSFET == 'C3M0075120D'):
    skiprow_3rd = 257
else:
    skiprow_3rd = 255

df_temp = pd.read_csv(filename, header = None, skiprows = skiprow_3rd, nrows = 2)
df_temp.columns = ['Name', 'Dimension1', 'Dimension2']
n_Id = df_temp['Dimension1'][0]
n_Vgs = df_temp['Dimension1'][1]

df_3rd = pd.read_csv(filename, header = None, skiprows = skiprow_3rd + 3)

if (selected_SiCMOSFET == 'C2M0080120D' or selected_SiCMOSFET == 'C2M0280120D' or 
selected_SiCMOSFET == 'C3M0350120D' or selected_SiCMOSFET == 'C3M0075120D'):
    df_3rd.columns = ['Name', 'VDS', 'ID']
else:
    df_3rd.columns = ['Name', 'ID', 'VDS']

fig_3rd, ax_3rd = plt.subplots()
for i in range(n_Vgs):
    ax_3rd.plot(df_3rd['VDS'][i*n_Id:(i+1)*n_Id-1],df_3rd['ID'][i*n_Id:(i+1)*n_Id-1], 
    label = 'Vgs=' + str(Vgs_3rd[i]) + 'V')
ax_3rd.set_xlabel('Vds (V)')
ax_3rd.set_ylabel('Ids (A)')
ax_3rd.grid(visible = bool, which = 'both', axis = 'both')
plt.legend()
#plt.show()

with colout1:
    st.text('3rd quadrant characteristics')
    st.pyplot(fig_3rd)
    st.download_button(
        label = 'Download data as CSV',
        data = df_3rd.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'ID-VDS-3rd-VGS_10_20.csv',
        mime = 'text/csv',
    )

# body diode characteristics
# load data
# name of csv file
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'ID-VDS-body-diode-VGS_-5_0.csv'

# Vgs sweep
if (selected_SiCMOSFET == 'IMW120R030M1HXKSA1'):
    Vgs_body = np.arange(-2, 1, 1)
else:
    Vgs_body = np.arange(-5, 1, 1)

df_temp = pd.read_csv(filename, header = None, skiprows = skiprow_3rd, nrows = 2)
df_temp.columns = ['Name', 'Dimension1', 'Dimension2']
n_Id = df_temp['Dimension1'][0]
n_Vgs = df_temp['Dimension1'][1]

df_body = pd.read_csv(filename, header = None, skiprows = skiprow_3rd + 3)

if (selected_SiCMOSFET == 'C2M0080120D' or selected_SiCMOSFET == 'C2M0280120D' or 
selected_SiCMOSFET == 'C3M0350120D' or selected_SiCMOSFET == 'C3M0075120D'):
    df_body.columns = ['Name', 'VDS', 'ID']
else:
    df_body.columns = ['Name', 'ID', 'VDS']

fig_body, ax_body = plt.subplots()
for i in range(n_Vgs):
    ax_body.plot(df_body['VDS'][i*n_Id:(i+1)*n_Id-1],df_body['ID'][i*n_Id:(i+1)*n_Id-1], 
    label = 'Vgs=' + str(Vgs_body[i]) + 'V')
ax_body.set_xlabel('Vds (V)')
ax_body.set_ylabel('Ids (A)')
ax_body.grid(visible = bool, which = 'both', axis = 'both')
plt.legend()
#plt.show()

with colout2:
    st.text('Body diode characteristics')
    st.pyplot(fig_body)
    st.download_button(
        label = 'Download data as CSV',
        data = df_body.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'ID-VDS-body-diode-VGS_-5_0.csv',
        mime = 'text/csv',
    )

# drain-to-source capacitance Cds
# load data
# name of csv file
filename = 'SiC_switch_data/Cds/Cds_' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC.csv'

df_temp = pd.read_csv(filename, header = None, skiprows = 150, nrows = 2)
df_temp.columns = ['Temp1', 'Dimension', 'Temp2', 'Temp3', 'Temp4', 'Temp5']
n_Vds = df_temp['Dimension'][0]  # number of data points of drain-to-source voltage

df_Cds = pd.read_csv(filename, header = None, skiprows = 153, nrows = n_Vds)
df_Cds.columns = ['Name', 'Ids', 'Vdrain', 'Cds', 'G', 'Ta']

fig_Cds, ax_Cds = plt.subplots()
ax_Cds.plot(df_Cds['Vdrain'], df_Cds['Cds'],'g-')
ax_Cds.set_xlabel('Vds (V)')
ax_Cds.set_ylabel('Cds (F)')
ax_Cds.set_yscale('log')
ax_Cds.grid(visible = bool, which = 'both', axis = 'both')

with colout1:
    st.text('Drain-to-source capacitance')
    st.pyplot(fig_Cds)
    st.download_button(
        label = 'Download data as CSV',
        data = df_Cds.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'Cds.csv',
        mime = 'text/csv',
    )

# gate-to-source capacitance Cgs
# load data
# name of csv file
filename = 'SiC_switch_data/Cgs/Cgs_' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC.csv'

df_temp = pd.read_csv(filename, header = None, skiprows = 150, nrows = 2)
df_temp.columns = ['Temp1', 'Dimension', 'Temp2', 'Temp3', 'Temp4', 'Temp5']
n_Vds = df_temp['Dimension'][0]  # number of data points of drain-to-source voltage

df_Cgs = pd.read_csv(filename, header = None, skiprows = 153, nrows = n_Vds)
df_Cgs.columns = ['Name', 'Ids', 'Vdrain', 'Cgs', 'G', 'Ta']

fig_Cgs, ax_Cgs = plt.subplots()
ax_Cgs.plot(df_Cgs['Vdrain'], df_Cgs['Cgs'],'b-')
ax_Cgs.set_xlabel('Vds (V)')
ax_Cgs.set_ylabel('Cgs (F)')
#ax_Cgs.set_yscale('log')
ax_Cgs.grid(visible = bool, which = 'both', axis = 'both')

with colout2:
    st.text('Gate-to-source capacitance')
    st.pyplot(fig_Cgs)
    st.download_button(
        label = 'Download data as CSV',
        data = df_Cgs.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'Cgs.csv',
        mime = 'text/csv',
    )

# gate to source leakage current
# load data
# name of csv file
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'IG-VGS-VDS_0.csv'

df_Ig = pd.read_csv(filename, header = None, skiprows = 259)
if (selected_SiCMOSFET == 'C2M0280120D' or selected_SiCMOSFET =='C2M0080120D' or 
selected_SiCMOSFET == 'C3M0350120D' or selected_SiCMOSFET == 'C3M0075120D'):
    df_Ig.columns = ['Name', 'Vgs', 'Ig']
else:
    df_Ig.columns = ['Name', 'Ig', 'Vgs']

fig_Ig, ax_Ig = plt.subplots()
ax_Ig.plot(df_Ig['Vgs'],df_Ig['Ig'],'g-')
ax_Ig.set_xlabel('Vgs (V)')
ax_Ig.set_ylabel('Ig (A)')
ax_Ig.grid(visible = bool, which = 'both', axis = 'both')
#plt.show()

with colout3:
    st.text('Gate leakage current')
    st.pyplot(fig_Ig)
    st.download_button(
        label = 'Download data as CSV',
        data = df_Ig.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'IG-VGS-VDS_0.csv',
        mime = 'text/csv',
    )

# drain to source leakage current with 0V gate voltage
# load data 
# name of csv file 
filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
    str(selected_temperature) + '_degC/' + 'ID(off)-VDS-VGS_0.csv'

df_Idoff_0 = pd.read_csv(filename, header = 252)
df_Idoff_0.columns = ['Dataname','ID', 'VDS']

fig_Idoff_0, ax_Idoff_0 = plt.subplots()
ax_Idoff_0.plot(df_Idoff_0['VDS'],df_Idoff_0['ID'],'r-')
ax_Idoff_0.set_xlabel('Vds (V)')
ax_Idoff_0.set_ylabel('Id (A)')
ax_Idoff_0.grid(visible = bool, which = 'both', axis = 'both')
#plt.show()

with colout3:
    st.text('Drain-to-source leakage current with 0V gate voltage')
    st.pyplot(fig_Idoff_0)
    st.download_button(
        label = 'Download data as CSV',
        data = df_Idoff_0.to_csv().encode('utf-8'),
        file_name = selected_SiCMOSFET + '_' + \
            str(selected_temperature) + 'degC_' + 'ID(off)-VDS-VGS_0.csv',
        mime = 'text/csv',
    )


# drain to souce leakage current with negative gate voltage
# load data
# name of csv file
if selected_SiCMfr == 'Infineon':
    with colout3:
        st.text('Infineon SiC MOSFETs are made with relatively high')
        st.text('threshold voltage, thereby do not need negative bias')
        st.text('voltage on gate in off state.')
else:
    filename = 'SiC_switch_data/' + selected_SiCMOSFET + '_' + \
        str(selected_temperature) + '_degC/' + 'ID(off)-VDS-VGS_-5.csv'

    df_Idoff_5 = pd.read_csv(filename, header = 252)
    df_Idoff_5.columns = ['Dataname','ID', 'VDS']

    fig_Idoff_5, ax_Idoff_5 = plt.subplots()
    ax_Idoff_5.plot(df_Idoff_5['VDS'],df_Idoff_5['ID'],'r-')
    ax_Idoff_5.set_xlabel('Vds (V)')
    ax_Idoff_5.set_ylabel('Id (A)')
    ax_Idoff_5.grid(visible = bool, which = 'both', axis = 'both')

    with colout3:
        st.text('Drain-to-source leakage current with -5V gate voltage')
        st.pyplot(fig_Idoff_5)
        st.download_button(
            label = 'Download data as CSV',
            data = df_Idoff_5.to_csv().encode('utf-8'),
            file_name = selected_SiCMOSFET + '_' + \
                str(selected_temperature) + 'degC_' + 'ID(off)-VDS-VGS_-5.csv',
            mime = 'text/csv',
        )

st.markdown('---')