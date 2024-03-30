import streamlit as st
from components import make_bar_plot, make_indicator_plot, make_barpolar_plot
from plotly.subplots import make_subplots
from urllib.parse import urlencode, urlunparse
import json, requests
from math import atan
from email.utils import parsedate_to_datetime
from datetime import timedelta, timezone

# Keep the API response for a maximum of 10 minutes
@st.cache_data(ttl=600)
def api_call():
    # Use demo example if API parameters are missing
    try:
        api_params = {
            'user': st.secrets['device_id'],
            'pass': st.secrets['password'],
            'apiToken': st.secrets['api_key']
        }
    except:
        api_params = {
            'user': '001D0A00DE6A',
            'pass': 'DEMO',
            'apiToken': 'demo0a002bc5272033001d0a002bc527'
        }
    
    # Build the URL according to the APIv1 documentation
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

    return json.loads(requests.get(request_url).text)

cond = api_call()

# Create helper functions to calculate the THW index and wet bulb temperature
def calc_thw_index(heat_index, wind_speed):
    heat_index, wind_speed = float(heat_index), float(wind_speed)
    thw_index = heat_index - (1.072 * wind_speed)
    return thw_index

def calc_wet_bulb(temp, rel_hum):
    temp, rel_hum = float(temp), float(rel_hum)
    wet_bulb = temp * atan(0.152 * (rel_hum + 8.3136) ** (1/2)) \
               + 0.00391838 * (rel_hum ** (3/2)) * atan(0.0231 * rel_hum) \
               - atan(rel_hum - 1.6763) \
               + atan(temp + rel_hum) \
               - 4.686
    return wet_bulb

# Import CSS styles
with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Customize sidebar
with st.sidebar:
    st.write('# PHIG')
    st.write('## Pleasant Hill, CA')
    st.map({'lat': [float(cond['latitude'])], 'lon': [float(cond['longitude'])]})

# Main section
st.markdown('## Pleasant Hill Instructional Garden (PHIG)')
st.markdown('# Weather Station')

col1, col2 = st.columns(2)

with col1:
    # Convert RFC822 timestamp to datetime format, then UTC to PST
    utc_datetime = parsedate_to_datetime(cond['observation_time_rfc822'])
    pst_datetime = utc_datetime.astimezone(timezone.utc) + timedelta(hours=-8)
    st.markdown(f'Last updated: {pst_datetime.strftime('%b %d, %I:%M %p')}')

with col2:
    unit = st.radio(
        'Choose units',
        ['US Customary', 'Metric'],
        horizontal=True,
        disabled=True
    )

dashboard = make_subplots(rows=4,
                          cols=2,
                          specs=[
                              [{'type': 'bar', 'colspan': 2}, None],
                              [{'type': 'indicator'}, {'type': 'bar'}],
                              [{'secondary_y': True}, {'type': 'indicator'}],
                              [{'type': 'indicator'}, {'type': 'barpolar'}],
                            #   [{'type': 'barpolar', 'rowspan': 2}, {'type': 'bar'}],
                            #   [None, {'type': 'bar'}],
                            #   [{'type': 'bar', 'colspan': 2}, None]
                          ],
                          subplot_titles=('Temperature',
                                          'THW Index',
                                          'Total Rain',
                                          'Current Rain',
                                          'Humidity',
                                          'Wind Speed',
                                          f'Wind Direction<br><sup>{cond['wind_dir']}</sup>',))
                                        #   'Wind Rose',
                                        #   'Sunrise/Sunset',
                                        #   'Moon Phase',
                                        #   'Barometer'))

# Temperature
dashboard.add_trace(make_bar_plot(
    x=['Outside Temp', 'Wind Chill', 'Heat Index', 'Dew Point', 'Wet Bulb'],
    y=[cond['temp_f'],
       cond['windchill_f'],
       cond['heat_index_f'], 
       cond['dewpoint_f'],
       calc_wet_bulb(cond['temp_f'], cond['relative_humidity'])],
    color=['#c42728', '#3188c2', '#e97f23', '#37916e', '#56a8cc'],
    dp='0'),
    row=1,
    col=1)

dashboard.update_yaxes(
    dtick=25,
    range=[0, 75],
    ticksuffix=' °F',
    row=1,
    col=1
)

# THW Index
dashboard.add_trace(make_indicator_plot(
    value=calc_thw_index(cond['heat_index_f'], cond['wind_mph']),
    unit=' °F',
    min=min(0, calc_thw_index(cond['heat_index_f'], cond['wind_mph'])) ,
    max=calc_thw_index(cond['davis_current_observation']['heat_index_year_high_f'], 0),
    color='#02a89c'),
    row=2,
    col=1)

# Total Rain
dashboard.add_trace(make_bar_plot(
    x=['month', 'year'],
    y=[cond['davis_current_observation']['rain_month_in'], cond['davis_current_observation']['rain_year_in']],
    color=['#28b574', '#3188c2'],
    dp='2'),
    row=2,
    col=2)

dashboard.update_yaxes(
    dtick=5,
    range=[0, 15],
    tickformat='.2f',
    ticksuffix=' in',
    row=2,
    col=2
)

# Current Rain
dashboard.add_trace(make_bar_plot(
    x=['day', 'storm'],
    y=[cond['davis_current_observation']['rain_day_in'],
       cond['davis_current_observation']['rain_storm_in']],
    color=['#3d464c', '#1ac1b5'],
    dp='2'),
    row=3,
    col=1,
    secondary_y=False)

dashboard.update_yaxes(
    dtick=0.2,
    range=[0, 0.6],
    tickformat='.2f',
    ticksuffix=' in',
    row=3,
    col=1,
    secondary_y=False
)

dashboard.add_trace(make_bar_plot(
    x=['rate'],
    y=[cond['davis_current_observation']['rain_rate_in_per_hr']],
    color=['#7cb5ec'],
    dp='2'),
    row=3,
    col=1,
    secondary_y=True)

dashboard.update_yaxes(
    showgrid=False,
    range=[0, 0.2],
    tickformat='.2f',
    ticksuffix=' in',
    row=3,
    col=1,
    secondary_y=True
)

# Humidity
dashboard.add_trace(make_indicator_plot(
    value=float(cond['relative_humidity']),
    unit=' %',
    min=0,
    max=100,
    color='#37916e'),
    row=3,
    col=2)

# Wind Speed
dashboard.add_trace(make_indicator_plot(
    value=float(cond['wind_mph']),
    unit=' mph',
    min=0,
    max=float(cond['davis_current_observation']['wind_year_high_mph']),
    color='#37916e'),
    row=4,
    col=1)

# Wind Direction
dashboard.add_trace(make_barpolar_plot(
    angle=cond['wind_degrees']),
    row=4,
    col=2)

dashboard.update_polars(
    angularaxis_direction='clockwise',
    radialaxis_visible=False,
    row=4,
    col=2
)

# Customize the dashboard
dashboard.update_annotations(
    font_family='Inria Serif',
    font_size=32
)

dashboard.update_layout(
    font_color='#000',
    font_family='Kanit',
    height=2300,
    paper_bgcolor='#fff',
    plot_bgcolor='#fff',
    showlegend=False
)

dashboard.update_xaxes(
    tickfont_color='#000',
)

dashboard.update_yaxes(
    tickfont_color='#000',
)

st.plotly_chart(dashboard)