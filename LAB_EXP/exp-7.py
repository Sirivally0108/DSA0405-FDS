import pandas as pd

df = pd.read_csv("order_data.csv")
total_orders = df.groupby("Full Name")["Order Count"].sum()
avg_order_per_product = df.groupby("Items")["Order Total"].mean()
earliest_order = df["Order"].min()
latest_order = df["Order"].max()

print("Total Number of Orders Made by Each Customer:")
print(total_orders)

print("\nAverage Order Value for Each Product:")
print(avg_order_per_product)

print("\nEarliest Order Date:", earliest_order)
print("Latest Order Date:", latest_order)