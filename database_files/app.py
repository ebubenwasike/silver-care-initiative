from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your MySQL details 👇
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a table (model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Route to test connection
@app.route('/')
def home():
    return "MySQL Database connected successfully!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the table inside 'flaskdb'
    app.run(debug=True)
