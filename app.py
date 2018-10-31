from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

competitions = [{
  'competicao': '100m',
  'atleta': 'Joao das Neves',
  'value': 10.234,
  'unidade': 's'
}]

class Competition(Resource):
    def get(self, name):
        for competition in competitions:
            if competition['competicao'] == name:
               return competition

    def post(self, name):
        competition = {'competicao': name, 'atleta':"Bolt", 'value': 12.00, 'unidade': "s" }
        competitions.append(competition)
        return competition

api.add_resource(Competition, '/competition/<string:name>')

app.run(port=5006)
