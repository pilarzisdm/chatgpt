import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io

# Load your dataset (change 'your_dataset.csv' to your file's name)
@st.cache_data
def load_data():
    data = pd.read_csv('data_harga.csv')
    return data

data = load_data()

st.title('Web Peramalan Harga Komoditas')

# Sidebar
#st.sidebar.header('Data Settings')
features = st.sidebar.multiselect('Pilih Data', data.columns)

# Choose features (independent variables) and the target (dependent variable)
if not features:
    st.warning('Silakan pilih minimal satu komoditas.')
else:
    target = st.sidebar.selectbox('Select Target', data.columns)

    # Split the data into training and testing sets
    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model (you may want to use different metrics)
    from sklearn.metrics import mean_squared_error, r2_score
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    st.subheader('Evaluasi Model')
    st.write(f"Mean Squared Error: {mse}")
    st.write(f"R-squared: {r2}")

    # Plot the actual vs. predicted prices
    fig, ax = plt.subplots()
    ax.scatter(y_test, predictions)
    ax.set_xlabel("Harga Aktual")
    ax.set_ylabel("Harga Prediksi")
    ax.set_title("Harga Aktual vs Harga Prediksi")

    # Save the plot to a BytesIO object
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    st.image(img_buf)

    # Market Price Forecast
    st.subheader('Peramalan Harga Komoditas')
    user_input = st.text_input('Silakan masukan nilai')

    if user_input:
        try:
            user_input = [float(x.strip()) for x in user_input.split(',')]  # Convert to a list of floats
            if len(user_input) == len(features):
                forecast = model.predict([user_input])
                st.write(f"Harga Prediksi: {forecast[0]}")
            else:
                st.warning(f"Please provide {len(features)} feature values.")
        except ValueError:
            st.warning("Format input salah. Silakan memasukan format numerik.")

