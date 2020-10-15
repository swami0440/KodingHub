from html.entities import name

from flask import  Flask
from flask_restful import  Resource,Api

app = Flask(__name__)
api = Api(app)

data = []
class CrudOperations(Resource):
    def get(self):
       for d in data:
           if d['data'] == name:
               return d
        return {'data': 'none'}


    def post(self, name):
        tmp = {
            'data': name
        }
        data.append(tmp)
        return tmp

    def delete(self, instance):
        pass
