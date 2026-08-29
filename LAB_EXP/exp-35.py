import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("retail_customers.csv")

# Select features
features = ["Total_Spending", "Visit_Frequency"]

X = df[features]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
model = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = model.fit_predict(X_scaled)

print("Customer Segments:")
print(df)

# Visualization
plt.scatter(
    df["Total_Spending"],
    df["Visit_Frequency"],
    c=df["Cluster"]
)

plt.xlabel("Total Spending")
plt.ylabel("Visit Frequency")
plt.title("Retail Customer Segmentation")
plt.show()