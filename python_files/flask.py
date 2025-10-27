from flask import Flask, render_template
import mysql.connector
app = Flask(__name__)

con=mysql.connector.connect(
    host='project275',
    user='project275',
    password='projecy275',
    database='mydatabse'
)

@app.route('/getTable',methods=['GET'])
def get_tables():
    cursor=con.cursoe()
    cursor.execute("SHOW TABLES;")
    tables=cursor.fetchall()
    cursor.close()
    con.close()
    table_names=[table[0] for table in tables]
    return jsonify({"tables":table_names}),200

if  __name__==" main ":
    print("connecting to database")
    app.run(debug=True)
