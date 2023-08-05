# Copyright 2019 School of Physics & Astronomy, Monash University
#
# This file is part of monashspa.
#
# monashspa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monashspa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monashspa.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages

# Define the current version of the library
# Update this before building and publishing a new version
# see https://semver.org/ for guidelines on how to modify the version string
VERSION = '1.6.1'
# version information generated by our GitHub Action (see .github/workflows/release.yml)
CURRENT_TAG = os.environ.get('GHA_TAG_VERSION')
CURRENT_GIT_COMMIT_HASH = os.environ.get('GHA_GIT_COMMIT')
if CURRENT_TAG is not None:
    print('GitHub Action debug: tag=', CURRENT_TAG)
if CURRENT_GIT_COMMIT_HASH is not None:
    print('GitHub Action debug: git hash=', CURRENT_GIT_COMMIT_HASH)
# Modify the current version if we are building inside our GitHub action
if CURRENT_TAG is not None and CURRENT_TAG and CURRENT_TAG != 'refs/heads/master':
    VERSION = CURRENT_TAG
elif CURRENT_GIT_COMMIT_HASH:
    index = 0
    try:
        import requests
        response = requests.get('https://test.pypi.org/pypi/monashspa/json', timeout=2)
        data = response.json()
        if response.status_code == 200:
            found = True
            while found:
                # PyPI converts '-' to '.' in version
                if '{version}.dev{index}'.format(version=VERSION, index=index) not in data['releases']:
                    break
                else:
                    index += 1
        else:
            print('GitHub Action debug: Error while getting JSON data from test PyPI. Status code was:', response.status_code)
    except BaseException:
        print('GitHub Action debug: Error while querying PyPI release information. Will guess -dev0 is the correct postfix.')
        pass

    # Despite PyPI converting '-' to '.', we want to use '-' in __version__.py as it matches semver specs.
    VERSION += '-dev{}'.format(index)

# get directory of setup.py and the rest of the code for the library
code_dir = os.path.abspath(os.path.dirname(__file__))

# Auto generate a __version__ file for the package to import
with open(os.path.join(code_dir, 'monashspa', '__version__.py'), 'w') as f:
    f.write("__version__ = '%s'\n" % VERSION)

# Work around the fact that the readme.md file doesn't exist for users installing
# from the tar.gz format. However, in this case, they won't be uploading to PyPi
# so they don't need it!
try:
    # Read in the readme file as the long description
    with open(os.path.join(code_dir, 'readme.md')) as f:
        long_description = f.read()
except Exception:
    long_description = ""

setup(
    name='monashspa',
    version=VERSION,
    description='Library of useful data analysis tools for Monash University Physics & Astronomy students',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://monashspa.readthedocs.io',
    project_urls={
        "Documentation": "https://monashspa.readthedocs.io",
        "Source Code": "https://github.com/Monash-University-Physics-Astronomy/monashspa",
    },
    license='GPLv3',
    author='School of Physics & Astronomy, Monash University',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Environment :: Console',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                ],
    python_requires='>=3.5, <4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy>=1.15',
        'lmfit>=1.0,<2',
        'requests>=2.21.0,<3',
        'colorama>=0.4.1,<1',
        'pandas>=1.0,<2',
        'scipy==1.4.1',
        'six',
        'piradon',
        'matplotlib',
        'h5py',
    ],
    extras_require={
        'PHS3302': [
            'tensorflow',
            'sklearn',
        ]
    },
    data_files=[
        ('monashspa/PHS2061', ['monashspa/PHS2061/PHS20x1UncertaintiesData.csv']),
        ('monashspa/PHS3000/tutorials', ['monashspa/PHS3000/tutorials/PHS3000UncertaintiesData.csv']),
        ('monashspa/PHS2062', ['monashspa/PHS2062/PHS2062_gas_short_data.csv',
                               'monashspa/PHS2062/PHS2062_gas_short_2_data.csv',
                               'monashspa/PHS2062/PHS2062_gas_data.csv',
                               'monashspa/PHS2062/PHS2062_gas_fit.py',
                               'monashspa/PHS2062/PHS2062_gas_fit.ipynb',
        ]),
        ('monashspa/PHS3302/calorimeter', ['monashspa/PHS3302/calorimeter/calorimeter.py',
                                           'monashspa/PHS3302/calorimeter/calorimeter.ipynb',
        ]),
        ('monashspa/PHS3302/selection', ['monashspa/PHS3302/selection/selection.py',
                                         'monashspa/PHS3302/selection/selection.ipynb',
        ]),
    ]
)
