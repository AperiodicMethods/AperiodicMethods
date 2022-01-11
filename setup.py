"""Setup script to install `apm`."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('apm', 'version.py')) as version_file:
    exec(version_file.read())

# Load the required dependencies from the requirements file
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name = 'AperiodicMethods',
    version = __version__,
    description = 'Aperiodic methods helper module.',
    python_requires = '>=3.6',
    maintainer = 'Thomas Donoghue',
    maintainer_email = 'tdonoghue.research@gmail.com',
    packages = find_packages(),
    license = 'MIT License',
    classifiers = [
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    platforms = 'any',
    install_requires = install_requires,
    tests_require = ['pytest'],
)