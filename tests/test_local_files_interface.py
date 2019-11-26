"""Test unit local files interface module."""

import os
from unittest import TestCase

from interfaces.local_files import LocalFiles


class TestLF(TestCase):
    """Testing local file interface module."""

    fname = 'README.md'

    def setUp(self):
        """Set up method."""
        self.lf = LocalFiles

    def test_get_file_list(self):
        """Test getting file list for the current directory."""
        files = len(self.lf.get_file_names())
        self.assertTrue(
            files > 0
        )

    def test_get_file_list_no_files(self):
        """Test getting file list from an empty directory."""
        files = len(self.lf.get_file_names('./db'))
        self.assertTrue(
            files == 1
        )

    def test_get_file_date(self):
        """Test getting file modified unix timestamp."""
        fdate = os.path.getmtime(self.fname)

        self.assertEqual(
            fdate,
            self.lf.get_file_mod_date(self.fname)
        )

    def test_get_file_date_worng_name(self):
        """Test getting a file date with a wrong filename."""
        self.assertRaises(
            FileNotFoundError,
            self.lf.get_file_mod_date,
            'wrong'
        )

    def test_get_file_size(self):
        """Test getting a file size."""
        fsize = os.path.getsize(self.fname)

        self.assertEqual(
            fsize,
            self.lf.get_file_size(self.fname)
        )

    def test_get_file_size_wrong_name(self):
        """Test getting file size with a wrong filename."""
        self.assertRaises(
            FileNotFoundError,
            self.lf.get_file_size,
            'wrong'
        )
