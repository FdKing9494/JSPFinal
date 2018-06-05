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
        try:
            USERNAME = data['USERNAME'].strip()
            PASSWORD = data['PASSWORD']
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

@app.route('/', methods = ['GET','POST'])
def index():
    all_data = record.query.all()
    # x = all_data['USERNAME']
    if request.method == 'GET':
        return render_template('index.html',data = all_data)
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        USERNAME = data['USERNAME']
        PASSWORD = data['PASSWORD']
        x = record.query.filter_by(USERNAME = USERNAME).one()
        if (x.password == PASSWORD):
            print("welcome!")


@app.route('/submit',methods = ['GET','POST','DELETE','PATCH'])
def submit():
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        try:
            USERNAME = data['USERNAME'].strip()
            PASSWORD = data['PASSWORD']
            if(USERNAME == '' or PASSWORD == ''):
                raise ValueError
            user = record(USERNAME = USERNAME,PASSWORD = PASSWORD)
            db.session.add(user)
        except ValueError:
            return '用户名或密码未填写，请重新填写'
        db.session.commit()
        db.session.close()
        print('写入成功！')
        return ''

    if request.method == 'DELETE':
        data = json.loads(request.data.decode('utf-8'))
        USERNAME = data['USERNAME'].strip()
        print(USERNAME)
        all_data = record.query.all()
        try:
            x = record.query.filter_by(USERNAME = USERNAME).one()
            db.session.delete(x)
        except:
            pass
        db.session.commit()
        return ''

    if request.method == 'PATCH':
        data = json.loads(request.data.decode('utf-8'))
        USERNAME = data['USERNAME'].strip()
        PASSWORD = data['PASSWORD']
        if(USERNAME == '' or PASSWORD == ''):
            raise ValueError
        try:
            x = record.query.filter_by(USERNAME = USERNAME).one()
            x.PASSWORD = PASSWORD
        except:
            pass
        finally:
            db.session.close()
        print('提交成功！')
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0')