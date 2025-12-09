import os
import seaborn as sns
import pandas as pd

# Function to extract and save the data


def extract_data():
    base_dr = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dr, "data", "raw")
    os.makedirs(data_dir, exist_ok=True)
    df = sns.load_dataset("titanic")
    raw_path = os.path.join(data_dir, "titanic_raw.csv")
    df.to_csv(raw_path, index=False)
    print(f"Data extracted and saved to {raw_path}")
    return raw_path


if __name__ == "__main__":
    extract_data()