class Movie(object):
    """Object representing information about a movie"""

    __youtube_url_base = 'https://www.youtube.com/watch?v=%s'

    def __init__(self, title, summary, poster_url, trailer_youtube_id):
        self.title = title
        self.summary = summary
        self.poster_image_url = poster_url
        self.youtube_id = trailer_youtube_id

    @property
    def trailer_youtube_url(self):
        return self.__youtube_url_base % self.youtube_id
