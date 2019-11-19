"""Test unit module."""

from unittest import TestCase

from db_interface import LogFiles

from models import FileSchema


class TestDB(TestCase):
    """Testing Database."""

    DB = 'testing.db'

    @classmethod
    def setUpClass(cls):
        """Set up method."""
        cls.log_files = LogFiles(cls.DB, FileSchema)

    @classmethod
    def tearDownClass(cls):
        """Tear down method."""
        cls.log_files.drop_table(FileSchema.__tablename__)

    def test_a_create_table(self):
        """Test creationg of table."""
        self.log_files.create_table(FileSchema)
        self.assertTrue(True)

    def test_b_table_drop(self):
        """Test the drop of a table."""
        self.assertTrue(self.log_files.drop_table(FileSchema.__tablename__))
        self.log_files.create_table(FileSchema)

    def test_create_file(self):
        """Test the creation of a file."""
        self.log_files.create_file(
            'test',
            'test',
            50
        )
        q = self.log_files.get_file_by_id('test')
        self.assertEqual('test', q.fileid)

    def test_remove_fileid(self):
        """Test the removal of a file by gdrive id."""
        self.log_files.create_file(
            '123',
            'test',
            22
        )
        q = self.log_files.get_file_by_id('123')
        self.assertEqual(q.fileid, '123')

        self.log_files.remove_file_by_id('123')
        q = self.log_files.get_file_by_id('123')
        self.assertEqual(q, None)

    def test_create_multi_files(self):
        """Test the creationg of multiple files."""
        self.log_files.create_files(
            [
                {
                    'fileid': '78',
                    'filename': 'tests.txt',
                    'filesize': 12
                },
                {
                    'fileid': '21',
                    'filename': 'test_a.txt',
                    'filesize': 11
                }
            ]
        )
        f1 = self.log_files.get_file_by_id('78')
        f2 = self.log_files.get_file_by_id('21')

        self.assertEqual(f1.fileid, '78')
        self.assertEqual(f2.fileid, '21')

    def test_get_all_files(self):
        """Test to get all files."""
        self.log_files.create_files(
            [
                {
                    'fileid': '78',
                    'filename': 'tests.txt',
                    'filesize': 12
                },
                {
                    'fileid': '21',
                    'filename': 'test_a.txt',
                    'filesize': 11
                },
                {
                    'fileid': '5',
                    'filename': 'text.txt',
                    'filesize': 88
                }
            ]
        )
        files = self.log_files.get_files()
        self.assertEqual(len(files), 3)
        self.assertEqual('78', files[1].fileid)

        def test_failed_file_creationg(self):
            """Test failed file creation."""
            pass

        def test_duplicated_file(self):
            """Test duplicated file."""
            pass

        def test_failed_drop_table(self):
            """Test drop table for non existing table."""
            pass

        def test_create_multiple_tables(self):
            """Test create multiple tables."""
            pass
