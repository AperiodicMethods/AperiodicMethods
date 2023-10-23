"""Utilities for I/O."""

from pathlib import Path

###################################################################################################
###################################################################################################

def clean_files(files):
    """Clean a list of files, removing any hidden files."""

    return list(filter(lambda x: x[0] != '.', files))


def check_folder(file_name, folder):
    """Check and extract a file path.

    Parameters
    ----------
    file_name : str or Path or None
        File name or path.
    folder : str or Path or None
        Folder name or path.

    Returns
    -------
    file_path : Path
        Full file path for the desired folder.
    """

    if isinstance(folder, (str, Path)):
        file_path = Path(folder) / file_name
    elif folder is None:
        file_path = file_name

    return file_path


def check_ext(file_name, extension):
    """"Check a file name for a given extension, and add if missing.

    Parameters
    ----------
    file_name : str
        File name to check.
    extension : str
        Extension to check / add to file name.

    Returns
    -------
    file_name : str
        File name, checked and updated for the extension.
    """

    if not extension[0] == '.':
        extension = '.' + extension

    if isinstance(file_name, str):
        if not file_name.split('.')[-1] == extension[1:]:
            file_name = file_name + extension
    elif isinstance(file_name, Path):
        file_name = file_name.with_suffix(extension)

    return file_name
