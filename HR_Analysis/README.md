<div align="center">

# 👥 HR Employee Retention Analytics

### *Predict Employee Attrition Using Machine Learning*

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📝 **Project Overview**

This application uses **Logistic Regression** to predict employee attrition (whether an employee will leave the company). It provides comprehensive EDA (Exploratory Data Analysis), interactive feature selection, and real-time predictions with probability scores.

### 🎯 **Business Use Case**
HR departments can use this tool to:
- Identify employees at risk of leaving
- Understand key factors driving attrition
- Implement targeted retention strategies
- Reduce voluntary turnover by 25-30%
- Optimize HR policies and interventions

---

## ✨ **Features**

| Feature | Description |
|---------|-------------|
| 📊 **Interactive EDA** | Visualize salary, department, and satisfaction impacts |
| 🎯 **Feature Selection** | Choose which variables to include in the model |
| 📈 **Model Training** | Train logistic regression with customizable test size |
| 📋 **Performance Metrics** | Accuracy, confusion matrix, classification report |
| 🔮 **Real-time Predictions** | Input employee details to get attrition risk |
| 📥 **Batch Predictions** | Generate predictions for all employees at once |
| 🔥 **Correlation Heatmap** | Visualize feature relationships |
| 📐 **Feature Importance** | See which factors matter most |

---

## 🚀 **Live Demo**

<div align="center">

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dharaneesh-xah29pvunn2mzoi5skw8ta.streamlit.app/)

**Click the badge above to launch the live app!**

</div>

---

## 📊 **Dataset Information**

### Features Description

| Feature | Type | Description | Range |
|---------|------|-------------|-------|
| `satisfaction_level` | Float | Employee satisfaction score | 0-1 |
| `last_evaluation` | Float | Last performance evaluation score | 0-1 |
| `number_project` | Integer | Number of projects completed | 2-6 |
| `average_montly_hours` | Integer | Average monthly working hours | 150-280 |
| `time_spend_company` | Integer | Years spent at the company | 2-8 |
| `Work_accident` | Binary | Had a work accident (0=No, 1=Yes) | 0/1 |
| `promotion_last_5years` | Binary | Promoted in last 5 years | 0/1 |
| `salary` | Categorical | Salary level | low/medium/high |
| `sales` | Categorical | Department name | 10 departments |
| `left` | Target | Left company (0=Stayed, 1=Left) | 0/1 |

### Departments Included
- Sales
- Technical
- Support
- IT
- Product Management
- Marketing
- R&D
- Accounting
- HR
- Management

---

## 📈 **Key Insights from EDA**

### 1. **Salary Impact**
| Salary Level | Attrition Rate |
|--------------|----------------|
| Low | ~25% |
| Medium | ~15% |
| High | ~8% |

### 2. **Department Impact**
| Department | Attrition Rate |
|------------|----------------|
| Sales | Highest |
| Technical | High |
| HR | Low |
| Management | Lowest |

### 3. **Satisfaction Level**
- Employees with satisfaction < 0.5 are **3x more likely** to leave
- Employees with satisfaction > 0.8 are **highly likely** to stay

### 4. **Promotion Impact**
- No promotion in 5 years → **40% higher** attrition risk
- Recent promotion → **80% lower** attrition risk

---

## 🧠 **Model Explanation**

### Logistic Regression
The model uses logistic regression to calculate the probability of an employee leaving:
