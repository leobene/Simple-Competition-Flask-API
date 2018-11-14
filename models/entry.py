from db import db
from models.competition import CompetitionModel

class EntryModel(db.Model):
    __tablename__ = 'entrys'

    id = db.Column(db.Integer, primary_key=True)
    atleta = db.Column(db.String(80))
    value = db.Column(db.Float(precision=2))
    unidade = db.Column(db.String(10))

    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'))
    competition = db.relationship('CompetitionModel')

    def __init__(self, atleta, value, unidade, competition_id):
        self.atleta = atleta
        self.value = value
        self.unidade = unidade
        self.competition_id = competition_id

    def json(self):
    	return {'atleta': self.atleta, 'value':self.value, 'unidade': self.unidade}

    @classmethod
    def find_by_name(cls, name):
      _competition_id = CompetitionModel.query.filter_by(competicao=name).first().id
      return cls.query.filter_by(competition_id=_competition_id).first()

    @classmethod
    def find_athelte_tries(cls, competition_id, athelte):
      return cls.query.filter_by(competition_id=competition_id, atleta=athelte).paginate().total

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
    	db.session.delete(self)
    	db.session.commit()

