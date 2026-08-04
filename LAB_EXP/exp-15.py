import pandas as pd
df = pd.read_csv("likes_data.csv")
frequency = df["Likes"].value_counts().sort_index()
print("Frequency Distribution of Likes")
print(frequency)