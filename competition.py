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