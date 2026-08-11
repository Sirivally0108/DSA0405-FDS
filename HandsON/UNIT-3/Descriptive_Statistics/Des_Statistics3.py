from collections import Counter

data = [1, 2, 2, 3, 4, 2, 5]

count = Counter(data)

mode_val = count.most_common(1)[0][0]

print("Mode:", mode_val)