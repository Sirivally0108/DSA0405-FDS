import pandas as pd

df = pd.DataFrame({
    'values': [10, 20, 30, 40, 50, 50]
})

print("Mean:", df['values'].mean())
print("Median:", df['values'].median())
print("Mode:", df['values'].mode().tolist())
print("Variance:", df['values'].var())
print("Standard Deviation:", df['values'].std())
print("Range:", df['values'].max() - df['values'].min())