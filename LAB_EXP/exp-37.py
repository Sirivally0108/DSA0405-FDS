import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("student_scores.csv")

# Correlation
correlation = df["Study_Hours"].corr(df["Exam_Score"])

print("Correlation coefficient:", round(correlation, 3))
if correlation > 0:
    print("There is a positive correlation.")
elif correlation < 0:
    print("There is a negative correlation.")
else:
    print("There is no linear correlation.")

# Scatter plot
plt.scatter(df["Study_Hours"], df["Exam_Score"])

plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.title("Study Time vs Exam Score")
plt.grid(True)
plt.show()