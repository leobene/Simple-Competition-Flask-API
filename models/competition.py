import sqlite3
from db import db

class CompetitionModel(db.Model):
  __tablename__ = 'competitions'

  id = db.Column(db.Integer, primary_key=True)
  competicao = db.Column(db.String(80))
  isFinished = db.Column(db.Boolean())
  numTrys = db.Column(db.Integer())

  entrys = db.relationship('EntryModel') #,lazy='dynamic')

  def __init__(self, competicao, isFinished, numTrys):
      self.competicao = competicao
      self.isFinished = isFinished
      self.numTrys = numTrys

  def json(self):
  	return {'competicao': self.competicao, 'isFinished':self.isFinished, 'numTrys': self.numTrys, 'entrys':[entry.json() for entry in self.entrys]} #.all()

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(competicao=name).first()

  @classmethod
  def find_competition_id(cls, name):
    return cls.query.filter_by(competicao=name).first().id

  @classmethod
  def find_all(cls):
    return cls.query.all()

  def save_to_db(self):
      db.session.add(self)
      db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()

