from models.entry import EntryModel
from models.competition import CompetitionModel
from tests.base_test import BaseTest


class EntryTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            competition = CompetitionModel('test', False, 1)
            competition.save_to_db()
            entry = EntryModel('test', 19.99, 'm', 1)

            self.assertIsNone(EntryModel.find_by_name('test'), "Found an entry with name 'test' before save_to_db")

            self.assertEqual(EntryModel.find_athlete_tries(1, 'test'), 0, "The number of tries for the athelte 'test' before save_to_db was not 0")


            entry.save_to_db()

            self.assertIsNotNone(EntryModel.find_by_name('test'),
                                 "Did not find an entry with name 'test' after save_to_db")

            self.assertEqual(EntryModel.find_athlete_tries(1, 'test'), 1, "The number of tries for the athelte 'test' after save_to_db was not 1")

            entry.delete_from_db()

            self.assertIsNone(EntryModel.find_by_name('test'), "Found an entry with name 'test' after delete_from_db")

    def test_competition_relationship(self):
        with self.app_context():
            competition = CompetitionModel('test_competition', False, 1)
            entry = EntryModel('test', 19.99, 'm', 1)

            competition.save_to_db()
            entry.save_to_db()

            self.assertEqual(entry.competition.competicao, 'test_competition')
