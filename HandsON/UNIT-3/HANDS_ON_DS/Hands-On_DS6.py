import pandas as pd

df = pd.read_csv("sales_data.csv")

Q1 = df["Sales"].quantile(0.25)
Q3 = df["Sales"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

cleaned = df[(df["Sales"] >= lower) & (df["Sales"] <= upper)]

print("Cleaned Dataset")
print(cleaned)