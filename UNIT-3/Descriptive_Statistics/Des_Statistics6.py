data = [2, 4, 4, 4, 5, 5, 7, 9]

mean_val = sum(data) / len(data)

variance_val = sum((x - mean_val) ** 2 for x in data) / len(data)

std_dev = variance_val ** 0.5

print("Standard Deviation:", std_dev)