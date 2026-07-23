import pandas as pd

data = {
    'Name': ['Arun', 'Bala', 'Chitra', 'Divya', 'Ezhil', 'Fathima'],
    'Department': ['CSE', 'ECE', 'CSE', 'ECE', 'CSE', 'ECE'],
    'Marks': [85, 78, 92, 88, 75, 95]
}

df = pd.DataFrame(data)

grouped_df = df.groupby('Department')['Marks'].mean()

print("Average Marks by Department")
print(grouped_df)