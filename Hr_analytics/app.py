# app.py
import streamlit as st
import pickle
import pandas as pd

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="HR Attrition Prediction", layout="centered")

st.title("HR Attrition Prediction")
st.write("Enter employee details to predict whether the employee will leave the company.")

# User Inputs
satisfaction_level = st.slider("Satisfaction Level", 0.0, 1.0, 0.5)
last_evaluation = st.slider("Last Evaluation", 0.0, 1.0, 0.5)
number_project = st.slider("Number of Projects", 1, 10, 3)
average_monthly_hours = st.slider("Average Monthly Hours", 50, 350, 160)
time_spend_company = st.slider("Years at Company", 1, 15, 3)
work_accident = st.selectbox("Work Accident", [0, 1])
promotion_last_5years = st.selectbox("Promotion in Last 5 Years", [0, 1])

sales = st.selectbox(
    "Department",
    [
        "IT",
        "RandD",
        "accounting",
        "hr",
        "management",
        "marketing",
        "product_mng",
        "sales",
        "support",
        "technical"
    ]
)

salary = st.selectbox(
    "Salary Level",
    ["low", "medium", "high"]
)

# Create dataframe
input_data = pd.DataFrame({
    'satisfaction_level': [satisfaction_level],
    'last_evaluation': [last_evaluation],
    'number_project': [number_project],
    'average_montly_hours': [average_monthly_hours],
    'time_spend_company': [time_spend_company],
    'Work_accident': [work_accident],
    'promotion_last_5years': [promotion_last_5years],
    'sales': [sales],
    'salary': [salary]
})

# Convert categorical columns
input_data = pd.get_dummies(input_data)

# Training columns used in model
model_columns = [
    'satisfaction_level',
    'last_evaluation',
    'number_project',
    'average_montly_hours',
    'time_spend_company',
    'Work_accident',
    'promotion_last_5years',
    'sales_RandD',
    'sales_accounting',
    'sales_hr',
    'sales_management',
    'sales_marketing',
    'sales_product_mng',
    'sales_sales',
    'sales_support',
    'sales_technical',
    'salary_low',
    'salary_medium'
]

# Add missing columns
for col in model_columns:
    if col not in input_data.columns:
        input_data[col] = 0

# Reorder columns
input_data = input_data[model_columns]

# Prediction
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"Employee is likely to leave the company.\nProbability: {probability:.2f}")
    else:
        st.success(f"Employee is likely to stay in the company.\nProbability: {1 - probability:.2f}")