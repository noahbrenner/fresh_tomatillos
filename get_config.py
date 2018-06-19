# -*- coding: utf-8 -*-

from __future__ import unicode_literals, with_statement
import io

# Use RawConfigParser so that interpolation is not performed when reading data
try:
    from configparser import RawConfigParser  # Python 3
except ImportError:
    from ConfigParser import RawConfigParser  # Python 2


def _has_valid_config_structure(config, valid_keys):
    """
    valid_keys: May be a set, frozenset, or any iterable that can be
                passed to frozenset().
    """
    # if `valid_keys` is not a type of set, convert it to one
    if not isinstance(valid_keys, (set, frozenset)):
        valid_keys = frozenset(valid_keys)

    # Get list of movies (each section of the config describes a single movie)
    movies = config.sections()
    # Access the function which returns all option names for a given movie
    get_keys = config.options

    # We don't need to worry about `frozenset` eliminating duplicate strings
    # because RawConfigParser will never produce duplicate keys.
    if all(frozenset(get_keys(movie)) == valid_keys for movie in movies):
        return True
    else:
        # TODO if invalid, provide the extra and/or missing keys for each movie
        # and include that info when raising an exception
        pass


def get_config(file_path, valid_keys):
    config = RawConfigParser()

    # Use io.open so we can specify UTF-8 and handle non-ASCII data in Python 2
    with io.open(file_path, 'r', encoding='utf-8') as config_file:
        config.readfp(config_file)

    return config if _has_valid_config_structure(config, valid_keys) else None
