from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Competition(Resource):
    def get(self, name):
        return{'competition': name}

api.add_resource(Competition, '/competition/<string:name>')

app.run(port=5004)
