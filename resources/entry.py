import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from models.entry import EntryModel

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
        if EntryModel.find_by_name(name): #ToDo se number of tries in the competition
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Entry.parser.parse_args()
        entry = EntryModel(name, data['atleta'], data['value'], data['unidade'])

        try:
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the entry."}, 500

        #add the new entry to its respective competition if the competition exists
        #for competition in competitions:
         #   if competition['competicao'] == name:
              #competition.update(comp)
              #return entry, 201
        #return{'competicao': None}, 404 #else competition not found

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
      
