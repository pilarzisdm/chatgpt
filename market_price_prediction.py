import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("harga.csv")
    return data

# Sidebar: Select commodities
st.sidebar.title("Select Commodities")
commodities = st.sidebar.multiselect("Select one or more commodities", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

# Main content
st.title("Daily Commodity Price Forecasting")

# Load data
data = load_data()

if len(commodities) > 0:
    # Filter data based on selected commodities
    selected_data = data[['Tanggal'] + commodities]
    st.subheader("Commodity Prices")
    st.write(selected_data.set_index('Tanggal'))

    # Plot selected commodities
    st.subheader("Commodity Price Chart")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for commodity in commodities:
        ax.plot(selected_data['Tanggal'], selected_data[commodity], label=commodity)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Commodity Prices Over Time")
    ax.legend()
    st.pyplot(fig)
    
    # Forecasting period
    st.subheader("Commodity Price Forecasting")
    forecasting_period = st.number_input("Enter the forecasting period (in days):", min_value=1, step=1)
    if st.button("Forecast"):
        # Perform your forecasting calculations here using the selected commodities and the forecasting period
        st.write(f"Forecasting for the next {forecasting_period} days for selected commodities")

else:
    st.warning("Please select one or more commodities from the sidebar.")

