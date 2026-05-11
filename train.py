import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Load dataset
df = pd.read_csv("HR_comma_sep.csv")

# Features and target
X = df.drop('left', axis=1)
y = df['left']

# Convert categorical columns
X = pd.get_dummies(X, drop_first=True)

# Train model
model = LogisticRegression(max_iter=1000)

model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model Saved")