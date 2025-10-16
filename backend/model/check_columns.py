import pandas as pd

# Load the CSV file from the correct path
df = pd.read_csv('../../data/heart.csv')

# Print all column names to verify spelling
print(df.columns)
