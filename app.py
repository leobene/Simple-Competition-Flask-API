from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'EV'
api = Api(app)

jwt = JWT(app, authenticate, identity)

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
    @jwt_required()
    def get(self, name):
        for entry in entrys:
            if entry['competicao'] == name:
               return entry
        return{'competicao': None}, 404

    def post(self, name):
        data = request.get_json()
        entry = {'competicao': name, 'atleta':data['atleta'], 'value': data['value'], 'unidade': data['unidade'] }
        entrys.append(entry)
        global competitions
        #add the new entry to its respective competition if the competition exists
        for competition in competitions:
            if competition['competicao'] == name:
              ranking = competition['ranking'].copy()
              ranking.update(entry)
              comp = {'competicao': competition['competicao'], 'ranking':ranking, 'isFinished': competition['isFinished'], 'numTrys': competition['numTrys'] }
              competition.update(comp)
              return entry, 201
        return{'competicao': None}, 404 #else competition not found

class EntryList(Resource):
    def get(self):
      return {'entradas': entrys}

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

class Finish(Resource):
    def get(self, name):
        for competition in competitions:
            if competition['competicao'] == name:
               return competition['isFinished']
        return{'competicao': None}, 404

    def post(self, name):
        for competition in competitions:
            if competition['competicao'] == name:
               comp = {'competicao': competition['competicao'], 'ranking':competition['ranking'], 'isFinished': True, 'numTrys': competition['numTrys'] }
               competition.update(comp)
               return competition, 201
        return{'competicao': None}, 404

api.add_resource(Entry, '/entry/<string:name>')
api.add_resource(EntryList, '/entrys')
api.add_resource(Competition, '/competition/<string:name>')
api.add_resource(CompetitionList, '/competitions')
api.add_resource(Finish, '/finish/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5006, debug=True)
