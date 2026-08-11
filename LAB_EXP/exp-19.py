import pandas as pd
# Load sales data
df = pd.read_csv("lab/sales_data_19.csv")
# Calculate total sales for each transaction
df["Total Sales"] = df["Quantity Sold"] * df["Unit Price"]
print("Sales Data:")
print(df)
# Calculate total sales for each product
product_sales = df.groupby("Product")["Total Sales"].sum()
print("\nTotal Sales for Each Product:")
print(product_sales)
# Calculate profit with 20% profit margin
product_profit = product_sales * 0.20
print("\nProfit for Each Product:")
print(product_profit)
# Overall profit
overall_profit = product_profit.sum()
print("\nOverall Profit:", overall_profit)
# Top 5 profitable products
top_5 = product_profit.sort_values(ascending=False).head(5)
print("\nTop 5 Most Profitable Products:")
print(top_5)