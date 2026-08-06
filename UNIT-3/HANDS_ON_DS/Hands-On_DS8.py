import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("iris.csv")

print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDescriptive Statistics")
print(df.describe())

df.hist(figsize=(8,6))
plt.show()

df.boxplot(figsize=(8,6))
plt.show()

numeric = df.select_dtypes(include="number")

Q1 = numeric.quantile(0.25)
Q3 = numeric.quantile(0.75)

IQR = Q3 - Q1

cleaned = numeric[
    ~((numeric < (Q1 - 1.5 * IQR)) |
      (numeric > (Q3 + 1.5 * IQR))).any(axis=1)
]

cleaned.to_csv("iris_cleaned.csv", index=False)

print("Cleaned dataset saved as iris_cleaned.csv")