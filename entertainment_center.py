#!/usr/bin/python

from fresh_tomatoes import open_movies_page
from media import Movie

test = Movie('My title', 'Somebody did a thing', 'https://example.com', 'alkv2')

if __name__ == '__main__':
    open_movies_page([test])
