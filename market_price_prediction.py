import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("harga_real.csv")
    #data['Tanggal'] = pd.to_datetime(data['Tanggal'])  # Parse the date column as datetime
    return data

# Sidebar: Select commodities
st.sidebar.title("Pilih Komoditas")
commodities = st.sidebar.multiselect("Pilih satu atau lebih komoditas", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

# Date range granularity options
granularity = st.sidebar.selectbox("Pilih Granularitas Tanggal", ["Harian", "Mingguan", "Bulanan", "Tahunan"])

# Main content
st.title("Peramalan Harga Komoditas Harian")

# Load data
data = load_data()

if len(commodities) > 0:
    # Filter data based on selected commodities
    selected_data = data[['Tanggal'] + commodities]
    selected_data = selected_data.sort_values(by='Tanggal', ascending=False)
    
    st.subheader("Harga Komoditas")
    st.write(selected_data.set_index('Tanggal'))

    # Plot selected commodities
    st.subheader("Grafik Harga Komoditas")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for commodity in commodities:
        ax.plot(selected_data['Tanggal'], selected_data[commodity], label=commodity)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga")
    ax.set_title("Harga Komoditas Antar Waktu")
    ax.legend()
    
    # Determine granularity multiplier
    if granularity == "Harian":
        granularity_multiplier = 1
    elif granularity == "Mingguan":
        granularity_multiplier = 7
    elif granularity == "Bulanan":
        granularity_multiplier = 30  # Approximate number of days in a month
    else:
        granularity_multiplier = 365  # Approximate number of days in a year
    
    # Calculate slider limits
    min_date = selected_data['Tanggal'].min()
    max_date = selected_data['Tanggal'].max()
    x_min = st.date_input("Pilih Rentang Tanggal Awal", min_date, min_date, max_date - pd.DateOffset(days=1))
    x_max = st.date_input("Pilih Rentang Tanggal Akhir", min_date + pd.DateOffset(days=granularity_multiplier), min_date, max_date)
    
    # Filter data based on the selected date range
    filtered_data = selected_data[(selected_data['Tanggal'] >= x_min) & (selected_data['Tanggal'] <= x_max)]
    
    # Update the plot with the filtered data
    for commodity in commodities:
        ax.plot(filtered_data['Tanggal'], filtered_data[commodity], label=commodity)
    
    # Set x-axis limits
    ax.set_xlim(x_min, x_max)
    
    st.pyplot(fig)
    
    # Forecasting period
    st.subheader("Peramalan Harga Komoditas")
    forecasting_period = st.number_input("Masukan periode peramalan (dalam hari):", min_value=1, step=1)
    if st.button("Forecast"):
        # Perform your forecasting calculations here using the selected commodities and the forecasting period
        st.write(f"Peramalan {forecasting_period} hari untuk komoditas terpilih")

else:
    st.warning("Silakan pilih satu atau lebih komoditas.")
