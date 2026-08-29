import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load dataset
data = pd.read_csv("clinical_trial.csv")

# Separate groups
control = data[
    data["group"] == "Control"
]["outcome"]

treatment = data[
    data["group"] == "Treatment"
]["outcome"]

# Calculate means
control_mean = control.mean()
treatment_mean = treatment.mean()

# Perform independent t-test
t_stat, p_value = ttest_ind(
    treatment,
    control,
    equal_var=False
)

alpha = 0.05

print("Control Group Mean:",
      round(control_mean, 3))

print("Treatment Group Mean:",
      round(treatment_mean, 3))

print("t-statistic:",
      round(t_stat, 3))

print("p-value:",
      round(p_value, 4))

# Decision
if p_value < alpha:
    print("\nReject H0")
    print("The treatment has a statistically significant effect.")
else:
    print("\nFail to reject H0")
    print("There is insufficient evidence of a significant effect.")

# Visualization
plt.boxplot(
    [control, treatment],
    labels=["Control", "Treatment"]
)

plt.ylabel("Outcome")
plt.title("Control vs Treatment Group")

# Display p-value on graph
plt.text(
    1.5,
    max(data["outcome"]) + 1,
    f"p-value = {p_value:.4f}",
    ha="center"
)

plt.show()