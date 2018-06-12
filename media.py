# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class Movie(object):
    """Object representing information about a movie"""

    __youtube_url_base = 'https://www.youtube.com/watch?v=%s'

    def __init__(self, title, summary, poster_url, trailer_youtube_id):
        self.title = title
        self.summary = summary
        # TODO verify that this is a valid URL (same for youtube, if URL?)
        self.poster_image_url = poster_url
        # TODO extract ID if a URL was passed in
        self.youtube_id = trailer_youtube_id

    @property
    def trailer_youtube_url(self):
        return self.__youtube_url_base % self.youtube_id
