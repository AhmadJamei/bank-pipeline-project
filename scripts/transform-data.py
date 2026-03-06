import pandas as pd
import sqlite3
import json
import os

# Path data
DATA_DIR = "/home/ahmad/data-pipeline-project/data"
DB_PATH = "/home/ahmad/data-pipeline-project/database/sales.db"

# Read JSON
with open(os.path.join(DATA_DIR, "sales.json"), "r") as f:
    json_data = json.load(f)

df_json = pd.DataFrame(json_data)

# Read Excel
df_excel = pd.read_excel(os.path.join(DATA_DIR, "sales.xlsx"))

# Combine numbers
df = pd.concat([df_json, df_excel], ignore_index=True)

# Cleaning data
df["quantity"] = df["quantity"].fillna(0)  # Empty  quantity equal to zero
df["total_price"] = df["quantity"] * df["price"]

# Save into SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql("sales", conn, if_exists="replace", index=False)

#  Run a simple query
result = pd.read_sql_query("SELECT product, SUM(total_price) as revenue FROM sales GROUP BY product", conn)
print(result)

conn.close()
