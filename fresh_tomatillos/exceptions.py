# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Error(Exception):
    """Base exception for Fresh Tomatillos.

    Other exceptions should inherit from Error, but Error should not be
    thrown directly.
    """

    pass


class ConfigError(Error, ValueError):
    """Base exception for errors in a user-created config file.

    Other exceptions should inherit from ConfigError, but ConfigError should
    not be thrown directly.

    ConfigError provides a heading in the `self.message` string, which child
    classes should include by running ConfigError's `__init__` method and
    then append their own messages to the `self.message` string:

        class ChildError(ConfigError):
            def __init__(self, message_arg):
                super(ChildError, self).__init__()
                self.message += message_arg
    """

    def __init__(self, message):
        """Initialize an instance of ConfigError."""
        super(ConfigError, self).__init__()

        # Set `.message` explicitly, since it isn't set by default in Python 3
        self.message = (
            '\nERROR IN CONFIG FILE'
            '\nPlease update your config file and run the program again.'
            '\n' + message)


class InvalidConfigKeys(ConfigError):
    """Invalid key in at least one [movie] section of current config file.

    Constructor Arg:
        An iterable of tuples.  Each tuple contained in the iterable
        describes a single movie which has at least one error in the names
        of its config keys.  Every tuple has the form:

                (title, missing_keys, extra_keys)

            Values in each tuple:
                title: A string - the title of the movie.

                missing_keys: An iterable (usually a frozenset) containing
                    any missing config keys (as strings).  May be empty.

                extra_keys: An iterable (usually a frozenset) containing
                    any unexpected config keys (as strings).  May be empty.
    """

    __heading_template = '\nInvalid config settings for movie:  {title}'

    def __init__(self, movie_errors):
        """Initialize an instance of InvalidConfigKeys."""
        self.config_errors = movie_errors

        # Create the error message string with a section for each movie
        message = []

        for title, missing_keys, extra_keys in movie_errors:
            message.append(self.__heading_template.format(title=title))

            if missing_keys:
                message.append('   This information is missing:')
                message.extend('    - ' + key for key in missing_keys)

            if extra_keys:
                message.append('   This information should not be included:')
                message.extend('    - ' + key for key in extra_keys)

        super(InvalidConfigKeys, self).__init__('\n'.join(message))


class InvalidVideoID(ConfigError):
    """Invalid YouTube video ID or URL (may be an error in URL formatting)."""

    __message_template = (
        '\nInvalid YouTube {self.source_type} for movie:  {self.title}'
        '\n   Invalid {self.source_type}:'
        '\n    {self.video_source}')

    def __init__(self, title, video_source, source_type='ID'):
        """Initialize an instance of InvalidVideoID."""
        self.title = title
        self.video_source = video_source
        self.source_type = source_type

        super(InvalidVideoID, self).__init__(
            self.__message_template.format(self=self))
