from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

"""
這是初始化數據庫的工具類
跟後端程序沒有聯繫
只有要重新配置數據庫時才用管
"""

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


def initialize_database():
    with app.app_context():
        with open('create_tables.sql', 'r') as f:
            sql_commands = f.read()
        db.engine.execute(sql_commands)
        print("All tables created")


def drop_database():
    with app.app_context():
        db.engine.execute("DROP TABLE IF EXISTS User, Post")
        print("All tables dropped")


if __name__ == '__main__':
    # 初始化数据库
    initialize_database()

    # 删除数据库
    # drop_database()
