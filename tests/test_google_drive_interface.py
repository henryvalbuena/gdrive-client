"""Test Google Drive interface module."""

from unittest import TestCase

from interfaces.google_drive_class import GDRIVE


class TESTGDRIVE(TestCase):
    """Test suit for Google Drive interface."""

    def setUp(self):
        """Set up method."""
        self.SERVICE = GDRIVE()

    def test_list_files_from_gdrive(self):
        """Test querying files from gdrive."""
        files = self.SERVICE.list_drive_files()

        self.assertTrue(len(files) > 0)
        self.assertIn('name', files[0])

    def test_create_new_file(self):
        """Test creating a temporary file."""
        file = self.SERVICE.create_new_file(
            filename='test1.txt',
            parents=['1uabjn86Q9z-jU_v69XUHCf8Md3A9Bpqd']
        )

        self.assertIn('id', file)

        self.SERVICE.delete_file(fileId=file['id'])
