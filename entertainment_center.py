#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

try:
    from future_builtins import map
except ImportError:
    # Already in Python 3
    pass

from fresh_tomatillos import open_movies_page
from media import Movie
from get_config import get_config


def get_movie_args(config, title, keys):
    """
    Assuming `keys = ['summary', 'poster']`, returns a list of the form:
        [title, summary, poster]
    The values are those taken from `config`.
    """
    result = [title]
    result.extend(config.get(title, key) for key in keys)

    return result


if __name__ == '__main__':
    valid_keys = ('summary', 'poster', 'youtube')
    config = get_config('test.cfg', valid_keys)

    # TODO use try except. If error, print it then exit 1
    if config:
        print(config.sections())
    else:
        print("There's no config!")

    movies = list(map(
        lambda title: Movie(*get_movie_args(config, title, valid_keys)),
        config.sections()
    ))

    open_movies_page(movies)
