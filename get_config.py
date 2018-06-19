# -*- coding: utf-8 -*-

from __future__ import unicode_literals, with_statement
import io

# Use RawConfigParser so that interpolation is not performed when reading data
try:
    from configparser import RawConfigParser  # Python 3
except ImportError:
    from ConfigParser import RawConfigParser  # Python 2


def _find_config_errors(config, valid_keys):
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
        config: An instance of *ConfigParser to validate.

        valid_keys: An iterable of valid keys for each movie in `config` to
            contain.  This will be converted to frozenset if it's not
            already a set or a frozenset.

    Returns:
        An error string, appropriate for surfacing to end users, which
        describes any extra and/or missing keys in `config`.  If there are no
        errors, returns None.
    """
    if not isinstance(valid_keys, (set, frozenset)):
        valid_keys = frozenset(valid_keys)

    errors = None

    # Check each config section for errors
    for movie in config.sections():
        movie_keys = frozenset(config.options(movie))

        # If there are invalid config keys, collect data to report to the user
        if not movie_keys == valid_keys:
            errors = errors or []  # Initialize errors if it doesn't exist
            errors.extend([
                'Config settings for the movie [%s] are not valid.' % movie,
                'Please update your config file and run the program again.'])

            missing_keys = valid_keys - movie_keys
            extra_keys = movie_keys - valid_keys

            if missing_keys:
                errors.extend([
                    '  This information is missing:',
                    '\n'.join('   - ' + key for key in missing_keys)])

            if extra_keys:
                errors.extend([
                    '  This information should not be included:',
                    '\n'.join('   - ' + key for key in extra_keys)])

    return '\n'.join(errors) if errors else None


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
        ValueError: Raised if there were extra or missing keys in `config`.
    """
    config = RawConfigParser()

    # Use io.open so we can specify UTF-8 and handle non-ASCII data in Python 2
    with io.open(file_path, 'r', encoding='utf-8') as config_file:
        config.readfp(config_file)

    # Check config data for errors
    error_message = _find_config_errors(config, valid_keys)

    if error_message:
        raise ValueError(error_message)

    return config
