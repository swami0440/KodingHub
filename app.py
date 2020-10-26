from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


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


if __name__ == '__main__':
    #app.run(port=8000, debug=True)
    app.run(debug=True)