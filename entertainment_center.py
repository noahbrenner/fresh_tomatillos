#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from fresh_tomatillos import open_movies_page
from media import Movie
from get_config import get_config


def _get_movie_args(config, title, keys):
    """Create a list of arguments to pass to the Movie constructor.

    Args:
        config: A config instance containing keys specified in `keys`.
        title: A string containing the title of the movie.
        keys: An iterable specifying, in order, the keys of `config` to use.

    Returns:
        A list of strings to be used as arguments to Movie().

        _get_movie_args(config, 'Foo', ('bar', 'baz'))

        result: ['Foo', config.bar, config.baz]
    """
    result = [title]
    result.extend(config.get(title, key) for key in keys)

    return result


def main():
    """Display movie trailer page in a browser using data from config file."""
    valid_config_keys = ('summary', 'poster', 'youtube')
    config = get_config('test.cfg', valid_config_keys)

    # TODO use try except. If error, print it then exit 1
    if config:
        print(config.sections())
    else:
        print("There's no config!")

    # Compile our list of Movie instances
    movies = [Movie(*_get_movie_args(config, title, valid_config_keys))
              for title in config.sections()]

    # Display our results in the terminal and the browser!
    print(movies)
    open_movies_page(movies)


if __name__ == '__main__':
    main()
