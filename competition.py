import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

class Competition(Resource):
    def get(self, name):
      competition = self.find_by_name(name)
      if competition:
        return competition
      return{'message': 'Competition not found'}, 404

    @classmethod
    def find_by_name(cls, name):
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "SELECT * FROM competitions WHERE competicao=?"
      result = cursor.execute(query, (name,))
      row = result.fetchone()
      connection.close()

      if row:
        return {'competicao': {'competicao': row[0], 'ranking': row[1], 'isFinished': row[2], 'numTrys': row[3]}}

    @classmethod
    def insert(cls, competition):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO competitions VALUES(?, ?, ?, ?)"
        cursor.execute(query, (competition['competicao'], competition['ranking'], competition['isFinished'], competition['numTrys']))

        connection.commit()


    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An competition with name '{}' already exists.".format(name)}

        #data = Entry.parser.parse_args()
        data = request.get_json()
        competition = {'competicao': name, 'ranking':0, 'isFinished': False, 'numTrys': data['numTrys'] }

        try:
            Competition.insert(competition)
        except:
            return {"message": "An error occurred inserting the competition."}, 500
        return competition, 200

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

    
    @classmethod
    def update(cls, competition):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE competitions SET isFinished=? WHERE competicao=?"
        cursor.execute(query, (competition['isFinished'], competition['competicao']))

        connection.commit()
        connection.close()

    #@jwt_required()
    def put(self, name):
        #data = Competition.parser.parse_args()
        data = request.get_json()
        competition = self.find_by_name(name)
        updated_competition = {'competicao': name, 'isFinished': data['isFinished'], 'ranking':0, 'numTrys': data['numTrys'] }
        if competition is None:
            try:
                Competition.insert(updated_competition)
            except:
                return {"message": "An error occurred inserting the competition."}
        else:
            try:
                Competition.update(updated_competition)
            except:
                raise
                return {"message": "An error occurred updating the competition."}
        return updated_competition

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