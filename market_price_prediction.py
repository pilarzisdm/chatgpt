import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
@st.cache
def load_data():
    data = pd.read_csv("harga.csv")
    return data

# Sidebar: Select commodities
st.sidebar.title("Pilih Komoditas")
commodities = st.sidebar.multiselect("Pilih satu atau lebih komoditas", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

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
    
    # Add slider for x-axis limits
    x_min, x_max = st.slider("Pilih Rentang Tanggal", min(selected_data['Tanggal']), max(selected_data['Tanggal']), (min(selected_data['Tanggal']), max(selected_data['Tanggal'])))
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
