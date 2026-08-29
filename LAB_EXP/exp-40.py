import pandas as pd
import matplotlib.pyplot as plt

# Create dataset
data = {
    "Name": [
        "Arun", "Ben", "Carlos", "David", "Ethan",
        "Frank", "George", "Henry", "Ivan", "Jack",
        "Kevin", "Leo"
    ],

    "Age": [
        22, 25, 28, 31, 24,
        27, 30, 21, 29, 26,
        23, 32
    ],

    "Position": [
        "Forward", "Midfielder", "Forward", "Defender",
        "Forward", "Midfielder", "Defender", "Forward",
        "Midfielder", "Defender", "Forward", "Goalkeeper"
    ],

    "Goals": [
        18, 10, 25, 5, 20,
        12, 4, 15, 11, 6,
        22, 2
    ],

    "Weekly_Salary": [
        5000, 4500, 8000, 4000,
        7000, 5500, 3500, 6000,
        5200, 4200, 7500, 3000
    ]
}

df = pd.DataFrame(data)

# Save dataset
df.to_csv("soccer_players.csv", index=False)

# Read dataset
df = pd.read_csv("soccer_players.csv")

print("Soccer Player Dataset:")
print(df)

# Top 5 goal scorers
top_goals = df.sort_values(
    by="Goals", ascending=False
).head(5)

print("\nTop 5 Goal Scorers:")
print(top_goals[["Name", "Goals"]])

# Top 5 salaries
top_salary = df.sort_values(
    by="Weekly_Salary", ascending=False
).head(5)

print("\nTop 5 Highest Salaries:")
print(top_salary[["Name", "Weekly_Salary"]])

# Average age
average_age = df["Age"].mean()

print("\nAverage Age:", round(average_age, 2))

# Players above average age
above_average = df[df["Age"] > average_age]

print("\nPlayers Above Average Age:")
print(above_average[["Name", "Age"]])

# Position distribution
position_count = df["Position"].value_counts()

print("\nPlayers by Position:")
print(position_count)

# Bar chart
position_count.plot(kind="bar")

plt.xlabel("Position")
plt.ylabel("Number of Players")
plt.title("Distribution of Players by Position")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()