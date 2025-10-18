from database.database_connection import execute_raw_sql

if __name__ == "__main__":
    # Example: Fetch all rows from the 'users' table
    query = "SELECT * FROM users;"
    result = execute_raw_sql(query)

    if result:
        print("✅ Query executed successfully! Results:")
        for row in result:
            print(row)
    else:
        print("❌ Query failed or returned no data.")
