data = [2, 4, 4, 4, 5, 5, 7, 9]

mean_val = sum(data) / len(data)

variance_val = sum((x - mean_val) ** 2 for x in data) / len(data)

print("Variance:", variance_val)