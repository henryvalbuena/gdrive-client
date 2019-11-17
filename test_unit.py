from unittest import TestCase

from db_interface import LogFiles
from models import TempFileSchema


class TestDB(TestCase):
    def setUp(self):
        self.log_files = LogFiles(TempFileSchema)

    def tearDown(self):
        self.log_files.drop(TempFileSchema.__tablename__)

    def test_table_creation(self):
        self.log_files.create_file(
            '1234',
            'test',
            100
        )
        q = self.log_files.get_file_by_id('1234')
        self.assertEqual('1234', q.fileid)

    def test_table_drop(self):
        self.assertTrue(self.log_files.drop(TempFileSchema.__tablename__))
