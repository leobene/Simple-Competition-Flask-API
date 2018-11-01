from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

competitions = [{
  'competicao': '100m',
  'ranking': {},
  'isFinished': False,
  'numTrys': 1
}]

entrys = [{
  'competicao': '100m',
  'atleta': 'Joao das Neves',
  'value': 10.234,
  'unidade': 's'
}]

class Entry(Resource):
    def get(self, name):
        for entry in entrys:
            if entry['competicao'] == name:
               return entry
        return{'competicao': None}, 404

    def post(self, name):
        data = request.get_json()
        entry = {'competicao': name, 'atleta':data['atleta'], 'value': data['value'], 'unidade': data['unidade'] }
        entrys.append(entry)
        return entry, 201

class EntryList(Resource):
    def get(self):
      return {'competicoes': entrys}

class Competition(Resource):
    def get(self, name):
        for competition in competitions:
            if competition['competicao'] == name:
               return competition
        return{'competicao': None}, 404

    def post(self, name):
        data = request.get_json()
        competition = {'competicao': name, 'ranking':{}, 'isFinished': False, 'numTrys': data['numTrys'] }
        competitions.append(competition)
        return competition, 201

class CompetitionList(Resource):
    def get(self):
      return {'competicoes': competitions}

api.add_resource(Entry, '/entry/<string:name>')
api.add_resource(EntryList, '/entrys')
api.add_resource(Competition, '/competition/<string:name>')
api.add_resource(CompetitionList, '/competitions')

app.run(port=5006, debug=True)
