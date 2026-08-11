import pandas as pd
# Load customer data
df = pd.read_csv("lab/customer_data_20.csv")
# Create customer segments
def segment(spending):
    if spending > 50000:
        return "High Spender"
    elif spending >= 20000:
        return "Medium Spender"
    else:
        return "Low Spender"
df["Segment"] = df["Total Spending"].apply(segment)
print("Customer Segmentation:")
print(df)
# Calculate average age of each segment
average_age = df.groupby("Segment")["Age"].mean()
print("\nAverage Age of Customers in Each Segment:")
print(average_age)