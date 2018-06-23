# -*- coding: utf-8 -*-
"""
fresh_tomatillos.media
~~~~~~~~~~~~~~~~~~~~~~

Defines the Movie class at the heart of fresh_tomatillos.
"""

from __future__ import unicode_literals


class Movie(object):
    """Class for representing movie data.

    Constructor Args:
        title (str): The title of the movie.

        summary (str): A brief summary of the movie's plot.

        poster_url (str): The URL of an image file of the movie's poster.

        youtube_id (str): A YouTube video ID for the movie's trailer.

    Instance Attributes:
        title (str): The title of the movie.

        summary (str): A brief summary of the movie's plot.

        poster_url (str): The URL of an image file of the movie's poster.

        youtube_id (str): A YouTube video ID for the movie's trailer.

        youtube_url (str): The full YouTube URL for the movie's trailer.
            (read only)
    """

    __slots__ = ['title', 'summary', 'poster_url', 'youtube_id']

    __repr_template = ('Movie(title={self.title!r},'
                       ' summary={self.summary!r},'
                       ' poster_url={self.poster_url!r},'
                       ' youtube_id={self.youtube_id!r})')

    __str_template = '<Movie: {self.title}>'

    __youtube_url_base = 'https://www.youtube.com/watch?v={self.youtube_id}'

    def __init__(self, title, summary, poster_url, youtube_id):
        """Initialize a Movie instance."""
        self.title = title
        self.summary = summary
        # TODO verify that this is a valid URL (same for youtube, if URL?)
        self.poster_url = poster_url
        self.youtube_id = youtube_id

    def __repr__(self):
        """Return a string `s` such that `Movie(s)` replicates the instance."""
        return self.__repr_template.format(self=self)

    def __str__(self):
        """Return a simple string identifying a Movie instance."""
        return self.__str_template.format(self=self)

    @property
    def youtube_url(self):
        return self.__youtube_url_base.format(self=self)
