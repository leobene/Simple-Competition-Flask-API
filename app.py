from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, current_identity
from security import authenticate, identity
from resources.user import UserRegister
from resources.entry import Entry, EntryList
from resources.competition import Competition, CompetitionList, Finish

app = Flask(__name__)
app.secret_key = 'EV'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Entry, '/entry/<string:name>')
api.add_resource(EntryList, '/entrys')
api.add_resource(Competition, '/competition/<string:name>')
api.add_resource(CompetitionList, '/competitions')
api.add_resource(Finish, '/finish/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5006, debug=True)
