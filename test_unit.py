"""Test unit module."""

from unittest import TestCase

from db_interface import LogFiles

from models import FileSchema

from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound


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
        try:
            self.log_files.drop_table(FileSchema.__tablename__)
        except OperationalError:
            pass  # No need to do anything here

    def test_create_duplicate_table(self):
        """Test duplicate table creation."""
        self.log_files.create_table(FileSchema)
        self.assertRaises(IntegrityError)

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

        self.assertRaises(
            NoResultFound,
            self.log_files.get_file_by_id,
            fid
        )

    def test_remove_non_existent_file(self):
        """Test for the removal of a non existent file."""
        self.assertRaises(
            NoResultFound,
            self.log_files.remove_file_by_id,
            'wrong'
        )

    def test_create_multi_files(self):
        """Test the creationg of multiple files."""
        fid1 = self.files[0]['fileid']
        fid2 = self.files[1]['fileid']

        self.log_files.create_files(self.files)
        f1 = self.log_files.get_file_by_id(fid1)
        f2 = self.log_files.get_file_by_id(fid2)

        self.assertEqual(f1.fileid, fid1)
        self.assertEqual(f2.fileid, fid2)

    def test_get_wrong_file(self):
        """Test for a file id that doesn't exist."""
        self.assertRaises(
            NoResultFound,
            self.log_files.get_file_by_id,
            'wrong'
        )

    def test_get_all_files(self):
        """Test to get all files."""
        fid = self.files[0]['fileid']

        self.log_files.create_files(self.files)
        files = self.log_files.get_files()

        self.assertEqual(len(files), 3)
        self.assertEqual(fid, files[0].fileid)

    def test_get_all_non_existing_files(self):
        """Test to get files with table empty."""
        files = self.log_files.get_files()

        self.assertEqual(len(files), 0)

    def test_duplicated_file(self):
        """Test duplicated file."""
        self.log_files.create_file(**self.file)

        self.assertRaises(
            IntegrityError,
            self.log_files.create_file,
            **self.file
        )

    def test_fail_create_file_no_table(self):
        """Test raise error when no table has been created."""
        self.log_files.drop_table(FileSchema.__tablename__)

        self.assertRaises(
            OperationalError,
            self.log_files.create_file,
            **self.file
        )

    def test_fail_create_multi_files_no_table(self):
        """Test raise error when no table has been created."""
        self.log_files.drop_table(FileSchema.__tablename__)

        self.assertRaises(
            OperationalError,
            self.log_files.create_files,
            self.files
        )

    def test_failed_drop_table_wrong_name(self):
        """Test drop table for non existing table."""
        self.assertFalse(
            self.log_files.drop_table('wrong')
        )

    def test_drop_table_if_db_empty(self):
        """Test drop table if the database is empty."""
        self.log_files.drop_table(FileSchema.__tablename__)

        self.assertRaises(
            OperationalError,
            self.log_files.drop_table,
            FileSchema.__tablename__
        )

    def test_update_existing_file(self):
        """Test file updates."""
        file = {
            'fileid': '80',
            'filename': 'updated',
            'filesize': 100
        }
        self.log_files.create_file(**self.file)
        self.log_files.update_file(self.file['fileid'], **file)
        ufile = self.log_files.get_file_by_id(file['fileid'])

        self.assertEqual(file['fileid'], ufile.fileid)
        self.assertEqual(file['filename'], ufile.filename)
        self.assertEqual(file['filesize'], ufile.filesize)

    def test_update_non_existing_file(self):
        """Test to update a file without table."""
        self.log_files.drop_table(FileSchema.__tablename__)

        self.assertRaises(
            OperationalError,
            self.log_files.update_file,
            self.file['fileid'],
            **self.file
        )

    def test_update_wrong_file(self):
        """Test to update a non-existing file."""
        self.log_files.create_file(**self.file)

        self.assertRaises(
            NoResultFound,
            self.log_files.update_file,
            'wrong',
            **self.file
        )
