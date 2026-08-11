import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
# Read CSV file
df = pd.read_csv("lab/age_bodyfat.csv")
# Calculate statistics
print("Mean:")
print(df.mean())
print("\nMedian:")
print(df.median())
print("\nStandard Deviation:")
print(df.std())
# Box plots
df.boxplot()
plt.title("Box Plot of Age and Body Fat")
plt.show()
# Scatter plot
plt.scatter(df["Age"], df["BodyFat"])
plt.xlabel("Age")
plt.ylabel("Body Fat (%)")
plt.title("Age vs Body Fat")
plt.show()
# Q-Q plots
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
stats.probplot(df["Age"], dist="norm", plot=plt)
plt.title("Q-Q Plot - Age")
plt.subplot(1, 2, 2)
stats.probplot(df["BodyFat"], dist="norm", plot=plt)
plt.title("Q-Q Plot - Body Fat")
plt.tight_layout()
plt.show()