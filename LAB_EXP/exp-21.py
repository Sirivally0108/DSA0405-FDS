import numpy as np

# Load data from CSV
data = np.genfromtxt(
    "rare_elements.csv",
    delimiter=",",
    skip_header=1
)

# User inputs
n = int(input("Enter sample size: "))
confidence = float(input("Enter confidence level (%): "))
precision = float(input("Enter desired precision: "))

# Check sample size
if n > len(data):
    print("Sample size is greater than available data.")
else:

    # Select random sample
    np.random.seed(42)
    sample = np.random.choice(data, n, replace=False)

    # Point estimate
    sample_mean = np.mean(sample)

    # Sample standard deviation
    sample_std = np.std(sample, ddof=1)

    # Standard error
    standard_error = sample_std / np.sqrt(n)

    # Z values for common confidence levels
    z_values = {
        90: 1.645,
        95: 1.96,
        99: 2.576
    }

    if confidence not in z_values:
        print("Use 90, 95, or 99 as confidence level.")
    else:

        z = z_values[confidence]

        # Margin of error
        margin_error = z * standard_error

        # Confidence interval
        lower = sample_mean - margin_error
        upper = sample_mean + margin_error

        print("\nPoint Estimate (Sample Mean):",
              round(sample_mean, 3))

        print("Standard Error:",
              round(standard_error, 3))

        print("Margin of Error:",
              round(margin_error, 3))

        print(
            f"{confidence}% Confidence Interval: "
            f"({lower:.3f}, {upper:.3f})"
        )

        if margin_error <= precision:
            print("Desired precision is achieved.")
        else:
            print("Desired precision is not achieved.")