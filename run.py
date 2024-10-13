from flask import Flask
from app import create_app


def index():
    return 'Welcome to Macau!'

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    debug=True
    #那麼修改代碼後不用重启項目就能更新
    