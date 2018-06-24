# -*- coding: utf-8 -*-
"""
fresh_tomatillos.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the exception classes specific to fresh_tomatillos.

Base Exceptions (not to be used directly):
    Error
    ConfigError

Exceptions For Direct Use:
    InvalidConfigKeys
    InvalidVideoID
"""

from __future__ import unicode_literals


class Error(Exception):
    """Base exception for Fresh Tomatillos.

    Error does not provide any functionality aside from being a base class,
    enabling developers to catch only those exceptions explicitly raised by
    Fresh Tomatillos.
    """

    pass


class ConfigError(Error, ValueError):
    """Base exception for errors in a user-created config file.

    Constructor Args:
        message (str): The Error message to append to ConfigError's header.

    ConfigError provides a heading in an instance's `self.message` string.
    In order to include this header, child classes must pass their own added
    messages to ConfigError's `__init__` method.  See example below:

        class ChildError(ConfigError):
            def __init__(self, message_arg):
                super(ChildError, self).__init__(message_arg)
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
    """Invalid key in at least one "[movie]" section of current config file.

    Constructor Args:
        movie_errors (Iterable[tuple]): Each tuple contained in this
            iterable describes a single movie.  Every movie included has at
            least one error in the names of its config keys.  Every
            contained tuple describing a movie has the form:

                (<title>, <missing_keys>, <extra_keys>)

                Values in each tuple:
                    str: The title of the movie.
                    frozenset[str]: Missing config keys.
                    frozenset[str]: Unexpected config keys.
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
    """Invalid YouTube video ID or URL (may be an error in URL formatting).

    Constructor Args:
        title (str): The title of the movie.
        video_source (str): The string provided by the end user to define a
                            YouTube video.  It could have been a video ID or
                            a full URL.

        source_type (str): The type(s) of data contained in `video_source`
            such as 'ID or URL' or 'URL'.
    """

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
