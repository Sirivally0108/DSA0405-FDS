import matplotlib.pyplot as plt
# Monthly Sales Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [15000, 18000, 17000, 22000, 25000, 28000]
# 1. Line Plot
plt.figure(figsize=(6,4))
plt.plot(months, sales, marker='o')
plt.title("Monthly Sales - Line Plot")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()
# 2. Scatter Plot
plt.figure(figsize=(6,4))
plt.scatter(months, sales)
plt.title("Monthly Sales - Scatter Plot")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()
# 3. Bar Plot
plt.figure(figsize=(6,4))
plt.bar(months, sales)
plt.title("Monthly Sales - Bar Plot")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()