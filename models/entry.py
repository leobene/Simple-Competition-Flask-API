import sqlite3
from db import db

class EntryModel(db.Model):
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
      return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
    	db.session.delete(self)
    	db.session.commit()

