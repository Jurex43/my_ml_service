"""
A/B Testing Script for Income Classifier

This script simulates A/B testing by sending test data to the server
and providing feedback with true labels.
"""

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import requests

print("Loading dataset...")
# load dataset
df = pd.read_csv('https://raw.githubusercontent.com/pplonski/datasets-for-start/master/adult/data.csv', skipinitialspace=True)
x_cols = [c for c in df.columns if c != 'income']
# set input matrix and target column
X = df[x_cols]
y = df['income']
print(f"Dataset loaded: {len(df)} rows")

print("\nSplitting data...")
# data split train / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=1234)
print(f"Test set size: {len(X_test)} rows")

print("\nRunning A/B test with 100 samples...")
print("Sending requests to: http://127.0.0.1:8000/api/v1/income_classifier/predict?status=ab_testing")

for i in range(100):
    input_data = dict(X_test.iloc[i])
    # Convert numpy types to Python native types and handle NaN
    input_data = {k: None if pd.isna(v) else int(v) if isinstance(v, (np.integer, np.int64)) else float(v) if isinstance(v, (np.floating, np.float64)) else v for k, v in input_data.items()}
    target = y_test.iloc[i]
    
    try:
        r = requests.post("http://127.0.0.1:8000/api/v1/income_classifier/predict?status=ab_testing", json=input_data)
        response = r.json()
        
        # provide feedback
        requests.put("http://127.0.0.1:8000/api/v1/mlrequests/{}".format(response["request_id"]), json={"feedback": target})
        
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/100 requests")
    except Exception as e:
        print(f"Error at request {i + 1}: {str(e)}")
        break

print("\n✓ A/B test completed!")
print("\nYou can check the results at:")
print("- http://127.0.0.1:8000/api/v1/mlrequests - to see all requests")
print("- http://127.0.0.1:8000/api/v1/abtests - to see A/B test information")
