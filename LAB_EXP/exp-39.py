import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("ecommerce_transactions.csv")

# Features
features = ["Total_Spent", "Items_Purchased"]

X = df[features]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
model = KMeans(n_clusters=3, random_state=42, n_init=10)

df["Cluster"] = model.fit_predict(X_scaled)

print("Customer Segmentation:")
print(df)

# Cluster summary
print("\nCluster Summary:")
print(
    df.groupby("Cluster")[features].mean()
)

# Visualization
plt.scatter(
    df["Total_Spent"],
    df["Items_Purchased"],
    c=df["Cluster"]
)

plt.xlabel("Total Spent")
plt.ylabel("Items Purchased")
plt.title("E-Commerce Customer Segmentation")
plt.grid(True)
plt.show()