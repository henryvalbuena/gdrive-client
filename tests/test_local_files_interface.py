"""Test unit local files interface module."""

import os
from unittest import TestCase

from interfaces.local_files import get_dictionary_files, get_directories
from interfaces.local_files import get_file_mod_date, get_file_names, \
    get_file_size


class TestLF(TestCase):
    """Testing local file interface module."""

    fname = 'README.md'

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        cls.temp_path = 'test_dir'
        os.mkdir(cls.temp_path)

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        os.rmdir(cls.temp_path)

    def test_get_file_list(self):
        """Test getting file list for the current directory."""
        files = len(get_file_names())

        self.assertTrue(
            files > 0
        )

    def test_get_file_list_no_files(self):
        """Test getting file list from an empty directory."""
        files = len(get_file_names(self.temp_path))

        self.assertTrue(files == 0)

    def test_get_file_date(self):
        """Test getting file modified unix timestamp."""
        fdate = os.path.getmtime(self.fname)

        self.assertEqual(
            fdate,
            get_file_mod_date(self.fname)
        )

    def test_get_file_date_wrong_name(self):
        """Test getting a file date with a wrong filename."""
        self.assertRaises(
            FileNotFoundError,
            get_file_mod_date,
            'wrong'
        )

    def test_get_file_size(self):
        """Test getting a file size."""
        fsize = os.path.getsize(self.fname)

        self.assertEqual(
            fsize,
            get_file_size(self.fname)
        )

    def test_get_file_size_wrong_name(self):
        """Test getting file size with a wrong filename."""
        self.assertRaises(
            FileNotFoundError,
            get_file_size,
            'wrong'
        )

    def test_get_directories(self):
        """Test getting directories only."""
        dirs = len(get_directories())

        self.assertTrue(dirs > 0)

    def test_getting_non_existing_directories(self):
        """Test getting directories from an empty directory."""
        dirs = len(get_directories(self.temp_path))

        self.assertTrue(dirs == 0)

    def test_get_files_details_dictionary(self):
        """Test getting details for all files."""
        deets = get_dictionary_files()

        self.assertIn('tests', deets)

    def test_getting_files_details_empty_directory(self):
        """Test getting files details from an empty directory."""
        deets = get_dictionary_files(self.temp_path)

        self.assertNotIn('tests', deets)
