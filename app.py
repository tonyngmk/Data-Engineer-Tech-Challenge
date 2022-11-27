import requests, json, datetime
import streamlit as st
import pandas as pd
import numpy as np

start = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
end = datetime.datetime.today().strftime("%Y-%m-%d")

st.title(f'COVID-19 Dashboard')

@st.cache
def get_data(url):
    data = requests.get(url)
    d = json.loads(data.content)
    df = pd.DataFrame(d)
    df['Date'] = df['Date'].str[:10]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').set_index('Date')
    return df

# Get world data
DATE_COLUMN = 'Date'
data_load_state = st.text('Loading data...')

url = f'https://api.covid19api.com/world?from={start}T00:00:00Z&to={end}T00:00:00Z'
data = get_data(url).iloc[:, :-2]
data_load_state.text("Done!")

if st.checkbox('Show raw data', key='1'):
    st.subheader('Raw data')
    st.write(data)

st.subheader(f'Data between ({start} - {end})')
# day_to_filter = (datetime.datetime.today() - datetime.timedelta(days=30)) + datetime.timedelta(days=15)
# day_to_filter = st.slider('hour', 0, 30, 14)
# data = data[data.index >= (datetime.datetime.today() - datetime.timedelta(days=30)) + datetime.timedelta(days=day_to_filter)]
rows_to_filter = st.slider('Days of data', 0, 30, 14, key='3')
data = data.iloc[:rows_to_filter]

st.subheader(f'World New Cases')

st.write('World new confirmed')
st.bar_chart(data['NewConfirmed'])

st.write('World new deaths')
st.area_chart(data['NewDeaths'])

st.subheader(f'World Total Cases')
st.bar_chart(data[['TotalDeaths', 'TotalConfirmed']])


asia_list = ['singapore', 'malaysia', 'vietnam', 'thailand', 'indonesia', 'taiwan', 'korea-south', 'korea-north']
df_list = []

for country in asia_list:
    url = f'https://api.covid19api.com/country/{country}/status/confirmed?from={start}T00:00:00Z&to={end}T00:00:00Z'
    data_country = get_data(url)
    df_list.append(data_country)

data_asia = pd.concat(df_list)[['Country', 'Lat', 'Lon', 'Cases']].reset_index()
data_asia = data_asia.groupby(['Country', 'Lat', 'Lon', 'Date']).sum().reset_index()
data_asia = data_asia.rename({"Lat":"lat", "Lon":"lon"}, axis=1)
data_asia = data_asia.astype({"lat":"float", "lon":"float"})


st.subheader(f'Asia Country Confirmed Cases')

if st.checkbox('Show raw data', key='4'):
    st.subheader('Raw data')
    st.write(data_asia)

if st.checkbox('Show summarised data', key='5'):
    st.subheader('Summarised data')
    st.write(data_asia.groupby(['Country', 'lat', 'lon']).sum().reset_index())

# Map
data_asia['Date'] = data_asia['Date'].astype('str').str[:10]
day_to_filter = st.slider('day', 0, 30, 14, key='6')
data_asia_map_plot = data_asia[data_asia['Date'] == ((datetime.datetime.today() - datetime.timedelta(days=30)) + datetime.timedelta(days=day_to_filter)).strftime('%Y-%m-%d')]
st.subheader('Map of cases in Asia')
st.map(data_asia_map_plot)