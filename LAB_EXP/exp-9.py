import pandas as pd

df = pd.read_csv("House_data_9.csv")

location_price_average = df.groupby("Location")["price"].mean()

more_than_4beds = df[df["beds"] > 4].count()["beds"]

largest_sq_feet = df["size"].max()

print("Average House Price for Each Location:")
print(location_price_average)

print("\nNumber of Houses with More Than 4 Bedrooms:", more_than_4beds)

print("Largest House Size:", largest_sq_feet)