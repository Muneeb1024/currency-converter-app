import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set up the app title
st.set_page_config(page_title="💰 Advanced Currency Converter", layout="wide")
st.title("💰 Advanced Currency Converter")

# API for live exchange rates
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Function to fetch real-time exchange rates
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_exchange_rates():
    response = requests.get(API_URL)
    return response.json()

data = get_exchange_rates()
currencies = list(data["rates"].keys())

# UI Elements
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From Currency", currencies)

with col2:
    to_currencies = st.multiselect("Convert To", currencies, default=["EUR", "GBP", "INR"])

amount = st.number_input("Enter Amount", min_value=0.01, format="%.2f")

# Convert button
if st.button("Convert"):
    st.subheader(f"Conversion Results for {amount} {from_currency}:")
    results = []
    for currency in to_currencies:
        rate = data["rates"][currency] / data["rates"][from_currency]
        converted_amount = amount * rate
        results.append((currency, converted_amount))
        st.write(f"➡️ **{converted_amount:.2f} {currency}**")

# 🌍 **Historical Exchange Rate Feature**
st.sidebar.title("📊 Currency Trends")
selected_currency = st.sidebar.selectbox("Select Currency to View Trends", currencies)

if st.sidebar.button("Show Historical Data"):
    # Fetch historical data (last 7 days)
    historical_data = []
    for i in range(7):
        date = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"https://api.exchangerate-api.com/v4/{date}/USD"
        try:
            response = requests.get(url)
            rate = response.json()["rates"][selected_currency]
            historical_data.append((date, rate))
        except:
            pass

    # Convert to DataFrame
    df = pd.DataFrame(historical_data, columns=["Date", "Exchange Rate"])
    df = df.sort_values("Date")

    # Plot the historical rates
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Exchange Rate"], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Exchange Rate (1 USD to {selected_currency})")
    ax.set_title(f"📈 Exchange Rate Trend for {selected_currency}")

    st.sidebar.pyplot(fig)
