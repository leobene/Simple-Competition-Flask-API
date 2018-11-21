from models.competition import CompetitionModel
from tests.base_test import BaseTest


class CompetitionTest(BaseTest):
    def test_create_competition(self):
        competition = CompetitionModel('test', False, 1)

        self.assertEqual(competition.competicao, 'test',
                         "The name of the competition after creation does not equal the constructor argument.")
        self.assertEqual(competition.isFinished, False,
                         "The boolean isFinished of the competition after creation does not equal the constructor argument.")
        self.assertEqual(competition.numTrys, 1,
                         "The number of tries of the competition after creation does not equal the constructor argument.")
        self.assertListEqual(competition.entrys, [],
                             "The competition's entries length was not 0 even though no entries were added.")

    def test_competition_json(self):
        competition = CompetitionModel('test', False, 1)
        expected = {
            'competicao': 'test',
            'isFinished': False,
            'numTrys': 1,
            'entrys':[]
        }

        self.assertEqual(
            competition.json(),
            expected,
            "The JSON export of the competition is incorrect. Received {}, expected {}.".format(competition.json(), expected))
