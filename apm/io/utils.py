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
