# -*- coding: utf-8 -*-
"""
fresh_tomatillos.movie_args
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides the glue between fresh_tomatillos.get_config and
fresh_tomatillos.media.Movie.  The `generate_movie_args()` function
defined here uses data from a config object to yield the arguments
required by the Movie class's constructor.
"""

from __future__ import unicode_literals
import string
try:
    # Python 3
    from urllib.parse import urlsplit, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlsplit, parse_qs

from .exceptions import InvalidVideoID


YOUTUBE_ID_CHARACTERS = frozenset(string.ascii_letters + string.digits + '-_')
LONG_HOSTNAMES = ('www.youtube.com', 'youtube.com', 'm.youtube.com')
SHORT_HOSTNAMES = ('youtu.be',)


def _is_potential_youtube_id(id_string):
    """Determine whether a string might be a valid YouTube video ID.

    This function does not *guarantee* that id_string is valid when
    returning True, just that it meets some basic requirements:
        - It is not an empty string.
        - It only contains characters that are permitted in video IDs.

    Args:
        id_string (str): The string to test.

    Returns:
        bool: True if `id_string` might be a valid video ID, False otherwise.
    """
    # Assume it's a valid ID if it only has YOUTUBE_ID_CHARACTERS
    # Don't require length of 11, since YouTube could change the length
    return (len(id_string) > 0 and
            frozenset(id_string).issubset(YOUTUBE_ID_CHARACTERS))


def _parse_youtube_url(url):
    """Split a URL into its component parts, correcting for a missing scheme.

    Args:
        url (str): The string assumed to be a URL.

    Returns:
        SplitResult: An object returned by `urllib.parse.urlsplit()`.
    """
    split_url = urlsplit(url)

    # Add a URL scheme if `url` doesn't already include one
    # (without a scheme, urlsplit incorrectly includes the hostname in 'path')
    if (not split_url.scheme):
        split_url = urlsplit('https://' + url)

    return split_url


def _get_youtube_id_from_url(url):
    """Extract a YouTube video ID from a URL.

    Args:
        url (str): The URL to search for a YouTube video ID, which should:
                    - Specify a video (not a channel page, for example).
                    - Have a hostname that matches one of these options:
                        - www.youtube.com
                        - m.youtube.com
                        - youtube.com
                        - youtu.be

    Returns:
        Optional[str]: A YouTube video ID if one was found, otherwise None.
    """
    youtube_id = None  # Initialize return value
    split_url = _parse_youtube_url(url)

    # For URLs like https://www.youtube.com/watch?v=youtube__id
    if split_url.hostname in LONG_HOSTNAMES:
        # e.g. query: {'v': ['youtube__id']}
        query = parse_qs(split_url.query)

        try:
            v_value = query['v'][0]
        except (KeyError, IndexError):
            pass  # The ID was not found
        else:
            if _is_potential_youtube_id(v_value):
                youtube_id = v_value

    # For URLs like https://youtu.be/youtube__id
    elif split_url.hostname in SHORT_HOSTNAMES:
        # Remove leading '/' from '/youtube__id'
        path = split_url.path[1:]

        if _is_potential_youtube_id(path):
            youtube_id = path

    return youtube_id


def _get_youtube_id(youtube_source, title):
    """Return a YouTube video ID.

    Args:
        youtube_source (str): A YouTube video URL or a YouTube video ID.
        title (str): The movie title associated with `youtube_source`.

    Returns:
        str: A YouTube Video ID.

    Raises:
        InvalidVideoID: Raised if `id_string` is neither a valid YouTube
                        video ID nor a valid YouTube URL.
    """
    # Return early if youtube_source already looks like an ID
    if _is_potential_youtube_id(youtube_source):
        return youtube_source

    youtube_id = _get_youtube_id_from_url(youtube_source)

    if not youtube_id:
        raise InvalidVideoID(
            title=title,
            video_source=youtube_source,
            source_type='ID or URL')

    return youtube_id


def generate_movie_args(config):
    """Return a generator, yielding arguments to pass to the Movie constructor.

    Args:
        config (ConfigParser): Every section in `config` is assumed to have
                               string values for all of the following keys:
                                - summary
                                - poster
                                - youtube

    Yields:
        tuple[str, str, str, str]: Each yielded tuple has this form:

                (<title>, <summary>, <poster_url>, <video_id>)

                Values in each tuple:
                    str: A movie title.
                    str: A summary of the movie's plot.
                    str: The URL of an image file of the movie's poster.
                    str: A YouTube video ID for the movie's trailer.

    Raises:
        InvalidVideoID: Raised if the 'youtube' key for any movie in
                        `config` is not valid as a YouTube video ID or URL.
                        (raised in a call to _get_youtube_id())
    """
    def lookup_function(title):
        """Create a function for looking up keys in the `title` config section.

        Args:
            title: (str): The section of `config` in which the returned
                          function will look up values by key.

        Returns:
            Callable[str] -> str: A function to look up values by key, specific
                                  to the `title` section of `config`.
        """
        return lambda key: config.get(title, key)

    for title in config.sections():
        get_key = lookup_function(title)
        yield (title,
               get_key('summary'),
               get_key('poster'),
               # Exceptions raised by _get_youtube_id() are not caught here
               _get_youtube_id(get_key('youtube'), title))
