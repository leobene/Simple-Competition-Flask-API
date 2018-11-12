import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from models.competition import CompetitionModel

class Competition(Resource):
    def get(self, name):
      competition = CompetitionModel.find_by_name(name)
      if competition:
        return competition.json()
      return{'message': 'Competition not found'}, 404

    def post(self, name):
        if CompetitionModel.find_by_name(name):
            return {'message': "An competition with name '{}' already exists.".format(name)}

        #data = Entry.parser.parse_args()
        data = request.get_json()
        competition = CompetitionModel(name, 0, False, data['numTrys'])

        try:
            competition.insert()
        except:
            return {"message": "An error occurred inserting the competition."}, 500
            
        return competition.json(), 200

    #@jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM competitions WHERE competicao=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        #ToDo: Delete all entries from that competition

        return {'message': 'Competition deleted'}, 404

    #@jwt_required()
    def put(self, name):
        #data = Competition.parser.parse_args()
        data = request.get_json()
        competition = CompetitionModel.find_by_name(name)
        updated_competition = CompetitionModel(name, data['isFinished'], 0, data['numTrys'])
        if competition is None:
            try:
                updated_competition.insert()
            except:
                return {"message": "An error occurred inserting the competition."}
        else:
            try:
                updated_competition.update()
            except:
                raise
                return {"message": "An error occurred updating the competition."}
        return updated_competition.json()

class CompetitionList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM competitions"
        result = cursor.execute(query)
        competitions = []
        for row in result:
            competitions.append({'competicao': row[0], 'isFinished': row[1], 'ranking':row[2], 'numTrys': row[3] })
        connection.close()

        return {'competitions': competitions}

class Finish(Resource):
    def get(self, name):
        competition = CompetitionModel.find_by_name(name)
        if competition:
            return competition.json()
        #ToDo retornar o isFinished
        return{'message': 'Competition not found'}, 404

    def post(self, name):
        data = request.get_json()
        competition = CompetitionModel.find_by_name(name)
        if competition is None:
            return{'message': 'Competition not found'}, 404
        else:
            try:
                updated_competition = CompetitionModel(name, data['isFinished'], 0, data['numTrys'])
                updated_competition.update()
            except:
                raise
                return {"message": "An error occurred finishing the competition."}
        return updated_competition.json(), 201
