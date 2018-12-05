import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from models.competition import CompetitionModel
from models.entry import EntryModel

class Competition(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('isFinished',
        type=bool,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('numTrys',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
      competition = CompetitionModel.find_by_name(name)
      if competition:
        return competition.json()
      return{'message': 'Competition not found'}, 404

    def post(self, name):
        if CompetitionModel.find_by_name(name):
            return {'message': "An competition with name '{}' already exists.".format(name)}, 500

        data = Competition.parser.parse_args()
        competition = CompetitionModel(name, 0, data['numTrys'])

        try:
            competition.save_to_db()
        except:
            return {"message": "An error occurred inserting the competition."}, 500

        return competition.json(), 201

    #@jwt_required()
    def delete(self, name):
        competition = CompetitionModel.find_by_name(name)
        if competition:
            competition.delete_from_db()

        return {'message': 'Competition deleted'}, 200

    #@jwt_required()
    def put(self, name):
        data = Competition.parser.parse_args()
        competition = CompetitionModel.find_by_name(name)

        if competition:
            competition.name = name
            competition.isFinished = data['isFinished']
            competition.numTrys = data['numTrys']
        else:
            competition = CompetitionModel(name, data['isFinished'], data['numTrys'])

        competition.save_to_db()

        return competition.json()

class CompetitionList(Resource):
    def get(self):
        return {'competitions': [competition.json() for competition in CompetitionModel.find_all()]}

class Finish(Resource):
    def get(self, name):
        competition = CompetitionModel.find_by_name(name)
        if competition:
            competition_id = CompetitionModel.find_competition_id(name)
            if competition.competicao.find("ardo") != -1:
                #same as
                #query = "SELECT atleta FROM entrys WHERE competition_id=? ORDER BY value desc"
                return [entry.json() for entry in EntryModel.query.filter_by(competition_id=competition_id).order_by(EntryModel.value.desc())]
            else:
                #query = "SELECT atleta FROM entrys WHERE competition_id=? ORDER BY value asc"
                return [entry.json() for entry in EntryModel.query.filter_by(competition_id=competition_id).order_by('value')]
        
        return{'message': 'Competition not found'}, 404

    def post(self, name):
        competition = CompetitionModel.find_by_name(name)

        if competition is None:
            return{'message': 'Competition not found'}, 404
        else:
            competition.isFinished = True

        competition.save_to_db()

        return competition.json(), 200