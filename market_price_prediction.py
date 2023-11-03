import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("harga_real.csv")
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])  # Parse the date column as datetime
    return data

# Sidebar: Select commodities
st.sidebar.title("Pilih Komoditas")
commodities = st.sidebar.multiselect("Pilih satu atau lebih komoditas", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

# Main content
st.title("Peramalan Harga Komoditas Harian")

# Load data
data = load_data()

# Filter data based on selected commodities
if len(commodities) > 0:
    selected_data = data[['Tanggal'] + commodities]
    selected_data = selected_data.sort_values(by='Tanggal', ascending=False)

    st.subheader("Harga Komoditas")
    selected_data['Tanggal'] = selected_data['Tanggal'].dt.date  # Extract date portion
    st.write(selected_data.set_index('Tanggal'))

    # Add select box for granularity just for the plot
    granularity = st.selectbox("Pilih Granularitas Tanggal untuk Grafik", ["Mingguan", "Bulanan", "Tahunan"])

    # Determine granularity multiplier
    if granularity == "Mingguan":
        granularity_multiplier = pd.DateOffset(weeks=1)
    elif granularity == "Bulanan":
        granularity_multiplier = pd.DateOffset(months=1)
    else:
        granularity_multiplier = pd.DateOffset(years=1)

    # Calculate the date range for the selected granularity
    max_date = selected_data['Tanggal'].max()
    min_date = max_date - granularity_multiplier

    # Filter data for the selected granularity
    min_date = pd.Timestamp(min_date)  # Convert to Timestamp
    filtered_data = selected_data[selected_data['Tanggal'] >= min_date]

    # Plot selected commodities with the selected granularity
    st.subheader("Grafik Harga Komoditas")
    fig, ax = plt.subplots(figsize=(10, 5))

    for commodity in commodities:
        ax.plot(filtered_data['Tanggal'], filtered_data[commodity], label=commodity)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga")
    ax.set_title("Harga Komoditas Antar Waktu")
    ax.legend()

    st.pyplot(fig)

    # Forecasting period
    st.subheader("Peramalan Harga Komoditas")
    forecasting_period = st.number_input("Masukan periode peramalan (dalam hari):", min_value=1, step=1)
    if st.button("Forecast"):
        # Perform time series forecasting using Prophet
        forecast_data = selected_data[['Tanggal', 'Beras']].rename(columns={'Tanggal': 'ds', 'Beras': 'y'})

        # Create and fit the Prophet model
        model = Prophet()
        model.fit(forecast_data)

        # Create a dataframe for future dates
        future = model.make_future_dataframe(periods=forecasting_period)
        
        # Make predictions
        forecast = model.predict(future)

        # Display the forecasted data
        st.subheader("Hasil Peramalan")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

else:
    st.warning("Silakan pilih satu atau lebih komoditas.")
