import matplotlib.pyplot as plt
# Monthly Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

temperature = [24, 26, 30, 34, 36, 35, 32, 31, 30, 28, 26, 24]
rainfall = [12, 18, 25, 40, 65, 110, 150, 140, 120, 80, 35, 15]

# 1. Line Plot for Temperature
plt.figure(figsize=(7,4))
plt.plot(months, temperature, marker='o')
plt.title("Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.show()

# 2. Scatter Plot for Rainfall
plt.figure(figsize=(7,4))
plt.scatter(months, rainfall)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.grid(True)
plt.show()