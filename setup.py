"""AperiodicMethods setup script."""

import os
from setuptools import setup, find_packages


# Load the required dependencies from the requirements file
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name = 'AperiodicMethods',
    python_requires = '>=3.5',
    author = 'The Voytek Lab',
    author_email = 'voyteklab@gmail.com',
    maintainer = 'Thomas Donoghue',
    maintainer_email = 'tdonoghue.research@gmail.com',
    packages = find_packages(),
    license = 'Apache License, 2.0',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    platforms = 'any',
    install_requires = install_requires,
    tests_require = ['pytest'],
)
