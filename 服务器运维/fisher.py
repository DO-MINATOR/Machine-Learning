from app import app
from app.web import web
from flask_login import LoginManager
from app.db import db

login_manager = LoginManager()

app.register_blueprint(web)

app.config.from_object('secure')
app.config.from_object('setting')
login_manager.init_app(app)
login_manager.login_view='web.login'
login_manager.login_message='请先登录'
db.init_app(app)
db.create_all(app=app)

if __name__ == '__main__':
    app.run(port=8000, debug=app.config['DEBUG'])
