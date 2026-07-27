from sqlalchemy import create_engine
engine = create_engine('sqlite:///instance/electoral.db')
print('Engine created ->', engine.url)
try:
    conn = engine.connect()
    print('Connected')
    res = conn.execute('SELECT 1')
    print('Query OK', list(res))
    conn.close()
except Exception as e:
    print('ERROR', repr(e))
