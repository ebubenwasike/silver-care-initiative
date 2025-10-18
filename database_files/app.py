from flask import Flask
from database.models import db
from database.database_connection import init_database, create_tables
from database.seed_data import create_sample_data

app = Flask(__name__)

#  Configure MySQL database connection for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://project275:project275@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Initialize SQLAlchemy with Flask
init_database(app)

@app.route('/')
def home():
    return "Flask connected to MySQL successfully!"

if __name__ == '__main__':
    with app.app_context():
        create_tables(app)       # Create all tables
        create_sample_data(app)  # Insert sample data
    app.run(debug=True)
