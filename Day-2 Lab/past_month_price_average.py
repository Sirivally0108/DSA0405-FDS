import pandas as pd

# Read CSV
df = pd.read_csv("Sales_data.csv")

# Average price in November 2023
average_price = df[df["Month_sales"] == "November 2023"]["Price"].mean()

print("Average Price in November 2023:", round(average_price, 2))