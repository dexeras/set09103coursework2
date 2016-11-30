from flask import Flask, render_template, url_for, request, session, g, redirect, flash
import sqlite3
from datetime import datetime, date
import bcrypt

app=Flask(__name__)
db_location='var/sqlite3.db'
app.secret_key = '>\xa9\xbf\x06b^\xcc}b\x1dn\xea\x92j\\\x84\xce\xdb9\x8dr\x0b\xfd\xdf'

def get_db():
  db=getattr(g,'db',None)
  if db is None:
    db=sqlite3.connect(db_location)
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
@app.route('/<message>',methods=['GET','POST'])
def index(message=None):
  if(message != None):
    flash(message)
  try:
    if session['user_name']:
      db=get_db()
      query='select Blubbers.UserName,Blubs.Content,Blubs.Time from Blubs,Blubbers where Blubs.Author=Blubbers.UserName'
      blubs=db.cursor().execute(query)
      listBlubs=[]
      for row in blubs:
        listBlubs.append(row)
      db.close()
      return render_template('index.html',user_name=session['user_name'],listBlubs=listBlubs)
  except KeyError:
    pass
  if request.method =="GET":
    return render_template('login.html')
  else:
    db=get_db()
    userName = request.form['user_name']
    typedPassword = request.form['password']
    query='select Password from Blubbers where UserName="'+userName+'"'
    result=db.cursor().execute(query)
    password=[]
    for row in result:
      password.append(row)
    if password:
      password=password[0][0]
      query='select * from Blubbers where UserName="'+userName+'" and Password="'+bcrypt.hashpw(typedPassword.encode('utf-8'),password)+'"'
      result=db.cursor().execute(query)
      blubber=[]
      for row in result:
        blubber.append(row)
      if blubber:
        session['user_name'] = blubber[0][0]
        message = 'Succesfully logged in!'
        return redirect(url_for('index',message=message))
  return redirect(url_for('index'))

@app.route('/disconnect')
def disconnect():
  session.pop('user_name',None)
  return redirect(url_for('index'))

@app.route('/createAccount',methods=['GET','POST'])
@app.route('/createAccount/<message>',methods=['GET','POST'])
def create_account(message=None):
  if(message != None):
    flash(message)
  if request.method=="GET":
    return render_template('createAccount.html')
  else:
    db=get_db()
    print request.form
    userName=request.form['user_name']
    query='select * from Blubbers where UserName="'+userName+'"'
    result=db.cursor().execute(query)
    accounts=[]
    for row in result:
      accounts.append(row)
    if accounts:
      message='A blubber with the same name already exists'
      return redirect(url_for('create_account',message=message))
    password=request.form['password']
    print userName
    print password
    query='insert into Blubbers(UserName,Password)values("'+userName+'","'+bcrypt.hashpw(password,bcrypt.gensalt())+'")'
    db.cursor().execute(query)
    db.commit()
    message='Account succesfully created!'
    return redirect(url_for('index',message=message))

@app.route('/blub',methods=['GET','POST'])
def blub():
  db=get_db()
  if request.method=="GET":
    return render_template('blub.html')
  else:
    print request.form
    user_name=session['user_name']
    content=request.form['content']
    print user_name
    print content
    now=datetime.now()
    print now
    now=now.strftime('%d/%m/%Y at %H:%M')
    print now
    query='insert into Blubs(Author,Content,Time)values("'+user_name+'","'+content+'","'+now+'")'
    db.cursor().execute(query)
    db.commit()
    message='You succesfully blubbed!'
    return redirect(url_for('index',message=message))

@app.route('/blubber/<blubber>')
def blubber(blubber):
  db=get_db()
  query='select * from Blubs where Author="'+blubber+'"'
  result=db.cursor().execute(query)
  blubberBlubs=[]
  for row in result:
    blubberBlubs.append(row)
  return render_template('blubber.html',blubberBlubs=blubberBlubs)

@app.errorhandler(404)
def page_not_found(error):
  return"This page doesn't exist",404

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)
