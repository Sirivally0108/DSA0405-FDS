import pandas as pd
import matplotlib.pyplot as plt
import string
from collections import Counter

# Read dataset
df = pd.read_csv("lab/data.csv")

# Combine feedback
text = " ".join(df["feedback"])

# Convert to lowercase
text = text.lower()

# Remove punctuation
text = text.translate(str.maketrans("", "", string.punctuation))

# Stop words
stop_words = {
    "the", "is", "and", "to", "a",
    "an", "of", "in", "for", "with"
}

# Remove stop words
words = [word for word in text.split() if word not in stop_words]

# Frequency count
frequency = Counter(words)

# User input
N = int(input("Enter Top N Words: "))

top_words = frequency.most_common(N)

print("\nTop", N, "Frequent Words\n")

for word, count in top_words:
    print(word, ":", count)

# Separate values for plotting
labels = []
counts = []

for word, count in top_words:
    labels.append(word)
    counts.append(count)

# Bar Graph
plt.bar(labels, counts)
plt.title("Top Frequent Words")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.show()