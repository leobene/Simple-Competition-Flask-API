import sqlite3
from db import db

class EntryModel(object):
    __tablename__ = 'entrys'

    id = db.Column(db.Integer, primary_key=True)
    competicao = db.Column(db.String(80))
    atleta = db.Column(db.String(80))
    value = db.Column(db.Float(precision=2))
    unidade = db.Column(db.String(10))

    def __init__(self, competicao, atleta, value, unidade):
        self.competicao = competicao
        self.atleta = atleta
        self.value = value
        self.unidade = unidade

    def json(self):
    	return {'competicao': self.competicao, 'atleta': self.atleta, 'value':self.value, 'unidade': self.unidade}

    @classmethod
    def find_by_name(cls, name):
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()
      print(name)
      query = "SELECT * FROM entrys WHERE competicao=?"
      result = cursor.execute(query, (name,))
      row = result.fetchone()
      connection.close()

      print(row)
      if row:
        return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO entrys VALUES(?, ?, ?, ?)"
        cursor.execute(query, (self.competicao, self.atleta, self.value, self.unidade))

        connection.commit()

