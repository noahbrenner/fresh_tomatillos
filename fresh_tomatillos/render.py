# -*- coding: utf-8 -*-
"""
fresh_tomatillos.render
~~~~~~~~~~~~~~~~~~~~~~~

Provides `compile_movies_page()` to render a movie trailer webpage.
"""

from __future__ import unicode_literals
import io
import os


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


def _read_file(relative_path):
    """Return the contents of a file as a Unicode string.

    Args:
        relative_path (str): The path to the file, relative to this module.

    Returns:
        str: The contents of the file.
    """
    path = os.path.normpath(os.path.join(MODULE_DIR, relative_path))

    with io.open(path, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def _create_movie_tiles(movies, tile_template):
    """Return a string containing unique HTML for each movie.

    Args:
        movies (list[Movie]): The movies for which to render content.

        tile_template (str): The template string to be used with
            str.format() containing references in curly braces to
            movie attributes such as "{movie.title}".

    Returns:
        str: The concatenation of all rendered movie tiles.
    """
    return '\n'.join(tile_template.format(movie=movie) for movie in movies)


def compile_movies_page(movies):
    """Return generated HTML for movies page.

    Args:
        movies (list[Movie]): The movies to include in the webpage.

    Returns:
        str: Rendered HTML for a movie trailer page.
    """
    # Get template and static content.  Each template has `{variable}`
    # sections meant to be used with `str.format()`.
    main_page = _read_file('templates/main_page.html')
    movie_tile = _read_file('templates/movie_tile.html')
    scripts = _read_file('static/scripts.js')
    styles = _read_file('static/styles.css')

    # Compile the full movies page, including movie tiles
    rendered_content = main_page.format(
        movie_tiles=_create_movie_tiles(movies, movie_tile),
        scripts=scripts,
        styles=styles)

    return rendered_content
