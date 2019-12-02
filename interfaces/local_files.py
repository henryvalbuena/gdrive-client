"""Local file interface module."""

import os


def get_file_names(path=None):
    """Return filename list.

    Args:
        path: optional - provide the path to scan for files

    Returns:
        List of file names from the current directory

    """
    return os.listdir(path)


def get_file_mod_date(filename):
    """Return unix timestamp of the file modified time.

    Args:
        filename: filename to which check for the creation time

    Returns:
        int representing the file's date unix timestamp

    """
    return os.path.getmtime(filename)


def get_file_size(filename):
    """Return file size in bytes.

    Args:
        filename: filename to which check for the creation time

    Returns:
        int representing the file's size in bytes

    """
    return os.path.getsize(filename)


def get_directories(path=None):
    """Return directories list.

    Args:
        path: optional - provide the path to scan for files

    Returns:
        List of directories names, empty if no directories are found

    """
    return [
        d
        for d in os.listdir(path)
        if '.' not in d
    ]


def get_dictionary_files(path=None):
    """Get a dictionary with filenames, sizes, and last modified timestamp.

    Args:
        path: optional - provide the path to scan for files

    Returns:
        Dictionary of file's filenames, sizes, and last modified timestamp

    """
    filenames = get_file_names(path)
    file_sizes = dict()

    for fname in filenames:
        file_sizes[fname] = [
            get_file_size(fname),
            get_file_mod_date(fname)
        ]
    return file_sizes
