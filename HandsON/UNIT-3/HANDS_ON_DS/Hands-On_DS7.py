import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data_values.csv")

Q1 = df["Value"].quantile(0.25)
Q3 = df["Value"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

cleaned = df[(df["Value"] >= lower) & (df["Value"] <= upper)]

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.hist(df["Value"])
plt.title("Before")

plt.subplot(1,2,2)
plt.hist(cleaned["Value"])
plt.title("After")

plt.show()

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.boxplot(df["Value"])

plt.subplot(1,2,2)
plt.boxplot(cleaned["Value"])

plt.show()