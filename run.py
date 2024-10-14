from flask import Flask
from app import create_app


def index():
    return 'Welcome to Macau!'

app = create_app()

if __name__ == "__main__":
    app.run(debug=True , ssl_context=('./ssl/fullchain.pem', './ssl/privkey.key'),host='0.0.0.0')
    debug=True
    #那麼修改代碼後不用重启項目就能更新
    