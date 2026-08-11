import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("salary_data.csv")

plt.boxplot(df["Salary"])

plt.title("Salary Box Plot")

plt.show()

print("Points outside the whiskers are outliers.")