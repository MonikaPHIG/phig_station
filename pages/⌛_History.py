import streamlit as st
import json, requests
from urllib.parse import urlencode, urlunparse

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
st.markdown('# Historical Data')

st.markdown('🚧 Coming soon... 🚧')