# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import string

try:
    # Python 3
    from urllib.parse import urlsplit, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlsplit, parse_qs

from exception import InvalidVideoID


YOUTUBE_ID_CHARACTERS = frozenset(string.ascii_letters + string.digits + '-_')
LONG_HOSTNAMES = ('www.youtube.com', 'youtube.com', 'm.youtube.com')
SHORT_HOSTNAMES = ('youtu.be',)


def _is_potential_youtube_id(id_string):
    """Test whether id_string might be a valid YouTube video ID.

    This function does not *guarantee* that id_string is valid when
    returning True, just that it meets some basic requirements:
        - It is not an empty string.
        - It only contains characters that are permitted in video IDs.

    Args:
        id_string: The string to test.

    Returns:
        True if `id_string` might be a valid YouTube ID, otherwise False.
    """
    # Assume a plain ID if it only has YOUTUBE_ID_CHARACTERS
    # Don't require length of 11, since YouTube could change the length
    return id_string and set(id_string).issubset(YOUTUBE_ID_CHARACTERS)


def _parse_youtube_url(url):
    split_url = urlsplit(url)

    # Add a URL scheme if `url` doesn't already include one
    # (without a scheme, urlsplit incorrectly includes the hostname in 'path')
    if (not split_url.scheme):
        split_url = urlsplit('https://' + url)

    return split_url


def _get_youtube_id_from_url(url):
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
        youtube_source: A YouTube video URL or a YouTube video ID.

            If a URL is provided, it must meet these requirements:
                - Include the scheme (probably 'https').
                - Have a hostname that matches one of these options:
                    - www.youtube.com
                    - m.youtube.com
                    - youtube.com
                    - youtu.be
                - Specify a video (not a channel page, for example).

    Returns:
        A string containing a YouTube Video ID.

    Raises:
        InvalidVideoID: Raised if `id_string` is neither a valid
            YouTube video ID nor a valid YouTube URL.
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


def get_args(config, title):
    """Create a list of arguments to pass to the Movie constructor.

    Args:
        config: A config instance containing the following keys in the
            section for `title` (all values must be strings):
                - summary
                - poster
                - youtube

        title: A string containing the title of the movie.

    Returns:
        A tuple of strings to be used as arguments to our Movie class.
        e.g. ['Movie Title', 'Summary', 'poster_url', 'YouTube_video_id']

    Raises:
        InvalidVideoID: Raised if the 'youtube' key of the current movie is
            not valid as either a  YouTube video ID or a YouTube URL.
            (raised in a call to _get_youtube_id())
    """
    def get_key(key):
        """Look up `key` in config for the current movie title."""
        return config.get(title, key)

    return (title,
            get_key('summary'),
            get_key('poster'),
            # Exceptions raised by _get_youtube_id() are not caught here
            _get_youtube_id(get_key('youtube'), title))
