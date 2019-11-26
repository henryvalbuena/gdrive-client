"""Local file interface module."""

import os


class LocalFiles:
    """Local file class."""

    @staticmethod
    def get_file_names(directory=None):
        """Return filename list.

        Returns:
            List of file names from the current directory

        """
        return os.listdir(directory)

    @staticmethod
    def get_file_mod_date(filename):
        """Return unix timestamp of the file modified time.

        Args:
            filename: filename to which check for the creation time
        Returns:
            int representing the file's date unix timestamp

        """
        return os.path.getmtime(filename)

    @staticmethod
    def get_file_size(filename):
        """Return file size in bytes.

        Args:
            filename: filename to which check for the creation time
        Returns:
            int representing the file's size in bytes

        """
        return os.path.getsize(filename)
