# 🩺 ANN Diabetes Prediction Project

This project demonstrates how to build an Artificial Neural Network (ANN) using TensorFlow and Keras to predict whether a person has diabetes based on medical diagnostic measurements.

---

## 📌 Project Overview

The project includes:

- Data Loading
- Data Preprocessing
- Feature Scaling
- Train-Test Splitting
- Building ANN Model
- Model Training
- Model Evaluation
- Prediction Generation

---

## 🧠 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TensorFlow
- Keras

---

## 📂 Dataset Information

The project uses the **Pima Indians Diabetes Dataset**.

### Features

- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age

### Target

- `0` → No Diabetes
- `1` → Diabetes

---

## ⚙️ Data Preprocessing

```python
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

---

## 🧠 ANN Model Architecture

```python
model = Sequential([
    Dense(12, input_dim=8, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

---

## ⚡ Model Compilation

```python
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
```

---

## 🚀 Model Training

```python
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=10
)
```

---

## 📊 Model Evaluation

```python
loss, accuracy = model.evaluate(X_test, y_test)
```

The project evaluates the model using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

---

## ▶️ How to Run the Project

### Step 1: Clone Repository

```bash
git clone your-repository-link
```

### Step 2: Install Required Libraries

```bash
pip install pandas numpy scikit-learn tensorflow
```

### Step 3: Run Jupyter Notebook

```bash
jupyter notebook
```

Then open:

```bash
ann_diabetes_project - task.ipynb
```

---

## 📁 Project Structure

```bash
├── diabetes.csv
├── ann_diabetes_project - task.ipynb
├── README.md
```

---

## 🎯 Future Improvements

- Add Dropout Layers
- Hyperparameter Tuning
- Deploy Using Streamlit
- Improve Accuracy
- Add Visualization Dashboard

---

## 👨‍💻 Author

Developed by **Dharaneesh**

---

## ⭐ Conclusion

This project provides a beginner-friendly implementation of an Artificial Neural Network for diabetes prediction using TensorFlow and Keras. It demonstrates how deep learning can be applied to healthcare-related prediction problems using structured medical data.
