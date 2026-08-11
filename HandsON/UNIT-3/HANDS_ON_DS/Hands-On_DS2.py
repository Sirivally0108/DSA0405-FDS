import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("student_grades.csv")

frequency = df["Grade"].value_counts().sort_index()

print(frequency)

frequency.plot(kind="bar")

plt.title("Grade Frequency")
plt.xlabel("Grade")
plt.ylabel("Frequency")
plt.show()