import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("stock_data.csv")

prices = df["Close"]

mean_price = prices.mean()
minimum = prices.min()
maximum = prices.max()
price_range = maximum - minimum
variance = prices.var()
std_dev = prices.std()
cv = (std_dev / mean_price) * 100

print("Stock Price Analysis")
print("--------------------")
print("Mean Price       :", round(mean_price, 2))
print("Minimum Price    :", round(minimum, 2))
print("Maximum Price    :", round(maximum, 2))
print("Price Range      :", round(price_range, 2))
print("Variance         :", round(variance, 2))
print("Standard Deviation:", round(std_dev, 2))
print("Coefficient of Variation:", round(cv, 2), "%")

# Plot
plt.plot(df["Date"], prices)
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.title("Stock Price Movement")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()