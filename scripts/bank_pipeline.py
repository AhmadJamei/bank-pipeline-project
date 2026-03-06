import os
import pandas as pd
import sqlite3
import json
import matplotlib.pyplot as plt
import random

# Paths
DATA_DIR = "/home/ahmad/data-pipeline-project/data"
DB_PATH = "/home/ahmad/data-pipeline-project/database/sales.db"

# -----------------------------
# 1. Data simulation
# -----------------------------

# JSON same as bank customer
customers = []
for i in range(1, 301):  # abaout 300 records
    customers.append({
        "customer_id": i,
        "name": f"Customer {i}",
        "account_type": random.choice(["Checking", "Savings", "Investment"]),
        "balance": random.randint(500, 5000)
    })

with open(os.path.join(DATA_DIR, "bank_customers.json"), "w") as f:
    json.dump(customers, f)

# Excel same as accouts
accounts = []
for i in range(1, 301):
    accounts.append({
        "account_id": 1000 + i,
        "customer_id": i,
        "transactions": random.randint(1, 20),
        "total": random.randint(500, 5000)
    })

df_accounts = pd.DataFrame(accounts)
excel_path = os.path.join(DATA_DIR, "bank_accounts.xlsx")
df_accounts.to_excel(excel_path, index=False)

# -----------------------------
# 2. Read data
# -----------------------------
json_path = os.path.join(DATA_DIR, "bank_customers.json")
with open(json_path, "r") as f:
    df_customers = pd.DataFrame(json.load(f))

df_accounts = pd.read_excel(excel_path)

# -----------------------------
# 3. Clean data
# -----------------------------
df_customers.fillna(0, inplace=True)
df_accounts.fillna(0, inplace=True)

#  Delete duplicate records
df_customers.drop_duplicates(subset="customer_id", inplace=True)
df_accounts.drop_duplicates(subset="account_id", inplace=True)

# -----------------------------
# 4. Data integration
# -----------------------------
df_merged = pd.merge(df_customers, df_accounts, on="customer_id")
df_merged["total_balance"] = df_merged["balance"] + df_merged["total"]

# ُShow sapmle data
print(df_merged.head())

# -----------------------------
# 5. Save data into SQLite
# -----------------------------
conn = sqlite3.connect(DB_PATH)
df_merged.to_sql("customers", conn, if_exists="replace", index=False)
conn.close()

# -----------------------------
# 6. Simple diagram
# -----------------------------
summary = df_merged.groupby("account_type")["total_balance"].sum()
summary.plot(kind="bar", title="Total Balance by Account Type")
plt.ylabel("Total Balance")
plt.xlabel("Account Type")
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "total_balance_chart.png"))
plt.show()
