from models.entry import EntryModel
from models.competition import CompetitionModel
from tests.base_test import BaseTest
import json


class CompetitionTest(BaseTest):
    def test_competition_not_found(self):
        with self.app() as c:
            r = c.get('/competition/test')
            self.assertEqual(r.status_code, 404)

    def test_competition_found(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.get('/competition/100m')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'competicao': '100m', 'entrys': [], 'isFinished': False, 'numTrys': 1},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_competition_with_entries_found(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                EntryModel('Bolt', 9.59, 's', 1).save_to_db()
                r = c.get('/competition/100m')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'competicao': '100m',
                    'entrys': [{'atleta': 'Bolt', 'unidade': 's', 'value': 9.59}],
                    'isFinished': False,
                    'numTrys': 1},
                    d2=json.loads(r.data.decode('utf-8')))


    def test_delete_competition(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.delete('/competition/100m')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'message': 'Competition deleted'},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_create_competition(self):
        with self.app() as c:
            with self.app_context():
                r = c.post('/competition/test', data={'isFinished': False, 'numTrys': 1})

                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(CompetitionModel.find_by_name('test'))
                self.assertDictEqual(d1={'competicao': 'test', 'entrys': [], 'isFinished': False, 'numTrys': 1},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_create_duplicate_competition(self):
        with self.app() as c:
            with self.app_context():
                c.post('/competition/test', data={'isFinished': False, 'numTrys': 1})
                r = c.post('/competition/test', data={'isFinished': False, 'numTrys': 1})

                self.assertEqual(r.status_code, 500)
                self.assertDictEqual(d1={'message': "An competition with name '{}' already exists.".format('test')},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_put_competition(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.put('/competition/100m', data={'isFinished': False, 'numTrys': 2})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(CompetitionModel.find_by_name('100m').numTrys, 2)
                self.assertDictEqual(d1={'competicao': '100m', 'entrys': [], 'isFinished': True, 'numTrys': 2},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_put_update_competition(self):
        with self.app() as c:
            with self.app_context():
                c.put('/competition/100m', data={'isFinished': False, 'numTrys': 1})
                r = c.put('/competition/100m', data={'isFinished': False, 'numTrys': 2})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(CompetitionModel.find_by_name('100m').numTrys, 2)

    def test_competition_list(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.get('/competitions')

                self.assertDictEqual(d1={'competitions': [{'competicao': '100m', 'entrys': [], 'isFinished': False, 'numTrys': 1}]},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_competition_with_entries_list(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                EntryModel('Bolt', 9.59, 's', 1).save_to_db()
                r = c.get('/competitions')

                self.assertDictEqual(d1={'competitions': [{'competicao': '100m',
                                    'entrys': [{'atleta': 'Bolt','unidade': 's','value': 9.59}],
                                    'isFinished': False,
                                    'numTrys': 1}]},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_get_competition_ranking(self):
        pass

    def test_set_competition_isFinished(self):
        pass
