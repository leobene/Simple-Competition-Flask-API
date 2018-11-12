import sqlite3

class EntryModel(object):
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

      query = "SELECT * FROM entrys WHERE competicao=?"
      result = cursor.execute(query, (name,))
      row = result.fetchone()
      connection.close()

      if row:
        return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO entrys VALUES(?, ?, ?, ?)"
        cursor.execute(query, (self.competicao, self.atleta, self.value, self.unidade))

        connection.commit()

