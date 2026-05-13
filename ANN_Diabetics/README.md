<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Prediction using ANN - Project README</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        h3 {
            color: #555;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        pre {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .badge-python {
            background-color: #3776ab;
            color: white;
        }
        .badge-tensorflow {
            background-color: #ff6f00;
            color: white;
        }
        .badge-keras {
            background-color: #d00000;
            color: white;
        }
        .note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Diabetes Prediction using Artificial Neural Network (ANN)</h1>
        
        <p>
            <span class="badge badge-python">Python</span>
            <span class="badge badge-tensorflow">TensorFlow</span>
            <span class="badge badge-keras">Keras</span>
        </p>
        
        <p>This project demonstrates how to build a basic Artificial Neural Network (ANN) using <strong>TensorFlow</strong> and <strong>Keras</strong> to predict diabetes based on diagnostic measurements. We will use the <strong>Pima Indians Diabetes Dataset</strong>.</p>
        
        <h2>📋 Project Overview</h2>
        <ol>
            <li><strong>Data Loading</strong>: Load the CSV dataset</li>
            <li><strong>Data Preprocessing</strong>: Prepare the data for the neural network</li>
            <li><strong>Model Architecture</strong>: Define the ANN using the Sequential API</li>
            <li><strong>Compilation</strong>: Configure the learning process</li>
            <li><strong>Training</strong>: Train the model on the data</li>
            <li><strong>Evaluation</strong>: Assess the model's performance</li>
        </ol>
        
        <h2>📊 Dataset Information</h2>
        <p>The dataset contains <strong>8 medical predictor variables</strong> and one target variable (Outcome).</p>
        
        <h2>🛠️ Installation & Dependencies</h2>
        <pre><code>pip install pandas numpy scikit-learn tensorflow</code></pre>
        
        <h2>📝 Complete Code</h2>
        <pre><code>import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Data Loading
data = pd.read_csv('/home/intellect/Phase_2_Of_ML/TASK/Dataset/diabetes.csv')

# 2. Data Preprocessing
print('Missing values per column:')
print(data.isnull().sum())

X = data.drop('Outcome', axis=1).values   
y = data['Outcome'].values                

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  
X_test = scaler.transform(X_test)

# 3. Model Architecture
model = Sequential([
    Dense(12, input_dim=8, activation='relu'),  # Hidden Layer 1
    Dense(8, activation='relu'),                 # Hidden Layer 2
    Dense(1, activation='sigmoid')               # Output Layer
])

# 4. Compilation
model.compile(optimizer='adam', 
              loss='binary_crossentropy', 
              metrics=['accuracy'])

# 5. Training
history = model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=1)

# 6. Evaluation
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob >= 0.5)

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred, target_names=['No Diabetes', 'Diabetes']))

cm = confusion_matrix(y_test, y_pred)</code></pre>
        
        <h2>🧠 Model Architecture</h2>
        <table>
            <thead>
                <tr>
                    <th>Layer Type</th>
                    <th>Neurons</th>
                    <th>Activation Function</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Hidden Layer 1</td>
                    <td>12</td>
                    <td>ReLU</td>
                </tr>
                <tr>
                    <td>Hidden Layer 2</td>
                    <td>8</td>
                    <td>ReLU</td>
                </tr>
                <tr>
                    <td>Output Layer</td>
                    <td>1</td>
                    <td>Sigmoid</td>
                </tr>
            </tbody>
        </table>
        
        <h2>⚙️ Compilation Configuration</h2>
        <ul>
            <li><strong>Optimizer</strong>: Adam</li>
            <li><strong>Loss Function</strong>: Binary Crossentropy</li>
            <li><strong>Metrics</strong>: Accuracy</li>
        </ul>
        
        <h2>🚀 Training Parameters</h2>
        <ul>
            <li><strong>Epochs</strong>: 100</li>
            <li><strong>Batch Size</strong>: 10</li>
            <li><strong>Validation Split</strong>: 20% test size</li>
            <li><strong>Random State</strong>: 42 (for reproducibility)</li>
        </ul>
        
        <h2>📈 Evaluation Metrics</h2>
        <p>The model is evaluated using:</p>
        <ul>
            <li>Accuracy and Loss on test data</li>
            <li>Classification Report (Precision, Recall, F1-Score)</li>
            <li>Confusion Matrix</li>
        </ul>
        
        <div class="note">
            <strong>💡 Note:</strong> Neural networks perform best when input features are on a similar scale. That's why we use <code>StandardScaler</code> for feature normalization.
        </div>
        
        <h2>📁 File Structure</h2>
        <pre><code>ann_diabetes_project - task.ipynb   # Main Jupyter Notebook containing the full implementation
diabetes.csv                         # Dataset file (update path as needed)</code></pre>
        
        <h2>▶️ How to Run</h2>
        <ol>
            <li>Ensure you have all dependencies installed</li>
            <li>Update the dataset path in the code to point to your <code>diabetes.csv</code> file</li>
            <li>Run the Jupyter notebook or convert to Python script</li>
            <li>Execute all cells to train and evaluate the model</li>
        </ol>
        
        <h2>🎯 Expected Output</h2>
        <p>The model will output:</p>
        <ul>
            <li>Training progress for 100 epochs</li>
            <li>Test accuracy score</li>
            <li>Classification report showing precision, recall, and F1-score for both classes</li>
            <li>Confusion matrix</li>
        </ul>
        
        <h2>🔧 Customization</h2>
        <p>You can modify:</p>
        <ul>
            <li>Number of hidden layers and neurons</li>
            <li>Activation functions</li>
            <li>Number of epochs and batch size</li>
            <li>Optimizer and learning rate</li>
        </ul>
        
        <h2>📚 References</h2>
        <ul>
            <li><a href="https://www.tensorflow.org/guide/keras">TensorFlow Keras Documentation</a></li>
            <li><a href="https://scikit-learn.org/stable/">Scikit-learn Documentation</a></li>
            <li>Pima Indians Diabetes Dataset</li>
        </ul>
        
        <div class="footer">
            <p>Built with ❤️ using TensorFlow and Keras | Phase 2 of ML Project</p>
        </div>
    </div>
</body>
</html>
