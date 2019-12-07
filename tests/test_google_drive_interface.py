"""Test Google Drive interface module."""

from unittest import TestCase

from interfaces.google_drive_class import GDRIVE


class TESTGDRIVE(TestCase):
    """Test suit for Google Drive interface."""

    temp_file = 'test1.txt'
    parent = '1uabjn86Q9z-jU_v69XUHCf8Md3A9Bpqd'

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
            filename=self.temp_file,
            parents=[self.parent]
        )

        self.assertIn('id', file)

        self.SERVICE.delete_file(fileId=file['id'])

    def test_delete_file(self):
        """Test deleting a temporary file."""
        file = self.SERVICE.create_new_file(
            filename=self.temp_file,
            parents=[self.parent]
        )

        self.assertIn('id', file)
        self.SERVICE.delete_file(fileId=file['id'])

        files = self.SERVICE.list_drive_files()

        exists = [
            file['id'] == f['id']
            for f in files
        ]

        self.assertNotIn(True, exists)

    def test_update_file(self):
        """Test uploading a file."""
        files = self.SERVICE.list_drive_files()
        print(files)
        dir4 = [f for f in files if f['name'] == 'dir4'][0]
        file = self.SERVICE.create_new_file('update.txt', parents=[dir4['id']])

        update = self.SERVICE.update_file({
            'fileId': file['id'],
            'media': 'gdrive_test/file1.txt',
            'name': 'file1.txt'
        })
        # Delete file from GDRIVE
        self.SERVICE.delete_file(file['id'])

        self.assertIn('id', update)
        self.assertTrue(update['name'], 'file1.txt')
