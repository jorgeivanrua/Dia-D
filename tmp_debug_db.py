import os
from backend.config import Config
print('CWD:', os.getcwd())
print('DB URI:', Config.SQLALCHEMY_DATABASE_URI)
if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
    rel = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    print('DB abs path:', os.path.abspath(rel))
else:
    print('Non-sqlite config')
