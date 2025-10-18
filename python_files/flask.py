from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#  Create MySQL connection
con = mysql.connector.connect(
    host='project275',
    user='project275',
    password='project275',   # Fixed typo
    database='mydatabase'    # Fixed typo
)

@app.route('/getTable', methods=['GET'])
def get_tables():
    try:
        cursor = con.cursor()  # Fixed typo: was 'cursoe'
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()

        #  Convert list of tuples into list of table names
        table_names = [table[0] for table in tables]
        return jsonify({"tables": table_names}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":   # Fixed typo: was `" main "`
    print("Connecting to database...")
    app.run(debug=True)
