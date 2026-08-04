import numpy as np
student_scores = np.loadtxt(
    "Students_d.csv",
    delimiter=",",
    skiprows=1,
    usecols=(1, 2, 3, 4)
)
subjects = ["Math", "Science", "English", "History"]
average_scores = np.mean(student_scores, axis=0)
highest_subject = subjects[np.argmax(average_scores)]
print("Average Scores:")
for i in range(len(subjects)):
    print(subjects[i], ":", round(average_scores[i], 2))
print("Subject with Highest Average Score:", highest_subject)