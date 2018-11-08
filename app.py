from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, current_identity
from security import authenticate, identity
from user import UserRegister
from entry import Entry, EntryList
from competition import Competition, CompetitionList, Finish

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

api.add_resource(Entry, '/entry/<string:name>')
api.add_resource(EntryList, '/entrys')
api.add_resource(Competition, '/competition/<string:name>')
api.add_resource(CompetitionList, '/competitions')
api.add_resource(Finish, '/finish/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
  app.run(port=5006, debug=True)
