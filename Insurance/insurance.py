import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="Insurance Prediction App",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# TITLE & DESCRIPTION
# -----------------------------------
st.title("📊 Insurance Purchase Prediction App")
st.markdown("""
This app predicts whether a person will buy insurance based on their age.
**Upload your CSV file** with columns: `age` and `bought_insurance`
- `bought_insurance`: 0 = No, 1 = Yes
""")

# -----------------------------------
# FILE UPLOAD SECTION
# -----------------------------------
st.sidebar.header("📁 Data Upload")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Upload a CSV file with 'age' and 'bought_insurance' columns"
)

# Sample data option
use_sample = st.sidebar.checkbox("Use sample data instead", value=False)

# -----------------------------------
# LOAD DATA BASED ON USER CHOICE
# -----------------------------------
df = None

if use_sample:
    # Create sample data
    st.sidebar.info("Using sample data...")
    sample_data = {
        'age': [22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60],
        'bought_insurance': [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]
    }
    df = pd.DataFrame(sample_data)
    st.success("✅ Using sample data")
    
elif uploaded_file is not None:
    # Read the uploaded file
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ File uploaded successfully! Found {len(df)} records")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    # No file uploaded and no sample data selected
    st.info("👈 Please upload a CSV file or check 'Use sample data' to begin")
    st.stop()

# -----------------------------------
# DATA VALIDATION
# -----------------------------------
# Check required columns
required_columns = ['age', 'bought_insurance']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"❌ Missing required columns: {missing_columns}")
    st.write("Your file has these columns:", list(df.columns))
    st.write("Required columns: 'age' and 'bought_insurance'")
    st.stop()

# Check data types
if not pd.api.types.is_numeric_dtype(df['age']):
    st.error("❌ 'age' column must contain numeric values")
    st.stop()

if not pd.api.types.is_numeric_dtype(df['bought_insurance']):
    st.error("❌ 'bought_insurance' column must contain numeric values (0 or 1)")
    st.stop()

# Check binary values
unique_values = df['bought_insurance'].unique()
if not all(val in [0, 1] for val in unique_values):
    st.error(f"❌ 'bought_insurance' should only contain 0 and 1. Found: {unique_values}")
    st.stop()

# -----------------------------------
# DATA PREVIEW
# -----------------------------------
st.subheader("📋 Data Preview")
col1, col2 = st.columns(2)

with col1:
    st.write("**First 5 rows:**")
    st.dataframe(df.head())

with col2:
    st.write("**Dataset Info:**")
    st.write(f"- Total records: {len(df)}")
    st.write(f"- Age range: {df['age'].min()} - {df['age'].max()}")
    st.write(f"- Insurance buyers: {df['bought_insurance'].sum()} ({df['bought_insurance'].mean()*100:.1f}%)")
    st.write(f"- Non-buyers: {len(df) - df['bought_insurance'].sum()}")

# -----------------------------------
# VISUALIZATION
# -----------------------------------
st.subheader("📊 Data Visualization")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Age distribution
axes[0].hist(df['age'], bins=10, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Age Distribution')

# Insurance purchase by age
buyers = df[df['bought_insurance'] == 1]['age']
non_buyers = df[df['bought_insurance'] == 0]['age']

axes[1].hist([buyers, non_buyers], bins=10, label=['Buyers', 'Non-buyers'], 
             alpha=0.7, edgecolor='black')
axes[1].set_xlabel('Age')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Insurance Purchase by Age')
axes[1].legend()

st.pyplot(fig)

# -----------------------------------
# PREPARE DATA FOR MODELING
# -----------------------------------
X = df[['age']]
y = df['bought_insurance']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------------
# TRAIN MODELS
# -----------------------------------
# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Logistic Regression
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

# Predictions
logistic_pred = logistic_model.predict(X_test)
accuracy = accuracy_score(y_test, logistic_pred)

# -----------------------------------
# MODEL PERFORMANCE
# -----------------------------------
st.subheader("🎯 Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model Accuracy", f"{accuracy*100:.2f}%")

with col2:
    st.metric("Logistic Regression Coef", f"{logistic_model.coef_[0][0]:.3f}")

with col3:
    st.metric("Intercept", f"{logistic_model.intercept_[0]:.3f}")

# Show prediction probabilities on test set
st.write("**Confusion Matrix on Test Set:**")
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, logistic_pred)

cm_df = pd.DataFrame(cm, 
                     index=['Actual Non-Buyer', 'Actual Buyer'],
                     columns=['Predicted Non-Buyer', 'Predicted Buyer'])
st.dataframe(cm_df)

# -----------------------------------
# PREDICTION INTERFACE
# -----------------------------------
st.subheader("🔮 Make Predictions")

col1, col2 = st.columns([1, 1])

with col1:
    age = st.slider(
        "Select Age",
        min_value=int(df['age'].min()),
        max_value=int(df['age'].max()),
        value=int(df['age'].median()),
        step=1
    )

with col2:
    threshold = st.slider(
        "Decision Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Adjust this to change sensitivity (lower = more likely to predict 'buy')"
    )

# Make prediction
test_age = [[age]]
prediction = logistic_model.predict(test_age)
probability = logistic_model.predict_proba(test_age)

# Apply custom threshold
custom_prediction = 1 if probability[0][1] > threshold else 0

# Display results
st.markdown("---")
st.subheader("📈 Prediction Results")

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:
    st.write("**Selected Age:**")
    st.write(f"## {age}")

with result_col2:
    st.write("**Prediction (Default):**")
    if prediction[0] == 1:
        st.success("✅ Will Buy Insurance")
    else:
        st.error("❌ Will Not Buy Insurance")

with result_col3:
    st.write(f"**Using {threshold:.0%} Threshold:**")
    if custom_prediction == 1:
        st.success("✅ Will Buy Insurance")
    else:
        st.error("❌ Will Not Buy Insurance")

# Probability meter
st.write("**Purchase Probability:**")
prob_percent = probability[0][1] * 100
st.progress(int(prob_percent))
st.write(f"### {prob_percent:.1f}% chance of buying insurance")

# Add interpretation
if prob_percent >= 70:
    st.success("📈 High likelihood of purchasing insurance")
elif prob_percent >= 40:
    st.warning("📊 Moderate likelihood - additional factors may influence decision")
else:
    st.error("📉 Low likelihood of purchasing insurance")

# -----------------------------------
# DOWNLOAD PREDICTIONS
# -----------------------------------
st.subheader("💾 Download Predictions")

if st.button("Generate Predictions for All Ages"):
    age_range = np.arange(int(df['age'].min()), int(df['age'].max()) + 1).reshape(-1, 1)
    all_predictions = logistic_model.predict(age_range)
    all_probabilities = logistic_model.predict_proba(age_range)
    
    results_df = pd.DataFrame({
        'age': age_range.flatten(),
        'buys_insurance': all_predictions,
        'probability': all_probabilities[:, 1]
    })
    
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Predictions CSV",
        data=csv,
        file_name="insurance_predictions.csv",
        mime="text/csv"
    )

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.markdown("""
**Note:** This model uses only age to predict insurance purchase. 
For better accuracy, upload more comprehensive data with additional features like income, health status, etc.
""")
