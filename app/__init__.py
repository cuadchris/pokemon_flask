from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db, User

from .user.routes import user


app = Flask(__name__)

login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

login.login_view = 'login'

app.config.from_object(Config)

app.register_blueprint(user)

db.init_app(app)
migrate = Migrate(app, db)

from app import routes, models