# -*- coding: utf-8 -*-
"""
fresh_tomatillos.get_config
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements the parsing and validating of user-created config files.
"""

from __future__ import unicode_literals, with_statement
import io
try:
    from configparser import RawConfigParser  # Python 3
except ImportError:
    from ConfigParser import RawConfigParser  # Python 2

from fresh_tomatillos.exceptions import InvalidConfigKeys


def _movie_key_frozensets(config):
    """Return a generator which yields titles and movie options.

    Args:
        config (ConfigParser): The object from which to draw data.

    Yields:
        tuple[str, frozenset]: Each tuple contains:

            (str): A movie title (a section in `config`).
            (frozenset): The option keys in `config` for that movie.
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
    source file contains duplicate settings.  Top level sections are free
    from duplication for the same reason.  Because of this guarantee,
    sections of `config` are not checked for duplicate values.

    Args:
        config (ConfigParser): The configuration object to validate.
        valid_keys (frozenset): The valid data attributes which every movie
                                in `config` must contain.

    Returns:
        ConfigParser: The same object that was passed in as `config`.

    Raises:
        InvalidConfigKeys: Raised if there are missing or extra option keys
                           for any movie section in `config`.
    """
    # Collect the errors (if any), grouped by config section
    # Results in: ((<str: movie_title>, <missing_keys>, <extra_keys>), ...)
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
        file_path (str): The path to the configuration file.
        valid_keys (Iterable[str]): The valid data attributes which must be
                                    defined for every movie in the config
                                    file.

    Returns:
        ConfigParser: A config object containing data read from `file_path`.

    Raises:
        InvalidConfigKeys: Raised if there are missing or extra data
                           attributes for any movie defined in the config
                           file.  (raised in a call to _verified_config())
    """
    try:
        # Not strict: Allow duplicate config entries to overwrite old values
        config = RawConfigParser(strict=False)
    except TypeError:
        # Python 2 doesn't accept `strict` parameter, but is already not strict
        config = RawConfigParser()

    # Use io.open so we can specify UTF-8 and handle non-ASCII data in Python 2
    with io.open(file_path, 'r', encoding='utf-8') as config_file:
        config.readfp(config_file)

    # Exceptions raised by _verified_config() are not caught here
    return _verified_config(config, frozenset(valid_keys))
