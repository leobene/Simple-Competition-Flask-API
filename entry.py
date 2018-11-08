import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

class Entry(Resource):
    @jwt_required()
    def get(self, name):
      entry = self.find_by_name(name)
      if entry:
        return entry
      return{'message': 'Entry not found'}, 404

    @classmethod
    def find_by_name(cls, name):
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "SELECT * FROM entrys WHERE competicao=?"
      result = cursor.execute(query, (name,))
      row = result.fetchone()
      connection.close()

      if row:
        return {'entry': {'competicao': row[0], 'atleta': row[1], 'value': row[2], 'unidade': row[3]}}

    def post(self, name):
        data = request.get_json()
        entry = {'competicao': name, 'atleta':data['atleta'], 'value': data['value'], 'unidade': data['unidade'] }
        entrys.append(entry)
        global competitions
        #add the new entry to its respective competition if the competition exists
        for competition in competitions:
            if competition['competicao'] == name:
              #ranking = competition['ranking'].copy()
              #ranking.update(entry)
              print("competition['ranking']")
              print(competition['ranking'])
              print("entry")
              print(entry)
              ranking = competition['ranking'].copy()
              ranking.update(entry)
              print("ranking")
              print(dict(list(competition['ranking'].items()) + list(entry.items())))
              comp = {'competicao': competition['competicao'], 'ranking':ranking, 'isFinished': competition['isFinished'], 'numTrys': competition['numTrys'] }
              competition.update(comp)
              print("competition.update(")
              print(competition)
              return entry, 201
        return{'competicao': None}, 404 #else competition not found

class EntryList(Resource):
    def get(self):
      return {'entradas': entrys}