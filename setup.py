# -*- coding: utf-8 -*-
"""
Fresh Tomatillos
----------------

Generate a webpage displaying posters and trailers for your favorite movies.



To install:

    $ pip install --user git+https://github.com/noahbrenner/fresh_tomatillos.git@master#egg=fresh_tomatillos

GitHub Repo:
https://github.com/noahbrenner/fresh_tomatillos
"""

from setuptools import setup

from fresh_tomatillos import __version__

setup(
    name='fresh_tomatillos',
    version=__version__,
    zip_safe=False,
    packages=['fresh_tomatillos'],
    package_data={'': ['templates/*', 'static/*']},
    entry_points={
        'console_scripts': [
            'fresh_tomatillos = fresh_tomatillos.__main__:main']}
)
