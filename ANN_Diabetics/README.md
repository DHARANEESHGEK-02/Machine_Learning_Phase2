<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANN Diabetes Prediction Project</title>

    <style>
        body{
            font-family: Arial, sans-serif;
            background-color:#f4f6f9;
            margin:0;
            padding:0;
            line-height:1.6;
            color:#333;
        }

        .container{
            width:80%;
            margin:auto;
            padding:20px;
        }

        .card{
            background:white;
            padding:25px;
            margin-bottom:20px;
            border-radius:10px;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
        }

        h1{
            color:#0d6efd;
            text-align:center;
        }

        h2{
            color:#198754;
            margin-top:20px;
        }

        code{
            background:#eee;
            padding:2px 5px;
            border-radius:5px;
        }

        pre{
            background:#272822;
            color:#f8f8f2;
            padding:15px;
            border-radius:8px;
            overflow-x:auto;
        }

        ul{
            padding-left:20px;
        }

        .footer{
            text-align:center;
            padding:20px;
            color:gray;
        }
    </style>
</head>

<body>

    <div class="container">

        <div class="card">
            <h1>🩺 ANN Diabetes Prediction Project</h1>

            <p>
                This project demonstrates how to build an 
                <b>Artificial Neural Network (ANN)</b> using 
                <b>TensorFlow</b> and <b>Keras</b> to predict whether 
                a person has diabetes based on medical diagnostic data.
            </p>
        </div>

        <div class="card">
            <h2>📌 Project Overview</h2>

            <ul>
                <li>Data Loading</li>
                <li>Data Preprocessing</li>
                <li>Feature Scaling</li>
                <li>Train-Test Splitting</li>
                <li>Building ANN Model</li>
                <li>Model Training</li>
                <li>Model Evaluation</li>
                <li>Prediction Generation</li>
            </ul>
        </div>

        <div class="card">
            <h2>🧠 Technologies Used</h2>

            <ul>
                <li>Python</li>
                <li>Pandas</li>
                <li>NumPy</li>
                <li>Scikit-learn</li>
                <li>TensorFlow</li>
                <li>Keras</li>
            </ul>
        </div>

        <div class="card">
            <h2>📂 Dataset Information</h2>

            <p>
                The project uses the 
                <b>Pima Indians Diabetes Dataset</b>.
            </p>

            <h3>Features</h3>

            <ul>
                <li>Pregnancies</li>
                <li>Glucose</li>
                <li>BloodPressure</li>
                <li>SkinThickness</li>
                <li>Insulin</li>
                <li>BMI</li>
                <li>DiabetesPedigreeFunction</li>
                <li>Age</li>
            </ul>

            <h3>Target</h3>

            <ul>
                <li>0 → No Diabetes</li>
                <li>1 → Diabetes</li>
            </ul>
        </div>

        <div class="card">
            <h2>⚙️ Data Preprocessing</h2>

<pre>
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
</pre>

        </div>

        <div class="card">
            <h2>🧠 ANN Model Architecture</h2>

<pre>
model = Sequential([
    Dense(12, input_dim=8, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])
</pre>

        </div>

        <div class="card">
            <h2>⚡ Model Compilation</h2>

<pre>
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
</pre>

        </div>

        <div class="card">
            <h2>🚀 Model Training</h2>

<pre>
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=10
)
</pre>

        </div>

        <div class="card">
            <h2>📊 Model Evaluation</h2>

<pre>
loss, accuracy = model.evaluate(X_test, y_test)
</pre>

            <p>
                The project evaluates the model using:
            </p>

            <ul>
                <li>Accuracy</li>
                <li>Precision</li>
                <li>Recall</li>
                <li>F1-Score</li>
                <li>Confusion Matrix</li>
            </ul>
        </div>

        <div class="card">
            <h2>▶️ How to Run the Project</h2>

            <h3>Step 1: Clone Repository</h3>

<pre>
git clone your-repository-link
</pre>

            <h3>Step 2: Install Libraries</h3>

<pre>
pip install pandas numpy scikit-learn tensorflow
</pre>

            <h3>Step 3: Run Jupyter Notebook</h3>

<pre>
jupyter notebook
</pre>

        </div>

        <div class="card">
            <h2>📁 Project Structure</h2>

<pre>
├── diabetes.csv
├── ann_diabetes_project - task.ipynb
├── README.md
</pre>

        </div>

        <div class="card">
            <h2>🎯 Future Improvements</h2>

            <ul>
                <li>Add Dropout Layers</li>
                <li>Hyperparameter Tuning</li>
                <li>Deploy Using Streamlit</li>
                <li>Improve Accuracy</li>
                <li>Add Data Visualization Dashboard</li>
            </ul>
        </div>

        <div class="card">
            <h2>👨‍💻 Author</h2>

            <p>
                Developed by <b>Dharaneesh</b>
            </p>
        </div>

        <div class="card">
            <h2>⭐ Conclusion</h2>

            <p>
                This project provides a beginner-friendly implementation 
                of an Artificial Neural Network for diabetes prediction 
                using TensorFlow and Keras. It demonstrates how deep learning 
                can be applied to healthcare-related prediction problems.
            </p>
        </div>

        <div class="footer">
            © 2026 ANN Diabetes Prediction Project
        </div>

    </div>

</body>
</html>
