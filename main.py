# -*- coding: utf-8 -*-
import json

from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig,DatabaseConfig

app = Flask(__name__)

app.config.from_object(DevConfig)
app.config.from_object(DatabaseConfig)

db = SQLAlchemy(app)

class record(db.Model):
    USERNAME = db.Column(db.String(5), primary_key = True,nullable=False)
    PASSWORD = db.Column(db.String(10), nullable = False)


@app.route('/register', methods = ['GET','POST'])
def reg():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        try:
            USERNAME = data['userid'].strip()
            PASSWORD = data['psw']
            if(USERNAME == '' or PASSWORD == ''):
                raise ValueError
            user = record(USERNAME = USERNAME, PASSWORD =PASSWORD)
            db.session.add(user)
        except ValueError:
            return '注册不合规，请检查'
        db.session.commit()
        db.session.close()
        print('committed!')
        return ''

@app.route('/home',methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/', methods = ['GET','POST'])
def index():
    all_data = record.query.all()
    if request.method == 'GET':
        return render_template('index.html',data = all_data)
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        USERNAME = str(data['USERNAME'])
        PASSWORD = str(data['PASSWORD'])
        try:
            x = record.query.filter_by(USERNAME = USERNAME).one()
            if (str(x.PASSWORD) == PASSWORD):
                print("welcome!")
            return ''
        except:
            pass
            return 'ERROR'


if __name__ == '__main__':
    app.run(host='0.0.0.0')