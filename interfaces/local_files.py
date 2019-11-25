"""Local file interface module."""

import os


class LocalFiles:
    """Local file class."""

    @staticmethod
    def get_file_names():
        """Return filename list.

        Returns:
            List of file names from the current directory

        """
        return os.listdir()
