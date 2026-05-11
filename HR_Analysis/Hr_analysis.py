import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="HR Employee Retention Analytics",
    page_icon="👥",
    layout="wide"
)

# -----------------------------------
# TITLE & DESCRIPTION
# -----------------------------------
st.title("👥 HR Employee Retention Analytics")
st.markdown("""
This app analyzes employee retention using logistic regression. 
Upload your HR dataset or use the sample data to predict whether employees leave the company.
""")

# -----------------------------------
# SIDEBAR - DATA UPLOAD
# -----------------------------------
st.sidebar.header("📁 Data Upload")

# Option to use sample data
use_sample = st.sidebar.checkbox("Use sample HR data", value=True)

uploaded_file = st.sidebar.file_uploader(
    "Or upload your own CSV file",
    type=['csv'],
    help="Upload HR dataset with employee information"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = None

if use_sample:
    # Create sample data matching the HR dataset structure
    np.random.seed(42)
    n_samples = 15000
    
    sample_data = {
        'satisfaction_level': np.random.uniform(0.2, 1.0, n_samples),
        'last_evaluation': np.random.uniform(0.5, 1.0, n_samples),
        'number_project': np.random.choice([2,3,4,5,6], n_samples),
        'average_montly_hours': np.random.choice([150, 160, 180, 200, 220, 250, 280], n_samples),
        'time_spend_company': np.random.choice([2,3,4,5,6,7,8], n_samples),
        'Work_accident': np.random.choice([0,1], n_samples, p=[0.85, 0.15]),
        'promotion_last_5years': np.random.choice([0,1], n_samples, p=[0.95, 0.05]),
        'sales': np.random.choice(['sales', 'technical', 'support', 'IT', 'product_mng', 
                                   'marketing', 'RandD', 'accounting', 'hr', 'management'], n_samples),
        'salary': np.random.choice(['low', 'medium', 'high'], n_samples, p=[0.4, 0.45, 0.15])
    }
    
    df = pd.DataFrame(sample_data)
    
    # Generate 'left' column based on patterns
    df['left'] = ((df['satisfaction_level'] < 0.5) & 
                  (df['average_montly_hours'] > 250) & 
                  (df['time_spend_company'] > 3)).astype(int)
    
    # Add some randomness
    df['left'] = df['left'] | (np.random.random(n_samples) < 0.1)
    df['left'] = df['left'].astype(int)
    
    st.success("✅ Using sample HR dataset")

elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ File uploaded successfully! Found {len(df)} records")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    st.info("👈 Please check 'Use sample HR data' or upload a CSV file to begin")
    st.stop()

# -----------------------------------
# DATA PREVIEW & INFO
# -----------------------------------
st.header("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Employees", f"{len(df):,}")

with col2:
    left_count = df['left'].sum()
    st.metric("Employees Who Left", f"{left_count:,}", 
              delta=f"{left_count/len(df)*100:.1f}%")

with col3:
    stayed_count = len(df) - left_count
    st.metric("Employees Who Stayed", f"{stayed_count:,}")

# Data preview tabs
tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "ℹ️ Data Info", "🔍 Missing Values"])

with tab1:
    st.dataframe(df.head(100))
    st.caption(f"Showing first 100 rows of {len(df)} total rows")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Column Names & Data Types**")
        dtype_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Data Type': df.dtypes.values
        })
        st.dataframe(dtype_df)
    with col2:
        st.write("**Statistical Summary**")
        st.dataframe(df.describe())

with tab3:
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing Percentage': missing_percent
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    if len(missing_df) > 0:
        st.dataframe(missing_df)
    else:
        st.success("✅ No missing values found!")

# -----------------------------------
# EXPLORATORY DATA ANALYSIS
# -----------------------------------
st.header("📈 Exploratory Data Analysis")

# 1. Salary vs Retention
st.subheader("💰 Impact of Salary on Employee Retention")

fig1, axes = plt.subplots(1, 2, figsize=(14, 5))

# FIXED: Use color palette correctly with proper mapping
salary_order = ['low', 'medium', 'high']

# Method 1: Use built-in palette names instead of dictionary
sns.countplot(data=df, x='salary', hue='left', 
              order=salary_order, 
              palette={0: '#ff6b6b', 1: '#6bcf7f'},  # Using Python ints
              ax=axes[0])
axes[0].set_title('Salary Level vs Employee Retention', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Salary Level')
axes[0].set_ylabel('Employee Count')
axes[0].legend(title='Left Company', labels=['Stayed (0)', 'Left (1)'])

# OR alternative: Use standard seaborn palettes (uncomment to use)
# sns.countplot(data=df, x='salary', hue='left', 
#               order=salary_order, 
#               palette='Set1',  # This works without dictionary
#               ax=axes[0])

# Percentage plot
salary_left_pct = df.groupby('salary')['left'].mean() * 100
colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
bars = axes[1].bar(salary_order, salary_left_pct, color=colors)
axes[1].set_title('Percentage Who Left by Salary Level', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Salary Level')
axes[1].set_ylabel('Left Company (%)')
axes[1].set_ylim(0, 100)

# Add percentage labels on bars
for bar, pct in zip(bars, salary_left_pct):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                 f'{pct:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
st.pyplot(fig1)

# 2. Department vs Retention
st.subheader("🏢 Department vs Employee Retention")

fig2 = plt.figure(figsize=(14, 6))

# Calculate percentages for better visualization
dept_stats = df.groupby('sales')['left'].agg(['count', 'mean'])
dept_stats['left_pct'] = dept_stats['mean'] * 100
dept_stats = dept_stats.sort_values('left_pct', ascending=False)

# Create bar chart
colors = plt.cm.RdYlGn_r(dept_stats['left_pct'] / 100)
bars = plt.bar(range(len(dept_stats)), dept_stats['left_pct'], color=colors, edgecolor='black')
plt.xticks(range(len(dept_stats)), dept_stats.index, rotation=45, ha='right')
plt.xlabel('Department')
plt.ylabel('Employees Who Left (%)')
plt.title('Department vs Employee Retention Rate', fontsize=14, fontweight='bold')

# Add percentage labels
for bar, pct in zip(bars, dept_stats['left_pct']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{pct:.1f}%', ha='center', fontweight='bold')

plt.ylim(0, max(dept_stats['left_pct']) + 10)
plt.grid(axis='y', alpha=0.3)
st.pyplot(fig2)

# 3. Satisfaction Level Distribution
st.subheader("😊 Satisfaction Level Impact")

fig3 = plt.figure(figsize=(12, 5))

# FIXED: Use palette with correct key types
# Convert 'left' to categorical for proper coloring
df['left_category'] = df['left'].astype('category')

# Method 1: Use dictionary with string keys after conversion
sns.histplot(data=df, x='satisfaction_level', hue='left', 
             bins=30, alpha=0.6, 
             palette={0: '#6bcf7f', 1: '#ff6b6b'},  # Using Python ints
             multiple="layer")
plt.title('Satisfaction Level Distribution: Stayed vs Left', fontsize=14, fontweight='bold')
plt.xlabel('Satisfaction Level')
plt.ylabel('Employee Count')
plt.legend(title='Left Company', labels=['Stayed (0)', 'Left (1)'])
plt.grid(axis='y', alpha=0.3)

st.pyplot(fig3)

# Alternative: Using seaborn's built-in palettes (simpler)
# st.subheader("😊 Satisfaction Level Impact (Alternative View)")
# fig3_alt = plt.figure(figsize=(12, 5))
# sns.histplot(data=df, x='satisfaction_level', hue='left', 
#              bins=30, alpha=0.6, palette='Set2')
# plt.title('Satisfaction Level Distribution', fontsize=14, fontweight='bold')
# st.pyplot(fig3_alt)

# 4. Correlation Heatmap
st.subheader("🔥 Correlation Heatmap")

fig4 = plt.figure(figsize=(12, 8))

# Select only numeric columns
numeric_df = df.select_dtypes(include=[np.number])
correlation = numeric_df.corr()

# Create heatmap
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, mask=mask, annot=True, cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')

st.pyplot(fig4)

# Display correlations with 'left'
st.write("**Top factors correlated with employee retention:**")
corr_with_left = correlation['left'].sort_values(ascending=False)
corr_df = pd.DataFrame({
    'Feature': corr_with_left.index,
    'Correlation with Leaving': corr_with_left.values
})
st.dataframe(corr_df.style.background_gradient(cmap='RdYlBu_r', subset=['Correlation with Leaving']))

# -----------------------------------
# FEATURE SELECTION
# -----------------------------------
st.header("🎯 Model Building")

st.subheader("Select Features for Logistic Regression")

# Let user choose features based on EDA insights
default_features = ['satisfaction_level', 'average_montly_hours', 'promotion_last_5years']

# Show correlation insights
st.info("💡 Based on the correlation heatmap, these features have the strongest relationship with employee retention:")

all_numeric_features = [col for col in df.select_dtypes(include=[np.number]).columns if col != 'left' and col != 'left_category']
if 'left_category' in all_numeric_features:
    all_numeric_features.remove('left_category')

selected_features = st.multiselect(
    "Select features to use in the model:",
    options=all_numeric_features,
    default=default_features,
    help="Choose which variables to include in the logistic regression model"
)

if len(selected_features) == 0:
    st.warning("⚠️ Please select at least one feature for the model")
    st.stop()

# Prepare data for modeling
X = df[selected_features]
y = df['left']

# Train-test split
test_size = st.slider("Test set size (%):", 10, 40, 20) / 100
random_state = st.number_input("Random state (for reproducibility):", 0, 100, 42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=random_state, stratify=y
)

st.write(f"📊 Training set: {len(X_train)} samples")
st.write(f"📊 Test set: {len(X_test)} samples")

# -----------------------------------
# TRAIN MODEL
# -----------------------------------
if st.button("🚀 Train Logistic Regression Model", type="primary"):
    with st.spinner("Training model..."):
        # Train logistic regression
        model = LogisticRegression(max_iter=1000, random_state=random_state)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        # Display results
        st.success(f"✅ Model trained successfully!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Accuracy", f"{accuracy*100:.2f}%")
        with col2:
            st.metric("Training Set Size", f"{len(X_train)}")
        with col3:
            st.metric("Test Set Size", f"{len(X_test)}")
        
        # Confusion Matrix
        st.subheader("📊 Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        
        fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm,
                    xticklabels=['Stayed', 'Left'],
                    yticklabels=['Stayed', 'Left'])
        ax_cm.set_xlabel('Predicted')
        ax_cm.set_ylabel('Actual')
        ax_cm.set_title('Confusion Matrix')
        st.pyplot(fig_cm)
        
        # Classification Report
        st.subheader("📋 Classification Report")
        report = classification_report(y_test, y_pred, 
                                      target_names=['Stayed', 'Left'],
                                      output_dict=True)
        
        # Convert to DataFrame for better display
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df.style.format("{:.3f}"))
        
        # Feature Importance (Coefficients)
        st.subheader("🔍 Feature Importance (Coefficients)")
        coef_df = pd.DataFrame({
            'Feature': selected_features,
            'Coefficient': model.coef_[0],
            'Absolute Impact': np.abs(model.coef_[0])
        }).sort_values('Absolute Impact', ascending=False)
        
        fig_coef, ax_coef = plt.subplots(figsize=(8, 5))
        colors = ['red' if c < 0 else 'green' for c in coef_df['Coefficient']]
        ax_coef.barh(range(len(coef_df)), coef_df['Coefficient'], color=colors)
        ax_coef.set_yticks(range(len(coef_df)))
        ax_coef.set_yticklabels(coef_df['Feature'])
        ax_coef.set_xlabel('Coefficient Value')
        ax_coef.set_title('Feature Coefficients in Logistic Regression')
        ax_coef.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        st.pyplot(fig_coef)
        
        # Store model in session state for predictions
        st.session_state['model'] = model
        st.session_state['features'] = selected_features
        st.session_state['accuracy'] = accuracy
        
        # Show equation
        st.subheader("📐 Model Equation")
        equation = f"P(Leave) = 1 / (1 + e^(-({model.intercept_[0]:.4f}"
        for feat, coef in zip(selected_features, model.coef_[0]):
            equation += f" + {coef:.4f} × {feat}"
        equation += "))"
        st.code(equation, language="python")

# -----------------------------------
# PREDICTION INTERFACE
# -----------------------------------
if 'model' in st.session_state:
    st.header("🔮 Predict Employee Retention")
    
    st.markdown("### Enter Employee Details")
    
    # Create input fields based on selected features
    input_data = {}
    cols = st.columns(min(3, len(selected_features)))
    
    for idx, feature in enumerate(selected_features):
        col_idx = idx % 3
        with cols[col_idx]:
            # Get min, max, and mean for slider ranges
            min_val = float(df[feature].min())
            max_val = float(df[feature].max())
            mean_val = float(df[feature].mean())
            
            if feature in ['satisfaction_level', 'last_evaluation']:
                input_data[feature] = st.slider(
                    f"{feature.replace('_', ' ').title()}",
                    min_value=min_val,
                    max_value=max_val,
                    value=mean_val,
                    step=0.01,
                    format="%.2f"
                )
            elif feature in ['number_project', 'time_spend_company', 'Work_accident', 'promotion_last_5years']:
                input_data[feature] = st.number_input(
                    f"{feature.replace('_', ' ').title()}",
                    min_value=int(min_val),
                    max_value=int(max_val),
                    value=int(mean_val),
                    step=1
                )
            else:
                input_data[feature] = st.number_input(
                    f"{feature.replace('_', ' ').title()}",
                    min_value=float(min_val),
                    max_value=float(max_val),
                    value=float(mean_val),
                    step=1.0
                )
    
    if st.button("Predict Employee Attrition Risk"):
        # Create DataFrame for prediction
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        model = st.session_state['model']
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Display results with styling
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if prediction == 1:
                st.error("## ⚠️ HIGH RISK")
                st.error(f"### This employee has a {probability[1]*100:.1f}% probability of leaving the company")
                st.warning("**Recommendation:** Consider retention strategies like salary review, promotion opportunities, or workload assessment.")
            else:
                st.success("## ✅ LOW RISK")
                st.success(f"### This employee has a {probability[0]*100:.1f}% probability of staying with the company")
                st.info("**Status:** Employee is likely to remain with the company.")
        
        # Show probability gauge
        st.markdown("### Risk Probability Gauge")
        prob_percent = probability[1] * 100
        st.progress(int(prob_percent))
        st.caption(f"{prob_percent:.1f}% probability of leaving")

# -----------------------------------
# SIGMOID FUNCTION VISUALIZATION
# -----------------------------------
st.header("📐 Logistic Regression: Sigmoid Function")

fig5 = plt.figure(figsize=(10, 5))

x = np.linspace(-10, 10, 200)
y = 1 / (1 + np.exp(-x))

plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sigmoid Function - Maps any value to probability between 0 and 1', 
          fontsize=14, fontweight='bold')
plt.xlabel('x (Linear combination of features)')
plt.ylabel('Probability (Sigmoid(x))')
plt.grid(True, alpha=0.3)
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Decision boundary (0.5)')
plt.axvline(x=0, color='r', linestyle='--', alpha=0.5)
plt.legend()
plt.ylim(-0.05, 1.05)

st.pyplot(fig5)

st.markdown("""
**How Logistic Regression Works:**
1. The model calculates a linear combination of input features
2. This value is passed through the sigmoid function
3. The sigmoid function outputs a probability between 0 and 1
4. If probability > 0.5, predict "Will Leave" (1), else predict "Will Stay" (0)
""")

# -----------------------------------
# DOWNLOAD RESULTS
# -----------------------------------
if 'model' in st.session_state:
    st.header("💾 Download Model Predictions")
    
    if st.button("Generate Predictions for All Employees"):
        all_predictions = st.session_state['model'].predict(X)
        all_probabilities = st.session_state['model'].predict_proba(X)[:, 1]
        
        results_df = df.copy()
        results_df['prediction'] = all_predictions
        results_df['probability_of_leaving'] = all_probabilities
        
        # Only show relevant columns
        display_cols = ['satisfaction_level', 'average_montly_hours', 'promotion_last_5years', 
                        'salary', 'sales', 'left', 'prediction', 'probability_of_leaving']
        available_cols = [col for col in display_cols if col in results_df.columns]
        
        csv = results_df[available_cols].to_csv(index=False)
        
        st.download_button(
            label="📥 Download Predictions CSV",
            data=csv,
            file_name="hr_retention_predictions.csv",
            mime="text/csv"
        )

# Clean up temporary column
if 'left_category' in df.columns:
    df.drop('left_category', axis=1, inplace=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.markdown("""
**Note:** This model helps identify employees at risk of leaving. 
Use these insights to implement targeted retention strategies and improve employee satisfaction.
""")
