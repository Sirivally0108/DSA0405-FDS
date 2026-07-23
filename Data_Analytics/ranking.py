import pandas as pd

data = {
    'Name': ['Arun', 'Bala', 'Chitra', 'Divya', 'Ezhil', 'Fathima'],
    'Department': ['CSE', 'ECE', 'CSE', 'ECE', 'CSE', 'ECE'],
    'Marks': [85, 78, 92, 88, 75, 95]
}

df = pd.DataFrame(data)

df['Rank'] = df['Marks'].rank(ascending=False, method='dense')

print("Student Ranking")
print(df.sort_values(by='Rank'))