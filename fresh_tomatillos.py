# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import webbrowser
import io
from os import path


def _read_file(path):
    """Return the contents of a file as a Unicode string."""
    with io.open(path, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def _create_movie_tiles(movies, tile_template):
    """Return a string containing unique HTML for each movie."""
    return '\n'.join(tile_template.format(movie=movie) for movie in movies)


def open_movies_page(movies):
    """Generate an HTML movies page and open it in a web browser."""
    # Get the content of our HTML templates.  Each one has `{variable}`
    # sections meant to be used with `str.format()`.
    main_page = _read_file('template.html')     # Page layout and title bar
    movie_tile = _read_file('movie_tile.html')  # Single movie tile

    # Get static content to be added to our template
    scripts = _read_file('scripts.js')
    styles = _read_file('styles.css')

    # Compile the full movies page, including movie tiles
    rendered_content = main_page.format(
        movie_tiles=_create_movie_tiles(movies, movie_tile),
        scripts=scripts,
        styles=styles)

    # Get the full path of where we'll save the rendered content
    output_path = path.abspath('fresh_tomatillos.html')

    # Output the file, overwriting it if one already exists
    with io.open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(rendered_content)

    # Open the output file in the browser (in a new tab, if possible)
    webbrowser.open_new_tab('file://' + output_path)
