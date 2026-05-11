import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv("insurance_data.csv")

X = df[['age']]
y = df['bought_insurance']

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------------
# LINEAR REGRESSION
# -----------------------------------

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_pred = linear_model.predict(X)

# -----------------------------------
# LOGISTIC REGRESSION
# -----------------------------------

logistic_model = LogisticRegression()

logistic_model.fit(X_train, y_train)

logistic_output = logistic_model.predict(X_test)

# -----------------------------------
# ACCURACY
# -----------------------------------

accuracy = accuracy_score(y_test, logistic_output)

# -----------------------------------
# STREAMLIT UI
# -----------------------------------

st.title("Insurance Prediction App")

st.write("Model Accuracy:",
         round(accuracy * 100,2),
         "%")

# -----------------------------------
# AGE INPUT
# -----------------------------------

age = st.slider(
    "Enter Age",
    18,
    60,
    30
)

test_age = [[age]]

prediction = logistic_model.predict(test_age)

probability = logistic_model.predict_proba(test_age)

# -----------------------------------
# PREDICTION OUTPUT
# -----------------------------------

st.write("Selected Age:", age)

if prediction[0] == 1:
    st.success("Bought Insurance")
else:
    st.error("Did Not Buy Insurance")

st.write(
    "Probability of Buying:",
    round(probability[0][1] * 100,2),
    "%"
)