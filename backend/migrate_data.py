# backend/migrate_data.py

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# This will load environment variables from a .env file.
load_dotenv()

# --- SOURCE DATABASE (Your local machine) ---
# CORRECTED: This section now builds an absolute path to the database file.
# This makes the script work correctly no matter which directory you run it from.
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'dashboard.db')
local_db_url = f"sqlite:///{db_path}"

print(f"-> Attempting to connect to local SQLite database at: {db_path}")
local_engine = create_engine(local_db_url)
print("-> Connection to local SQLite database successful.")


# --- DESTINATION DATABASE (Your live database on Render) ---
# This gets the connection URL you set in your terminal.
render_db_url_from_env = os.getenv("RENDER_DATABASE_URL")

# Check if the URL was provided.
if not render_db_url_from_env:
    print("\n[ERROR] RENDER_DATABASE_URL environment variable is not set.")
    print("Please set it before running the script.")
    print("Example command: export RENDER_DATABASE_URL='your_postgres_url_here'")
    exit()

# Adjust the URL for SQLAlchemy if it starts with "postgres://"
if render_db_url_from_env.startswith("postgres://"):
    render_db_url = render_db_url_from_env.replace("postgres://", "postgresql://", 1)
else:
    render_db_url = render_db_url_from_env

print(f"-> Attempting to connect to Render PostgreSQL database...")
render_engine = create_engine(render_db_url)
print("-> Connection to Render PostgreSQL database successful.")


# --- DATA MIGRATION PROCESS ---
# The table names discovered in the previous step.
tables_to_migrate = ['business_summaries', 'hirings']
print("\nStarting data migration...")

for table_name in tables_to_migrate:
    try:
        print(f"  - Migrating table: '{table_name}'...")
        df = pd.read_sql_table(table_name, local_engine)
        
        df.to_sql(table_name, render_engine, if_exists='replace', index=False)
        
        print(f"  - SUCCESS: Migrated {len(df)} rows to '{table_name}'.")
    except Exception as e:
        print(f"  - FAILED to migrate table '{table_name}': {e}")

print("\nMigration process complete!")
