from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from models.entry import EntryModel
from models.competition import CompetitionModel

class Entry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('atleta',
        type=str,
        required=True,
        help="This field cannot be left blank!"
      )
    parser.add_argument('value',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('unidade',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
      entry = EntryModel.find_by_name(name)
      if entry:
        return entry.json()
      return{'message': 'Entry not found'}, 404

    def post(self, name):
        _entry = EntryModel.find_by_name(name)
        competition = CompetitionModel.find_by_name(name)
        if competition:
          if competition.isFinished:
            return {'message': "The competition '{}' is Finished! Can not accept more entries!".format(name)}

          competition_num_tries = competition.numTrys
        else:
          return {'message': "The competition '{}' doesen't exists.".format(name)}

        data = Entry.parser.parse_args()
        competition_id = CompetitionModel.find_competition_id(name)
        print(competition_id)
        athlete_num_tries = EntryModel.find_athlete_tries(competition_id, data['atleta'])
        
        if _entry and athlete_num_tries and athlete_num_tries > competition_num_tries:
            return {'message': "{} has reached the maximum number of attempts in {} competition.".format(data['atleta'], name)}

        competition = CompetitionModel.find_by_name(name)
        entry = EntryModel(data['atleta'], data['value'], data['unidade'], competition.id)

        try:
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the entry."}, 500

        return entry.json(), 201

    #@jwt_required()
    def delete(self, name):
        item = EntryModel.find_by_name(name)
        if item:
          item.delete_from_db()

        return {'message': 'Entry deleted'}, 404

class EntryList(Resource):   
    def get(self):
      return {'entradas': [entry.json() for entry in EntryModel.query.all()]}
      
