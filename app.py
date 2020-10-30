from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail
import pymysql

with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b39d11e9fe9bb9:284f46990974059@us-cdbr-east-02.cleardb.com/heroku_df998aa187223ac'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

CORS(app)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

@app.route('/')
@cross_origin()
def home():
    return render_template("index.html")


@app.route('/about')
@cross_origin()
def about():
    return render_template("about.html")


@app.route('/blog-list')
@cross_origin()
def blog_list():
    return render_template("blog-list.html")


@app.route('/blog')
@cross_origin()
def blog():
    return render_template("blog-post.html")


@app.route('/portfolio')
@cross_origin()
def portfolio():
    return render_template("portfolio.html")


@app.route('/contact', methods = ['GET', 'POST'])
@cross_origin()
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        print(name,phone,email,message)
        print(type(name),type(phone),type(email),type(message))
        entry = Contacts(name=name, email=email, phone=phone, date=datetime.now(), message=message )
        #entry = ('pratik','fdfd@dfd.d','88888','fdfdf','dfdfdfdf')
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n Phone Number:" + phone+ "\n Mail from :" + email
                          )

    return render_template("contact.html")


if __name__ == '__main__':
    #app.run(port=8000, debug=True)
    db.init_app(app)
    app.run(debug=False)