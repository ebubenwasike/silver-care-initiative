import mysql.connector
from mysql.connector import Error
from database.models import db

def get_mysql_connection():
    """Create direct MySQL connection for manual queries"""
    try:
        connection = mysql.connector.connect(
            host='project275',
            user='project275',
            password='project275',  # Fixed typo
            database='mydatabase'   # Fixed typo
        )
        return connection
    except Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        return None


def init_database(app):
    """Initialize SQLAlchemy with Flask app"""
    db.init_app(app)
    print("✅ Database connected to Flask app")


def create_tables(app):
    """Create all tables in MySQL database"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ All database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")


def test_mysql_connection():
    """Test direct MySQL connection"""
    connection = get_mysql_connection()
    if connection:
        print("✅ Direct MySQL connection successful")
        connection.close()
        return True
    else:
        print("❌ Direct MySQL connection failed")
        return False


def execute_raw_sql(query, params=None):
    """Execute raw SQL queries for complex operations"""
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().lower().startswith('select'):
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"❌ SQL Execution Error: {e}")
            return None
    return None
