import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
@st.cache
def load_data():
    data = pd.read_csv("harga.csv")
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
    st.write(selected_data.set_index('Tanggal'))

    # Add select box for granularity
    granularity = st.selectbox("Pilih Granularitas Tanggal", ["Harian", "Mingguan", "Bulanan", "Tahunan"])

    # Determine granularity multiplier
    if granularity == "Harian":
        granularity_multiplier = 1
    elif granularity == "Mingguan":
        granularity_multiplier = 7
    elif granularity == "Bulanan":
        granularity_multiplier = 30  # Approximate number of days in a month
    else:
        granularity_multiplier = 365  # Approximate number of days in a year

    # Plot selected commodities with the selected granularity
    st.subheader("Grafik Harga Komoditas")
    fig, ax = plt.subplots(figsize=(10, 5))

    for commodity in commodities:
        filtered_data = selected_data[selected_data['Tanggal'] >= (selected_data['Tanggal'].max() - pd.DateOffset(days=granularity_multiplier))]
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
        # Perform your forecasting calculations here using the selected commodities and the forecasting period
        st.write(f"Peramalan {forecasting_period} hari untuk komoditas terpilih")

else:
    st.warning("Silakan pilih satu atau lebih komoditas.")
