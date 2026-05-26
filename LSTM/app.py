
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

st.set_page_config(page_title="Electricity Forecasting LSTM", layout="wide")

st.title("Electricity Consumption Forecasting using LSTM")
st.write("Upload your electricity consumption dataset to train and predict future power usage.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    # Load Dataset
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Column Selection
    datetime_col = st.selectbox("Select Datetime Column", df.columns)
    target_col = st.selectbox("Select Target Column", df.columns)

    # Convert Datetime
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    st.subheader("Dataset Information")
    st.write(df.describe())

    # Plot Original Data
    st.subheader("Electricity Consumption Visualization")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df[datetime_col][:500], df[target_col][:500])
    ax.set_title("Electricity Consumption")
    ax.set_xlabel("Time")
    ax.set_ylabel("Power Usage")

    st.pyplot(fig)

    # Scaling
    data = df[target_col].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # Time Step
    time_step = st.slider("Select Time Step", 1, 48, 24)

    X = []
    y = []

    for i in range(time_step, len(scaled_data)):
        X.append(scaled_data[i-time_step:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)

    X = X.reshape(X.shape[0], X.shape[1], 1)

    st.write("X Shape:", X.shape)
    st.write("y Shape:", y.shape)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Build Model
    model = Sequential()

    model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], 1)))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')

    st.subheader("Model Summary")
    model_summary = []
    model.summary(print_fn=lambda x: model_summary.append(x))
    st.text("\n".join(model_summary))

    # Training
    epochs = st.slider("Select Epochs", 1, 50, 5)
    batch_size = st.selectbox("Select Batch Size", [16, 32, 64], index=1)

    if st.button("Train Model"):
        history = model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )

        st.success("Model Training Completed")

        # Plot Loss
        st.subheader("Training Loss")

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.legend()

        st.pyplot(fig2)

        # Predictions
        predictions = model.predict(X_test)

        predictions = scaler.inverse_transform(predictions.reshape(-1, 1))
        actual = scaler.inverse_transform(y_test.reshape(-1, 1))

        # Plot Predictions
        st.subheader("Actual vs Predicted Electricity Consumption")

        fig3, ax3 = plt.subplots(figsize=(12, 5))

        ax3.plot(actual[:200], label='Actual Consumption')
        ax3.plot(predictions[:200], label='Predicted Consumption')

        ax3.set_title("Actual vs Predicted Electricity Consumption")
        ax3.set_xlabel("Samples")
        ax3.set_ylabel("Power Usage")
        ax3.legend()

        st.pyplot(fig3)
