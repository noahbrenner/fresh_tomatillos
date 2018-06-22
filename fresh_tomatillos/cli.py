#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import os
import sys

from .exceptions import ConfigError
from .fresh_tomatillos import open_movies_page
from .get_config import get_config
from .media import Movie
from .movie_args import get_movie_args


try:
    # Make sure str() outputs Unicode in Python 2
    str = unicode
except NameError:
    pass  # str is already Unicode in Python 3


def main_logic():
    """Display movie trailer page in a browser using data from config file.

    Raises:
        ValueError: May be raised due to failed validation of the config
            file during a call to one of the following internal functions:
                - get_config()
                - movie_args.get_args()
    """
    # Load settings from the config file
    valid_config_keys = ('summary', 'poster', 'youtube')
    config_file_path = os.path.join(os.path.dirname(__file__), 'test.cfg')
    config = get_config(config_file_path, valid_config_keys)

    # Compile our list of Movie instances
    movies = [Movie(*get_movie_args(config, title))
              for title in config.sections()]

    # Uncomment this line for repr output
    # print(repr(movies))

    print('Opening webpage for:')

    for movie in movies:
        print(str(movie))

    open_movies_page(movies)


# Separate function so that we can handle all internal errors at once
def main():
    """Display movie trailer page in a browser using data from config file.

    Catch errors inheriting from package-specific ConfigError and print
    their error messages out to the console before exiting.  This creates a
    better user experience when run as a CLI, while still providing feedback
    on the user's mistake when creating the config file.
    """
    try:
        main_logic()
    except ConfigError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
