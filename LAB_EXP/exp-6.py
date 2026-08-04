import pandas as pd

df = pd.read_csv("grocerystore.csv")

total_sales = df["Sales"].sum()

print("Total Sales for the Grocery Store:", round(total_sales, 2))

discount = 0.10
tax = 0.18

price_after_discount = total_sales - (total_sales * discount)
price_after_tax = price_after_discount + (price_after_discount * tax)

print("Final Amount after Applying Discount and Tax:",
      round(price_after_tax, 2))