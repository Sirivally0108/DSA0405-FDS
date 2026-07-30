import numpy as np

data = np.array([10, 20, 20, 30, 40])

print("Mean:", np.mean(data))
print("Median:", np.median(data))
print("Variance (Sample):", np.var(data, ddof=1))
print("Standard Deviation:", np.std(data, ddof=1))
print("Range:", np.ptp(data))