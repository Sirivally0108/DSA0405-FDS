import pandas as pd
import numpy as np
from scipy import stats

# Load CSV file
data = pd.read_csv("customer_reviews_22.csv")

# Extract ratings
ratings = data["rating"].dropna()

# Calculate sample statistics
n = len(ratings)
mean_rating = ratings.mean()
std_rating = ratings.std()

# Confidence level
confidence = 0.95
alpha = 1 - confidence

# Standard error
standard_error = std_rating / np.sqrt(n)

# t critical value
t_value = stats.t.ppf(
    1 - alpha / 2,
    df=n - 1
)

# Margin of error
margin_error = t_value * standard_error

# Confidence interval
lower = mean_rating - margin_error
upper = mean_rating + margin_error

print("Number of Reviews:", n)
print("Average Rating:", round(mean_rating, 3))
print("Standard Deviation:", round(std_rating, 3))
print("Standard Error:", round(standard_error, 3))
print("Margin of Error:", round(margin_error, 3))

print(
    "95% Confidence Interval:",
    (round(lower, 3), round(upper, 3))
)