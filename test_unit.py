"""Test unit module."""

from unittest import TestCase, skip

from db_interface import LogFiles

from models import FileSchema

from sqlalchemy.exc import IntegrityError


class TestDB(TestCase):
    """Testing Database."""

    DB = 'testing.db'
    file = {
        'fileid': '80',
        'filename': 'tests80.txt',
        'filesize': 12
    }
    files = [
        {
            'fileid': '78',
            'filename': 'tests78.txt',
            'filesize': 12
        },
        {
            'fileid': '33',
            'filename': 'test33.txt',
            'filesize': 11
        },
        {
            'fileid': '5',
            'filename': 'text5.txt',
            'filesize': 88
        }
    ]

    def setUp(self):
        """Set up method."""
        self.log_files = LogFiles(self.DB, FileSchema)
        self.log_files.create_table(FileSchema)

    def tearDown(self):
        """Tear down method."""
        self.log_files.drop_table(FileSchema.__tablename__)

    @skip('Pending correct implementation')
    def test_a_create_table(self):
        """Test creationg of table."""
        pass

    def test_b_table_drop(self):
        """Test the drop of a table."""
        self.assertTrue(self.log_files.drop_table(FileSchema.__tablename__))

    def test_create_file(self):
        """Test the creation of a file."""
        fid = self.file['fileid']

        self.log_files.create_file(**self.file)
        q = self.log_files.get_file_by_id(fid)

        self.assertEqual(fid, q.fileid)

    def test_remove_fileid(self):
        """Test the removal of a file by gdrive id."""
        fid = self.file['fileid']

        self.log_files.create_file(**self.file)
        q = self.log_files.get_file_by_id(fid)

        self.assertEqual(q.fileid, fid)

        self.log_files.remove_file_by_id(fid)
        q = self.log_files.get_file_by_id(fid)

        self.assertEqual(q, None)

    def test_create_multi_files(self):
        """Test the creationg of multiple files."""
        fid1 = self.files[0]['fileid']
        fid2 = self.files[1]['fileid']

        self.log_files.create_files(self.files)
        f1 = self.log_files.get_file_by_id(fid1)
        f2 = self.log_files.get_file_by_id(fid2)

        self.assertEqual(f1.fileid, fid1)
        self.assertEqual(f2.fileid, fid2)

    def test_get_all_files(self):
        """Test to get all files."""
        fid = self.files[0]['fileid']

        self.log_files.create_files(self.files)
        files = self.log_files.get_files()

        self.assertEqual(len(files), 3)
        self.assertEqual(fid, files[0].fileid)

    @skip('To be implemented')
    def test_failed_file_creation(self):
        """Test failed file creation."""
        pass

    def test_duplicated_file(self):
        """Test duplicated file."""
        self.log_files.create_file(**self.file)
        self.log_files.create_file(**self.file)

        self.assertRaises(IntegrityError)

    @skip('To be implemented')
    def test_failed_drop_table(self):
        """Test drop table for non existing table."""
        pass

    @skip('To be implemented')
    def test_create_multiple_tables(self):
        """Test create multiple tables."""
        pass
