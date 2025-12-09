import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
 
 
# -----------------------------------------
# Initialize Supabase Client
# -----------------------------------------
def get_supabase_client():
    load_dotenv()
 
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
 
    if not url or not key:
        raise ValueError("Missing Supabase URL or Supabase KEY in .env")
 
    return create_client(url, key)
 
 
# -----------------------------------------
# Create iris_data table (if not exists)
# -----------------------------------------
def create_table_if_not_exists():
    try:
        supabase = get_supabase_client()
 
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS iris_data (
            id BIGSERIAL PRIMARY KEY,
            sepal_length FLOAT,
            sepal_width FLOAT,
            petal_length FLOAT,
            petal_width FLOAT,
            species TEXT,
            sepal_ratio FLOAT,
            petal_ratio FLOAT,
            is_petal_long INTEGER
        );
        """
 
        try:
            supabase.rpc("execute_sql", {"query": create_table_sql}).execute()
            print("Table 'iris_data' created or already exists.")
        except Exception as e:
            print(f"RPC failed: {e}")
            print("Assuming table already exists or will auto-create.")
 
    except Exception as e:
        print(f"Error creating table: {e}")
        print("Continuing with data insertion...")
 
 
# -----------------------------------------
# Load CSV into Supabase
# -----------------------------------------
def load_to_supabase(staged_path: str, table_name: str = "iris_data"):
 
    # Convert to absolute path if needed
    if not os.path.isabs(staged_path):
        staged_path = os.path.abspath(os.path.join(os.path.dirname(__file__), staged_path))
 
    print(f"Looking for the data file at: {staged_path}")
 
    if not os.path.exists(staged_path):
        print(f"Error: File not found at {staged_path}")
        print("Run transform_iris.py first.")
        return
 
    try:
        supabase = get_supabase_client()
 
        df = pd.read_csv(staged_path)
        total_rows = len(df)
        batch_size = 50
 
        print(f"Loading {total_rows} rows into table '{table_name}'...")
 
        # Insert in batches
        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i: i + batch_size].copy()
 
            # Replace NaN with None (Supabase requires None for NULL)
            batch = batch.where(pd.notnull(batch), None)
 
            records = batch.to_dict("records")
 
            try:
                supabase.table(table_name).insert(records).execute()
 
                end = min(i + batch_size, total_rows)
                print(f"Inserted rows {i + 1} – {end} of {total_rows}")
 
            except Exception as e:
                print(f"Error in batch {i // batch_size + 1}: {str(e)}")
                continue
 
        print(f"Finished loading data into '{table_name}'.")
 
    except Exception as e:
        print(f"Error loading data: {e}")
 
 
# -----------------------------------------
# Main Execution
# -----------------------------------------
if __name__ == "__main__":
 
    staged_csv_path = os.path.join("..", "data", "staged", "iris_transformed.csv")
 
    create_table_if_not_exists()
    load_to_supabase(staged_csv_path)
    