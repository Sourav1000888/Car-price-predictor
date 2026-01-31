import streamlit as st
import joblib 
import pandas as pd
import numpy as np
from datetime import datetime


column = joblib.load('feature.pkl')
model = joblib.load('pipe.pkl')


# Car prediction function
def predict_car_price(car_name, car_model, location, kms_driven, fuel_type, year):
    prediction = model.predict(pd.DataFrame([[car_model, location, kms_driven, fuel_type, year, car_name]], 
                    columns=['Name', 'Location', 'Kms_driven', 'Fuel_type', 'Year', 'Company']))[0]
    return prediction


# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Header
st.title("🚗 Car Price Prediction App")
st.markdown("Predict used car prices based on brand, model, location, and features.")

# Sidebar
st.sidebar.header("Quick Actions")
if st.sidebar.button("New Prediction"):
    st.rerun()

# Slider filter
st.sidebar.header("Filters")
currency = st.sidebar.selectbox("Currency", ["INR", "USD"])  # Optional


# Main Content with Tabs
tab1, tab2 = st.tabs(["Predict", "History"])

# Predict tab
with tab1:
    st.header("Enter Car Details")
    
    # Input fields
    car_name = st.selectbox("Car Name (Brand)", sorted(set(column['Company'])))
    same_car = []
    for i in column['Name']:
        if car_name in i.split():
            same_car.append(i)
    car_model = st.selectbox("Car Model", set(same_car))
    location = st.selectbox("Location", sorted(set(column['Location'])))
    kms_driven = st.selectbox("Kms Driven", sorted(set(column['Kms_driven'])))
    fuel_type = st.selectbox("Fuel Type", sorted(set(column['Fuel_type'])))
    year = st.selectbox("Year of Manufacture", sorted(set(column['Year'])))
    
    #predict button
    if st.button("Predict Price"):
        predicted_price = predict_car_price(car_name, car_model, location, kms_driven, fuel_type, year)
        if currency == "INR":
            st.success(f"Predicted Price: ₹{round(np.expm1(predicted_price), 2)} INR")
        elif currency == 'USD':
            st.success(f"Predicted Price: ${round(np.expm1(predicted_price)*0.010894, 2)} USD")
        
        # Display details
        st.subheader("Prediction Details")
        st.write(f"**Car Name:** {car_name}")
        st.write(f"**Car Model:** {car_model}")
        st.write(f"**Location:** {location}")
        st.write(f"**Kms Driven:** {kms_driven}")
        st.write(f"**Fuel Type:** {fuel_type}")
        st.write(f"**Year:** {year}")
        
        # Add to history
        st.session_state.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "car_name": car_name,
            "car_model": car_model,
            "location": location,
            "kms_driven": kms_driven,
            "fuel_type": fuel_type,
            "year": year,
            "predicted_price": f'{round(np.expm1(predicted_price), 2)} INR' if currency == 'INR' else  f'{round(np.expm1(predicted_price)*0.010894, 2)} USD'
        })

# History tab
with tab2:
    st.header("Prediction History")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        # Clear history button
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No history yet.")

