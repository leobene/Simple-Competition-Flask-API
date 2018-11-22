from models.user import UserModel
from models.entry import EntryModel
from models.competition import CompetitionModel
from tests.base_test import BaseTest
import json


class EntryTest(BaseTest):
    def setUp(self):
        super(EntryTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                self.auth_header = "JWT {}".format(json.loads(auth_request.data.decode('utf-8'))['access_token'])

    def test_entry_no_auth(self):
        with self.app() as c:
            r = c.get('/entry/test')
            self.assertEqual(r.status_code, 401)

    def test_entry_not_found(self):
        with self.app() as c:
            r = c.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(r.status_code, 404)

    def test_entry_found(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                EntryModel('Usain Bolt', 9.59, 's', 1).save_to_db()
                r = c.get('/entry/100m', headers={'Authorization': self.auth_header})

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'atleta': 'Usain Bolt', 'unidade': 's', 'value': 9.59},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_delete_entry(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                EntryModel('Bolt', 9.59, 's', 1).save_to_db()
                r = c.delete('/entry/100m')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'message': 'Entry deleted'},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_create_entry(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.post('/entry/100m', data={'atleta': 'Bolt', 'unidade': 's', 'value': 9.59})

                self.assertEqual(r.status_code, 201)
                #self.assertEqual(EntryModel.find_by_name('Bolt').atleta, 9.59)
                self.assertDictEqual(d1={'atleta': 'Bolt', 'unidade': 's', 'value': 9.59},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_create_another_entry_in_the_same_competition(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 2).save_to_db()
                c.post('/entry/100m', data={'atleta': 'Bolt', 'unidade': 's', 'value': 9.59})
                r = c.post('/entry/100m', data={'atleta': 'Bolt', 'unidade': 's', 'value': 9.29})

                self.assertEqual(r.status_code, 201)

    def test_create_another_entry_but_exceeds_number_of_tries(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                c.post('/entry/100m', data={'atleta': 'Bolt', 'unidade': 's', 'value': 9.59})
                r = c.post('/entry/100m', data={'atleta': 'Bolt', 'unidade': 's', 'value': 9.29})

                self.assertDictEqual(d1={'message': "{} has reached the maximum number of attempts in {} competition.".format('Bolt', '100m')},
                                     d2=json.loads(r.data.decode('utf-8')))
                self.assertEqual(r.status_code, 500)


    def test_entry_list(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                r = c.get('/entrys')

                self.assertDictEqual(d1={'entradas': []},
                                     d2=json.loads(r.data.decode('utf-8')))

    def test_entry_list_with_entry(self):
        with self.app() as c:
            with self.app_context():
                CompetitionModel('100m', False, 1).save_to_db()
                EntryModel('Bolt', 9.59, 's', 1).save_to_db()
                r = c.get('/entrys')

                self.assertDictEqual(d1={'entradas': [{'atleta': 'Bolt', 'unidade': 's', 'value': 9.59}]},
                                     d2=json.loads(r.data.decode('utf-8')))
