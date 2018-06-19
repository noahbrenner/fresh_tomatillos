# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Movie(object):
    """Object representing information about a movie"""

    __youtube_url_base = 'https://www.youtube.com/watch?v=%s'

    __repr_template = ('Movie(title={self.title!r},'
                       ' summary={self.summary!r},'
                       ' poster_url={self.poster_url!r},'
                       ' youtube_id={self.youtube_id!r})')

    def __init__(self, title, summary, poster_url, youtube_id):
        self.title = title
        self.summary = summary
        # TODO verify that this is a valid URL (same for youtube, if URL?)
        self.poster_url = poster_url
        self.youtube_id = youtube_id

    def __repr__(self):
        return self.__repr_template.format(self=self)

    @property
    def trailer_youtube_url(self):
        return self.__youtube_url_base % self.youtube_id
