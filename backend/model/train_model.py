import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Build absolute path to data
project_root = os.path.dirname(os.path.dirname(os.getcwd()))
data_path = os.path.join(project_root, 'data', 'heart.csv')

# Load the dataset
df = pd.read_csv(data_path)

# Split features and labels
X = df[['age', 'gender', 'impluse', 'pressurehight', 'pressurelow', 'glucose',
       'kcm', 'troponin']]
y = df['class']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Ensure model directory exists
model_dir = os.path.join(os.getcwd())
os.makedirs(model_dir, exist_ok=True)

# Save the model and scaler
joblib.dump(model, os.path.join(model_dir, 'heart_disease_model.pkl'))
joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))

print("✅ Model and Scaler saved successfully.")
