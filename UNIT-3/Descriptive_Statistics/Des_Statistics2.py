data = [40, 10, 30, 50, 20]

data.sort()

n = len(data)

if n % 2 == 0:
    median_val = (data[n // 2 - 1] + data[n // 2]) / 2
else:
    median_val = data[n // 2]

print("Median:", median_val)