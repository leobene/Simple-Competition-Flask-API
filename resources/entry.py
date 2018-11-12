import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from models.entry import EntryModel

class Entry(Resource):
    @jwt_required()
    def get(self, name):
      entry = EntryModel.find_by_name(name)
      if entry:
        return entry.json()
      return{'message': 'Entry not found'}, 404

    def post(self, name):
        if EntryModel.find_by_name(name): #ToDo se number of tries in the competition
            return {'message': "An item with name '{}' already exists.".format(name)}

        #data = Entry.parser.parse_args()
        data = request.get_json()

        entry = EntryModel(name, data['atleta'], data['value'], data['unidade'])

        try:
            entry.insert()
        except:
            return {"message": "An error occurred inserting the entry."}, 500

        #add the new entry to its respective competition if the competition exists
        #for competition in competitions:
         #   if competition['competicao'] == name:
              #competition.update(comp)
              #return entry, 201
        #return{'competicao': None}, 404 #else competition not found

        return entry.json(), 200

    #@jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM entrys WHERE competicao=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Entry deleted'}, 404

class EntryList(Resource):   
    def get(self):
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "SELECT * FROM competitions"
      result = cursor.execute(query)
      entrys = []
      for row in result:
        entrys.append({'competicao': row[0], 'atleta': row[1], 'value':row[2], 'unidade': row[3] })

      connection.close()
      return {'entradas': entrys}
      
