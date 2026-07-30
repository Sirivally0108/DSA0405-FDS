from scipy import stats

data = [5, 2, 5, 3, 5, 4]

mode_result = stats.mode(data, keepdims=True)

print("Mode:", mode_result.mode[0])
print("Count:", mode_result.count[0])