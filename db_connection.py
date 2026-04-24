from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- YOUR DATABASE CONFIGURATION ---
# Format: mysql+pymysql://user:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123@127.0.0.1:3306/adbms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# A simple model to test the connection
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def index():
    try:
        # This simple command checks if the database is reachable
        db.session.execute(db.text('SELECT 1'))
        return "<h1>Success!</h1><p>Connected to the 'adbms' database.</p>"
    except Exception as e:
        return f"<h1>Connection Failed</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    # This creates the tables in your MySQL database automatically
    with app.app_context():
        db.create_all()
    app.run(debug=True)