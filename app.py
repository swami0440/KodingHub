from flask import Flask, render_template, request, session, redirect
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

app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b39d11e9fe9bb9:284f46990974059@us-cdbr-east-02.cleardb.com/heroku_df998aa187223ac'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

CORS(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Blog_home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(100), nullable=False)
    blog_intro = db.Column(db.String(300), nullable=False)
    blog_image_name = db.Column(db.String(21), nullable=False)
    blog_slug = db.Column(db.String(120), nullable=False)
    blog_category = db.Column(db.String(12), nullable=False)


class Sub_blog(db.Model):
    idsub_blog = db.Column(db.Integer, primary_key=True)
    sub_blog_title = db.Column(db.String(100), nullable=False)
    sub_blog_intro = db.Column(db.String(300), nullable=False)
    sub_blog_image = db.Column(db.String(20), nullable=False)
    blog_fk_id = db.Column(db.Integer, db.ForeignKey('Blog_home.id'), nullable=False)
    sub_blog_date = db.Column(db.String(12), nullable=True)
    sub_blog_slug = db.Column(db.String(25), nullable=False)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    if request.method == "GET":
        blogs = Blog_home.query.filter_by().all()[0:params['no_of_posts']]
        return render_template("index.html", blogs=blogs)


@app.route('/about')
@cross_origin()
def about():
    return render_template("about.html")


@app.route('/sub-blog-list/<blog_id>')
@cross_origin()
def sub_blog_list(blog_id):
    sub_blogs = Sub_blog.query.filter_by(blog_fk_id=blog_id).all()
    return render_template("blog-list.html", sub_blogs=sub_blogs)


@app.route('/blog/<page_name>')
@cross_origin()
def blog(page_name):
    return render_template("blogs/" + page_name)


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('dashboard.html')

    if request.method == 'POST':
        userpass = request.form.get('password')
        if userpass == params['admin-password']:
            # set the session variable
            session['user'] = "pratik"
            return render_template('dashboard.html')

    return render_template("login.html")


@app.route('/dash/<name>', methods=['GET', 'POST'])
@cross_origin()
def blog_dashboard(name):
    if request.method == 'GET' and 'user' in session and session['user'] == params['admin_user'] and name == "blog":
        blogs = Blog_home.query.filter_by().all()
        return render_template("blog-dashboard.html", blogs=blogs)

    elif request.method == 'GET' and 'user' in session and session['user'] == params[
        'admin_user'] and name == "subblog":

        return render_template("sub-blog-dashboard.html")

    return render_template("login.html")


@app.route('/portfolio')
@cross_origin()
def portfolio():
    return render_template("portfolio.html")


@app.route('/contact', methods=['GET', 'POST'])
@cross_origin()
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        print(name, phone, email, message)
        print(type(name), type(phone), type(email), type(message))
        entry = Contacts(name=name, email=email, phone=phone, date=datetime.now(), message=message)
        # entry = ('pratik','fdfd@dfd.d','88888','fdfdf','dfdfdfdf')
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n Phone Number:" + phone + "\n Mail from :" + email
                          )

    return render_template("contact.html")


# Edit blog function
@app.route('/blog-edit/<blog_id>', methods=['GET', 'POST'])
@cross_origin()
def blog_edit(blog_id):

    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            blog_title = request.form.get('blog_title')
            blog_intro = request.form.get('blog_intro')
            blog_image_name = request.form.get('blog_image_name')
            blog_slug = request.form.get('blog_slug')
            blog_category = request.form.get('blog_category')

            if blog_id == '0':
                blog_home = Blog_home(blog_title=blog_title, blog_intro=blog_intro, blog_image_name=blog_image_name,
                                      blog_slug=blog_slug, blog_category=blog_category)
                db.session.add(blog_home)
                db.session.commit()
            else:
                current_blog = Blog_home.query.filter_by(id=blog_id).first()
                current_blog.blog_title = blog_title
                current_blog.blog_intro = blog_intro
                current_blog.blog_image_name = blog_image_name
                current_blog.blog_slug = blog_slug
                current_blog.blog_category = blog_category
                db.session.commit()
                blogs = Blog_home.query.filter_by().all()
                return render_template("blog-dashboard.html", blogs=blogs)
        current_blog = Blog_home.query.filter_by(id=blog_id).first()
        return render_template('edit-blog.html', blog=current_blog, blog_id=blog_id)


# Delete blog function
@app.route('/blog-delete/<blog_id>', methods=['GET', 'POST'])
@cross_origin()
def blog_delete(blog_id):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'GET':
            Blog_home.query.filter_by(id=blog_id).delete()
            db.session.commit()
            blogs = Blog_home.query.filter_by().all()
            return render_template("blog-dashboard.html", blogs=blogs)


if __name__ == '__main__':

    # app.run(port=8000, debug=True)
    db.init_app(app)
    app.run(debug=True)
