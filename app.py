import pymysql
import os
from flask import Flask

from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    #  Auto-create database if it doesn't exist 
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        conn.commit()
        conn.close()
        print(f"Verified database: {Config.DB_NAME}")
    except Exception as e:
        print(f"Could not auto-create database: {e}")

    # Init extensions 
    db.init_app(app)
    login_manager.init_app(app)

    #  User loader 
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #  Register blueprints 
    from routes import main, auth, inv
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(inv)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)