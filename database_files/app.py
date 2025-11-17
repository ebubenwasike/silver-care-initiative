from flask import Flask
from database_files.models import db
from database_files.database_connection import init_database, create_tables
from database_files.seed_data import create_sample_data


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


    from flask import jsonify
from database.models import User  # make sure this import exists

@app.route('/users')
def get_users():
    """Display all users in JSON format"""
    users = User.query.all()  # fetch all users from DB
    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(user_list)

