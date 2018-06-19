#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys

from fresh_tomatillos import open_movies_page
from media import Movie
from get_config import get_config
import movie_args


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

    # Display our results in the terminal and the browser
    print(movies)
    open_movies_page(movies)


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e.args[0], file=sys.stderr)
        sys.exit(1)
