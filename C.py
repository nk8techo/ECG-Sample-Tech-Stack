import pandas as pd
import numpy as np


def process_data():
    # Generate random data
    data = {
        "A": np.random.randint(1, 100, 10),
        "B": np.random.rand(10),
    }
    df = pd.DataFrame(data)

    # Display original data
    print("Original Data:")
    print(df)

    # Normalize column 'A'
    df["A_normalized"] = (df["A"] - df["A"].min()) / (df["A"].max() - df["A"].min())

    print("\nData with normalized A column:")
    print(df)

    # Bin column 'A' into 4 equal-sized bins
    bins = np.linspace(df["A"].min(), df["A"].max(), 5)
    df["A_bin"] = pd.cut(df["A"], bins=bins, include_lowest=True)

    # Aggregate mean of 'B' for each bin of 'A'
    aggregated = df.groupby("A_bin").agg({"B": "mean"})

    print("\nAggregated data (mean of B by A bins):")
    print(aggregated)


if __name__ == "__main__":
    process_data()
