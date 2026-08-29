import pandas as pd

# Load dataset
df = pd.read_csv("city_temperature.csv")

# Mean temperature
mean_temp = df.groupby("City")["Temperature"].mean()

# Standard deviation
std_temp = df.groupby("City")["Temperature"].std()

# Temperature range
range_temp = df.groupby("City")["Temperature"].agg(
    lambda x: x.max() - x.min()
)

print("Mean Temperature:")
print(mean_temp)

print("\nStandard Deviation:")
print(std_temp)

print("\nTemperature Range:")
print(range_temp)

# Highest range
highest_range_city = range_temp.idxmax()

# Most consistent city
consistent_city = std_temp.idxmin()

print("\nCity with highest temperature range:",
      highest_range_city)

print("Most consistent city:",
      consistent_city)