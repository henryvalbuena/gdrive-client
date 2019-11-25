"""Test unit local files interface module."""

from unittest import TestCase

from interfaces.local_files import LocalFiles


class TestLF(TestCase):
    """Testing local file interface module."""

    def setUp(self):
        """Set up method."""
        self.lf = LocalFiles

    def test_get_file_list(self):
        """Test getting file list for the current directory."""
        files = self.lf.get_file_names()
        self.assertTrue(
            len(files) > 0
        )
