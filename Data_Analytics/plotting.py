import pandas as pd
import matplotlib.pyplot as plt
data = {
    'Name': ['Arun', 'Bala', 'Chitra', 'Divya', 'Ezhil', 'Fathima'],
    'Department': ['CSE', 'ECE', 'CSE', 'ECE', 'CSE', 'ECE'],
    'Marks': [85, 78, 92, 88, 75, 95]
}
df = pd.DataFrame(data)
plt.figure(figsize=(8,5))
plt.bar(df['Name'], df['Marks'])
plt.title("Student Marks")
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.show()
grouped_df = df.groupby('Department')['Marks'].mean()
grouped_df.plot(kind='bar')
plt.title("Average Marks by Department")
plt.xlabel("Department")
plt.ylabel("Average Marks")
plt.show()