import streamlit as st
import pandas as pd
from components import bar, gauge, rose
from urllib.parse import urlencode, urlunparse
import json, requests

api_params = {
    'device_id': st.secrets['device_id'],
    'password': st.secrets['password'],
    'api_key': st.secrets['api_key']
}

# Build URL according to the APIv1 documentation
# https://www.weatherlink.com/static/docs/APIdocumentation.pdf
request_url = urlunparse(
    (
        'https',
        'api.weatherlink.com',
        '/v1/NoaaExt.json',
        '',
        urlencode(api_params),
        ''
    )
)

try:
    current_conditions = json.loads(requests.get(request_url).text)
except:
    pass

st.title("Weather Station")

st.plotly_chart(bar(
    'Temperature', 
    ['Outside Temp', 'Wind Chill', 'Heat Index', 'Dew Point', 'Wet Bulb'],
    [49, 49, 49, 45, 47],
    ['#c42728', '#3188c2', '#e97f23', '#37916e', '#56a8cc'],
    ' °F'))
st.plotly_chart(gauge('THW Index', 48, '°F', 0, 50, '#02a89c'))
st.plotly_chart(bar(
    'Total Rain', 
    ['month', 'year'],
    [2.15, 11.33],
    ['#28b574', '#3188c2'],
    ' in'))
st.plotly_chart(gauge('Humidity', 87, '%', 0, 100, '#37916e'))
st.plotly_chart(gauge('Wind Speed', 0, 'mph', 0, 100, '#37916e'))
st.plotly_chart(rose())