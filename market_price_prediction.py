import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load your dataset (change 'your_dataset.csv' to your file's name)
@st.cache(persist=True)
def load_data():
    data = pd.read_csv('rice.prices.csv')
    return data

data = load_data()

st.title('Market Price Forecasting App')

# Sidebar
st.sidebar.header('Data Settings')
features = st.sidebar.multiselect('Select Features', data.columns)

# Choose features (independent variables) and the target (dependent variable)
if not features:
    st.warning('Please select at least one feature.')
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

    st.subheader('Model Evaluation')
    st.write(f"Mean Squared Error: {mse}")
    st.write(f"R-squared: {r2}")

    # Plot the actual vs. predicted prices
    st.subheader('Actual vs. Predicted Prices')
    st.pyplot(plt.scatter(y_test, predictions))

    # Market Price Forecast
    st.subheader('Market Price Forecast')
    user_input = st.text_input('Enter feature values separated by commas')
    user_input = [float(x.strip()) for x in user_input.split(',')]  # Convert to a list of floats

    if len(user_input) == len(features):
        forecast = model.predict([user_input])
        st.write(f"Forecasted Price: {forecast[0]}")
