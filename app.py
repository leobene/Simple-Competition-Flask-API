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
        return{'competicao': None}, 404

    def post(self, name):
        competition = {'competicao': name, 'atleta':"Bolt", 'value': 12.00, 'unidade': "s" }
        competitions.append(competition)
        return competition, 201

class CompetitionList(Resource):
    def get(self):
      return {'competicoes': competitions}

api.add_resource(Competition, '/competition/<string:name>')
api.add_resource(CompetitionList, '/competitions')

app.run(port=5006, debug=True)
