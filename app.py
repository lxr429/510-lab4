import streamlit as st
import pytz
from datetime import datetime
import time

# List of time zones
time_zones = list(pytz.all_timezones)

st.title("World Clock App")

# Multi-select dropdown for time zones
selected_zones = st.multiselect("Choose up to 4 time zones", time_zones, default=["UTC"])

# Placeholder for clocks
clocks_container = st.empty()

while True:
    with clocks_container.container():
        # Display clocks
        for zone in selected_zones:
            tz = pytz.timezone(zone)
            time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            st.metric(zone, time_now)
    time.sleep(1)
