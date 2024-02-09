import streamlit as st
import time
from datetime import datetime
import pytz
from forex_python.converter import CurrencyRates
import yfinance as yf

st.title("World Clock App")
unix_timestamp = int(time.time())

timezones = pytz.all_timezones
selected_timezones = st.multiselect("Select up to 4 timezones", timezones, default=["UTC"])


c = CurrencyRates()


placeholders = [st.empty() for _ in range(len(selected_timezones) * 4)]
unix_timestamp_placeholder = st.sidebar.empty()


st.sidebar.title("UNIX Timestamp Converter")
unix_input = st.sidebar.number_input("Enter UNIX Timestamp:", value=unix_timestamp, step=1)


if st.sidebar.button("Convert"):
    human_time = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    st.sidebar.write(f"Converted Human Time: {human_time}")


while True:
    all_data = []
    
    for timezone in selected_timezones:
        current_time = datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')

        try:
            forex_rate = c.get_rate('USD', 'CNY')
        except Exception as e:
            forex_rate = f"Error: {e}"

        try:
            stock_data = yf.Ticker('AAPL')
            stock_price = stock_data.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            stock_price = f"Error: {e}"

        all_data.append((timezone, current_time, forex_rate, stock_price))

    for i, (timezone, current_time, forex_rate, stock_price) in enumerate(all_data):
        placeholders[i * 4].text(f"--- {timezone} ---")  # Separator
        placeholders[i * 4 + 1].text(f"Time: {current_time}")
        placeholders[i * 4 + 2].text(f"Exchange rate: {forex_rate}")
        placeholders[i * 4 + 3].text(f"Stock price: {stock_price}")
        unix_timestamp = int(time.time())
        unix_timestamp_placeholder.text(f"UNIX Timestamp: {unix_timestamp}")


    time.sleep(1)

