from flask import Flask
from backend.config import Config
from backend.database import db
import os

app = Flask(__name__)
app.config.from_object(Config)
print('cwd', os.getcwd())
print('dburi', app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)
with app.app_context():
    print('engine url', db.engine.url)
    conn = db.engine.connect()
    print('direct connect ok')
    conn.close()
    from backend.models import user, location
    try:
        db.create_all()
        print('create_all ok')
    except Exception as e:
        print('create_all ERROR', repr(e))
