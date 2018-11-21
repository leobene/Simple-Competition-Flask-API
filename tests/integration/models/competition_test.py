from models.competition import CompetitionModel
from models.entry import EntryModel
from tests.base_test import BaseTest


class CompetitionTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            competition = CompetitionModel('test', False, 1)

            self.assertIsNone(CompetitionModel.find_by_name('test'), "Found an competition with name 'test' before save_to_db")

            competition.save_to_db()

            self.assertIsNotNone(CompetitionModel.find_by_name('test'),
                                 "Did not find a competition with name 'test' after save_to_db")

            competition.delete_from_db()

            self.assertIsNone(CompetitionModel.find_by_name('test'), "Found an competition with name 'test' after delete_from_db")

    def test_competition_relationship(self):
        with self.app_context():
            competition = CompetitionModel('test', False, 1)
            entry = EntryModel('test_entry', 19.99, 'm', 1)

            competition.save_to_db()
            entry.save_to_db()

            self.assertIsNotNone(competition.entrys[0])
            self.assertEqual(competition.entrys[0].atleta, 'test_entry')
