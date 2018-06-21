# -*- coding: utf-8 -*-

from __future__ import unicode_literals, with_statement
import io

# Use RawConfigParser so that interpolation is not performed when reading data
try:
    from configparser import RawConfigParser  # Python 3
except ImportError:
    from ConfigParser import RawConfigParser  # Python 2

from exception import InvalidConfigKeys


def _movie_key_frozensets(config):
    """Return a generator providing titles and frozensets of movie options.

    Args:
        config: An instance of ConfigParser.

    Yields:
        tuples of (movie_title, movie_keys). Details of tuple contents:
            movie_title: A string - one of the sections in `config`.

            movie_keys: A frozenset - the option keys in `movie_title`.
    """
    for movie_title in config.sections():
        yield movie_title, frozenset(config.options(movie_title))


def _verified_config(config, valid_keys):
    """Determine if `config` has all required values and no extra values.

    If `valid_keys` is ['foo', 'bar'], each movie included in `config` must
    have data stored in the key 'foo' and in the key 'bar'. It must not have
    any other keys.

    Because `config` is an instance of ConfigParser, it will never have
    duplicate keys; ConfigParser simply overwrites the previous value if a
    source file contains duplicate settings.  The same is true for top level
    sections.  Because of this guarantee, sections of `config` are not
    checked for duplicate values.

    Args:
        config: An instance of ConfigParser to validate.

        valid_keys: An iterable of valid keys for each movie in `config` to
            contain.  This will be converted to frozenset if it is not
            already a set or a frozenset.

    Returns:
        The same ConfigParser instance that was passed in.

    Raises:
        InvalidConfigKeys: Raised if there are missing or extra option keys
            for any movie section in `config`.
    """
    if not isinstance(valid_keys, (set, frozenset)):
        valid_keys = frozenset(valid_keys)

    # Collect a list of errors, if any, grouped by config section
    # Results in: ((movie_title, missing_keys, extra_keys), ...)
    errors = tuple((movie_title, valid_keys - keys, keys - valid_keys)
                   for movie_title, keys in _movie_key_frozensets(config)
                   if not valid_keys == keys)

    if errors:
        raise InvalidConfigKeys(errors)

    return config


def get_config(file_path, valid_keys):
    """Return a config object using data from the specified file.

    Each section (each movie) of `config` will be checked to confirm that it
    contains keys to match every value in `valid_keys` AND that it has no
    additional keys.  The *values* in each section are not verified.

    Args:
        file_path: The path to the configuration file.

        valid_keys: An iterable containing the keys which will be considered
            valid for each movie that is defined.

    Returns:
        An instance of ConfigParser.

    Raises:
        InvalidConfigKeys: Raised if there are missing or extra option keys
            for any movie section in `config`.
            (raised in a call to _verified_config())
    """
    config = RawConfigParser()

    # Use io.open so we can specify UTF-8 and handle non-ASCII data in Python 2
    with io.open(file_path, 'r', encoding='utf-8') as config_file:
        config.readfp(config_file)

    # Exceptions raised by _verified_config() are not caught here
    return _verified_config(config, valid_keys)
