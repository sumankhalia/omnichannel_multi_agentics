import sqlite3
import pandas as pd

DB_PATH = "omni.db"

def run_query(sql_query):

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(sql_query, conn)
        conn.close()
        return df

    except Exception as e:
        return f"SQL_ERROR: {str(e)}"
