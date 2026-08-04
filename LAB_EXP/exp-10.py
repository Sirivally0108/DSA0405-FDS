import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Sales_data_10.csv")

monthly_sales = df.groupby("Month_sales")["Price"].sum()

plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title("Monthly Sales Data")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=60)
plt.show()

plt.bar(monthly_sales.index, monthly_sales.values)
plt.title("Monthly Sales Data")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=60)
plt.show()