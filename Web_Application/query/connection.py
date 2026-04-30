import sqlite3
import os

# Path to database
DB_PATH = os.path.join(os.getcwd(), "coursework.db")
# Helper function to run queries
def run_query(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        import pandas as pd
        return pd.read_sql_query(query, conn, params=params)