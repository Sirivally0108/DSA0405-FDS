import pandas as pd
df = pd.read_csv("customer_data.csv")
frequency = df["Age"].value_counts().sort_index()
print("Frequency Distribution of Customer Ages")
print(frequency)