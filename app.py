from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8000, debug=True)
