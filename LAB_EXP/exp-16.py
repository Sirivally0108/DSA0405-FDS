import pandas as pd
from collections import Counter

# Read dataset
df = pd.read_csv("lab/customer_reviews.csv")

# Combine all reviews
text = " ".join(df["Review"])

# Convert to lowercase
text = text.lower()

# Split into words
words = text.split()

# Count frequency
frequency = Counter(words)

print("Word Frequency Distribution\n")

for word, count in frequency.items():
    print(word, ":", count)