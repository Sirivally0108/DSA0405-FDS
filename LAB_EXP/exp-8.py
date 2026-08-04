import pandas as pd

df = pd.read_csv("Sales_data_8.csv")

top_5_products = df.groupby("Product_Name")["Price"].sum().nlargest(5)

print("Five Most Sold Products:")
print(top_5_products)