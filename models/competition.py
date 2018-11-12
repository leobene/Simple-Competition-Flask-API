import sqlite3

class CompetitionModel(object):
    def __init__(self, competicao, ranking, isFinished, numTrys):
        self.competicao = competicao
        self.ranking = ranking
        self.isFinished = isFinished
        self.numTrys = numTrys

    def json(self):
    	return {'competicao': self.competicao, 'ranking': self.ranking, 'isFinished':self.isFinished, 'numTrys': self.numTrys}

    @classmethod
    def find_by_name(cls, name):
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "SELECT * FROM competitions WHERE competicao=?"
      result = cursor.execute(query, (name,))
      row = result.fetchone()
      connection.close()

      if row:
        return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO competitions VALUES(?, ?, ?, ?)"
        cursor.execute(query, (self.competicao, self.ranking, self.isFinished, self.numTrys))

        connection.commit()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE competitions SET isFinished=? WHERE competicao=?"
        cursor.execute(query, (self.isFinished, self.competicao))

        connection.commit()
        connection.close()

