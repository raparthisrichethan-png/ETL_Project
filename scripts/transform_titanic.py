import os
import pandas as pd
from extract_titanic import extract_data  # use titanic extractor


def transform_data(raw_path: str) -> str:
    # Base and staged directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_dir = os.path.join(base_dir, "data", "staged")
    os.makedirs(staged_dir, exist_ok=True)

    # Read raw data
    df = pd.read_csv(raw_path)

    # 1. Handling missing values

    # Numeric columns in typical Titanic dataset
    numeric_cols = ["survived", "pclass", "age", "sibsp", "parch", "fare"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Categorical
    categorical_cols = ["sex", "embarked", "class", "who",
                        "deck", "embark_town", "alive", "alone"]

    for col in categorical_cols:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # 2. Feature Engineering (optional examples)
    if "age" in df.columns:
        df["is_child"] = (df["age"] < 18).astype(int)

    # Example: family size = sibsp + parch + 1 (self)
    if "sibsp" in df.columns and "parch" in df.columns:
        df["family_size"] = df["sibsp"] + df["parch"] + 1

    # 3. Drop unnecessary columns 
    
    cols_to_drop = ["passengerid"]  
    df.drop(columns=[c for c in cols_to_drop if c in df.columns],
            inplace=True, errors="ignore")

    # 4. Save transformed data
    staged_path = os.path.join(staged_dir, "titanic_transformed.csv")
    df.to_csv(staged_path, index=False)

    print(f"Data transformed and saved to {staged_path}")
    return staged_path

if __name__ == "__main__":
    from extract_titanic import extract_data
    raw_path = extract_data()  
    transform_data(raw_path)
