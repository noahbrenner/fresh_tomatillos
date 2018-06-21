#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys

from exception import ConfigError
from fresh_tomatillos import open_movies_page
from get_config import get_config
from media import Movie
import movie_args


try:
    # Make sure str() outputs Unicode in Python 2
    str = unicode
except NameError:
    pass  # str is already Unicode in Python 3


def main():
    """Display movie trailer page in a browser using data from config file.

    Raises:
        ValueError: May be raised due to failed validation of the config
            file during a call to one of the following internal functions:
                - get_config()
                - movie_args.get_args()
    """
    # Load settings from the config file
    valid_config_keys = ('summary', 'poster', 'youtube')
    config = get_config('test.cfg', valid_config_keys)

    # Compile our list of Movie instances
    movies = [Movie(*movie_args.get_args(config, title))
              for title in config.sections()]

    # Uncomment this line for repr output
    # print(repr(movies))

    print('Opening webpage for:')

    for movie in movies:
        print(str(movie))

    open_movies_page(movies)


if __name__ == '__main__':
    try:
        main()
    except ConfigError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
