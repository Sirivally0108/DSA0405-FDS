import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("ecommerce_customers.csv")

# Remove spaces from column names
df.columns = df.columns.str.strip()

print("Columns available in dataset:")
print(df.columns.tolist())

# Select numerical columns automatically
numeric_columns = df.select_dtypes(include="number").columns.tolist()

print("\nNumerical columns:")
print(numeric_columns)

# Select the first two numerical columns
features = numeric_columns[:2]

print("\nFeatures used for clustering:")
print(features)

# Extract features
X = df[features].dropna()

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Number of clusters
k = 3

# Ensure number of clusters does not exceed number of samples
k = min(k, len(X_scaled))

# Create K-Means model
model = KMeans(
    n_clusters=k,
    random_state=42,
    n_init=10
)

# Train the model
model.fit(X_scaled)

# Add cluster labels
df.loc[X.index, "Cluster"] = model.labels_

# Display results
print("\nCustomer Segmentation Results:")
print(df)

print("\nNumber of clusters:", k)
print("Features used:", features)