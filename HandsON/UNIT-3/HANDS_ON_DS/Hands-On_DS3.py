import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("house_prices.csv")

plt.hist(df["Price"], bins=5)

plt.title("House Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")

plt.show()

print("Observe the histogram to determine whether the data is normally distributed or skewed.")