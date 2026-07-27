from flask import Flask
from backend.config import Config
from backend.database import db
import os

app = Flask(__name__)
app.config.from_object(Config)
print('cwd', os.getcwd())
print('dburi', app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)
from backend.models import user, location
with app.app_context():
    db.create_all()
    print('create_all ok')
