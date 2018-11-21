from models.entry import EntryModel
from tests.base_test import BaseTest


class EntryTest(BaseTest):
    def test_create_entry(self):
        entry = EntryModel('test', 19.99, 'm', 1)

        self.assertEqual(entry.atleta, 'test',
                         "The name of the atlhete after creation does not equal the constructor argument.")
        self.assertEqual(entry.value, 19.99,
                         "The value of the entry after creation does not equal the constructor argument.")
        self.assertEqual(entry.unidade, 'm',
                         "The unit of the entry after creation does not equal the constructor argument.")
        self.assertEqual(entry.competition_id, 1,
                         "The competition_id of the entry after creation does not equal the constructor argument.")
        self.assertIsNone(entry.competition, "The entry's competition was not None even though the store was not created.")

    def test_entry_json(self):
        entry = EntryModel('test', 19.99, 'm', 1)
        expected = {
            'atleta': 'test',
            'value': 19.99,
            'unidade': 'm'
        }

        self.assertEqual(
            entry.json(),
            expected,
            "The JSON export of the entry is incorrect. Received {}, expected {}.".format(entry.json(), expected))
