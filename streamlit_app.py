import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    h1 {
        color: #00ffcc;
        text-align: center;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dynamic path
model_path = os.path.join(os.path.dirname(__file__), "loan_approval_model.pkl")
model = joblib.load(model_path)

st.title("Loan Approval Prediction")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        Gender = st.selectbox("Gender", ["Male", "Female"])
        Married = st.selectbox("Married", ["Yes", "No"])
        ApplicantIncome = st.number_input("Applicant Income")
        LoanAmount = st.number_input("Loan Amount")
        Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        Property_Area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])
    with col2:
        CoapplicantIncome = st.number_input("Coapplicant Income")
        Loan_Amount_Term = st.number_input("Loan Amount Term")
        Credit_History = st.number_input("Credit History")
        Self_Employed = st.selectbox("Self Employed", ["Yes", "No"])
        Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])

# Convert inputs to model format — update this preprocessing as per your dataset
gender_num = 1 if Gender == "Male" else 0
married_num = 1 if Married == "Yes" else 0
education_num = 1 if Education == "Not Graduate" else 0
self_employed_num = 1 if Self_Employed == "Yes" else 0
property_area_semiurban = 1 if Property_Area == "Semiurban" else 0
property_area_urban = 1 if Property_Area == "Urban" else 0
Dependent_1_count = 1 if Dependents == "1" else 0
Dependent_2_count = 2 if Dependents == "2" else 0
Dependent_3_above_count = 1 if Dependents == "3+" else 0

# Cr

if st.button("Predict"):
  # Create a dictionary with column names as keys and user inputs as values
  input_dict = {
      'ApplicantIncome': [ApplicantIncome],
      'CoapplicantIncome': [CoapplicantIncome],
      'LoanAmount': [LoanAmount],
      'Loan_Amount_Term': [Loan_Amount_Term],
      'Credit_History': [Credit_History],
      'Gender_Male': [gender_num],
      'Married_Yes': [married_num],
      'Education_Not Graduate': [education_num],
      'Self_Employed_Yes': [self_employed_num],
      'Property_Area_Semiurban': [property_area_semiurban],
      'Property_Area_Urban': [property_area_urban],
      'Dependents_1': [Dependent_1_count],
      'Dependents_2': [Dependent_2_count],
      'Dependents_3+': [Dependent_3_above_count]
  }

  # Convert dictionary to DataFrame
  input_df = pd.DataFrame(input_dict)

  # Predict using the model
  prediction = model.predict(input_df)[0]
  if prediction == 1:
    st.success("Loan Status: Approved")
  else:
    st.error("Loan Status: Rejected")

