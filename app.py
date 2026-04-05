import streamlit as st
import pandas as pd
import joblib

# Load the model, scaler, and columns
model = joblib.load('heart_disease_model.pkl')
scaler = joblib.load('scaler.pkl')
expected_columns = joblib.load('columns.pkl')


st.title("Heart Disease Predictor")
st.markdown("Enter the following details to predict the likelihood of heart disease:")  

# Create input fields for each feature
age = st.slider("Age", min_value=18, max_value=100, value=40)
sex = st.selectbox("Sex", options=['F', 'M'])
chest_pain = st.selectbox("Chest Pain Type", options=["ATA", "NAP", "TA", "ASY"])
resting_bp = st.number_input("Resting Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1])
resting_ecg = st.selectbox("Resting ECG Results", options=["Normal", "ST", "LVH"])
max_hr = st.slider("Maximum Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=150)
exercise_angina = st.selectbox("Exercise Induced Angina", options=["Y", "N"])
oldpeak = st.slider("Oldpeak (ST Depression)", min_value=0.0, max_value=6.0, value=1.0)
st_slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])


# When the user clicks the "Predict" button, create a raw input dictionary and preprocess it
if st.button("Predict"):
    
    # Create a raw input dictionary
    raw_input = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,
        'Sex_' + sex: 1,
        'ChestPainType_' + chest_pain: 1,
        'RestingECG_' + resting_ecg: 1,
        'ExerciseAngina_' + exercise_angina: 1,
        'ST_Slope_' + st_slope: 1
    }

    # Create a DataFrame and ensure all columns are present
    input_df = pd.DataFrame([raw_input])

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[expected_columns]
    
    # Scale the input features
    scaled_input = scaler.transform(input_df)

    # Make a prediction
    prediction = model.predict(scaled_input)[0]

    # Display the result
    if prediction == 1:
        st.error("You are likely to have heart disease. Please consult a healthcare professional for further evaluation.")
    else:
        st.success("You are unlikely to have heart disease. However, please maintain a healthy lifestyle and consult a healthcare professional for regular check-ups.")
