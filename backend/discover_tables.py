# backend/discover_tables.py
import sqlite3
import os

# --- This new section makes the script more reliable ---
# It finds the absolute path to the script itself.
script_dir = os.path.dirname(os.path.abspath(__file__))
# Then, it creates the full path to the database file.
db_path = os.path.join(script_dir, 'dashboard.db')

print(f"-> Attempting to connect to database at: {db_path}")

# First, check if the file actually exists at that path.
if not os.path.exists(db_path):
    print(f"\n[ERROR] The database file was not found.")
    print("Please make sure 'dashboard.db' is in the same 'backend' folder as this script.")
else:
    try:
        # Connect to the database using the full, absolute path.
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("-> Connection successful.")

        # Query the database for table names.
        print("-> Querying for table names...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        tables = cursor.fetchall()

        if not tables:
            print("\n[RESULT] No tables were found in the database.")
            print("This could mean the database is empty or was not created correctly.")
        else:
            print("\n[RESULT] Found the following tables in dashboard.db:")
            for table in tables:
                print(f"  - {table[0]}")

    except Exception as e:
        print(f"\n[ERROR] An error occurred while reading the database: {e}")
    finally:
        # Ensure the connection is closed if it was opened.
        if 'conn' in locals() and conn:
            conn.close()
            print("-> Connection closed.")