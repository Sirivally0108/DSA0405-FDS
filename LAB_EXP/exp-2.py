import pandas as pd
df = pd.read_csv("Sales_data.csv")
average_price = df[df["Month_sales"] == "November 2023"]["Price"].mean()
print("Average Price in November 2023:", round(average_price, 2))