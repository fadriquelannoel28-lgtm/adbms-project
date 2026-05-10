import os 

class Config:
    DB_USER = 'root'
    DB_PASSWORD = 'Admin123'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_NAME = 'medstock'

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'medsave_key'

    UPLOAD_FOLDER = os.path.join('static', 'images', 'ids')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 