import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://user:Abc123456@83.229.126.125:3306/tdm_database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
