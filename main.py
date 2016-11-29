from flask import Flask, render_template, url_for, request, session, g, redirect
import sqlite3

app=Flask(__name__)
db_location='var/database.db'
app.secret_key = '>\xa9\xbf\x06b^\xcc}b\x1dn\xea\x92j\\\x84\xce\xdb9\x8dr\x0b\xfd\xdf'

def get_db():
  db=getattr(g,'db',None)
  if db is None:
    db.sqlite3.connect(db_location)
    g.db = db
    db.text_factory=str
  return db

@app.teardown_appcontext
def close_db_connection(exception):
  db=getattr(g,'db',None)
  if db is not None:
    db.close()

def init_db():
  with app.app_context():
    db=get_db()
    with app.open_resource('schema.sql',mode='r')as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.route('/',methods=['GET','POST'])
def index():
  try:
    if(session['user_name']):
      return render_template('index.html', user_name=session['user_name'])
  except KeyError:
    pass
  if request.method =="GET":
    return render_template('login.html')
  else:
    session['user_name'] = request.form['user_name']
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
  return"This page doesn't exist",404

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)
