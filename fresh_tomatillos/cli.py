# -*- coding: utf-8 -*-

"""
Implements the command-line interface for fresh_tomatillos.


Usage:
  fresh_tomatillos
  fresh_tomatillos <file_path>
  fresh_tomatillos -v | --version
  fresh_tomatillos -h | --help

Where:
  <file_path> is a path to a config file from which to read movie data.

Config File Format:
  [Movie Title]
  summary: Brief description of the plot.
  poster: https://url/of/poster/image
  youtube: YouTube_video-id

Config File notes:
 - `youtube` value may also be a full YouTube URL.
 - Any number of movie sections may be included in a single config file.
"""

from __future__ import print_function, unicode_literals
import errno
import io
import os
import sys
import webbrowser

from . import __version__
from .exceptions import InvalidConfigKeys, InvalidVideoID
from .get_config import get_config
from .media import Movie
from .movie_args import get_movie_args
from .render import compile_movies_page


try:
    # Make sure str() outputs Unicode in Python 2
    str = unicode
except NameError:
    pass  # str is already Unicode in Python 3


USAGE = __doc__.split('\n\n\n')[1]
VERSION = 'Fresh Tomatillos ' + __version__
DIRNAME = os.path.dirname(os.path.abspath(__file__))


def _module_path(path):
    return os.path.join(DIRNAME, path)


def print_err(message):
    """Print Unicode string to stderr."""
    print(str(message), file=sys.stderr)


def main(argv=None):
    """Display movie trailer page in a browser using data from config file."""
    # Get command line arguments
    if argv is None:
        argv = sys.argv[1:]

    # Did the user ask for help?
    if any(arg in ('-h', '--help') for arg in argv):
        print(VERSION + '\n\n' + USAGE)
        return 0

    # Did the user ask for the version?
    if any(arg in ('-v', '--version') for arg in argv):
        print(VERSION)
        return 0

    # Did the user pass to many arguments?
    if len(argv) > 1:
        print_err('Whoops, fresh_tomatillos only accepts 1 argument.\n')
        print_err('USAGE INFO')
        return 1

    # Load settings from the config file
    config_path = argv[0] if argv else _module_path('sample.cfg')
    valid_config_keys = ('summary', 'poster', 'youtube')
    try:
        config = get_config(config_path, valid_config_keys)
    except InvalidConfigKeys as e:
        print_err(e.message)
        return 1
    except (IOError, OSError) as e:
        if e.errno == errno.ENOENT:
            print_err('The specified filename was not found: ' + e.filename)
        elif e.errno == errno.EACCES:
            print_err("You don't have read access to the file: " + e.filename)
        elif e.errno == errno.EISDIR:
            print_err('Expected a file, but found a directory: ' + e.filename)
        else:
            # TODO raise e instead, or optionally provide the stack trace
            print_err(e)
        return 1

    # Compile our list of Movie instances
    try:
        movies = [Movie(*get_movie_args(config, title))
                  for title in config.sections()]
    except InvalidVideoID as e:
        print_err(e.message)
        return 1

    # Uncomment this line for repr output
    # print(repr(movies))

    # Get HTML for the movies page
    try:
        page_content = compile_movies_page(movies)
    except (IOError, OSError) as e:
        if e.errno == errno.ENOENT:
            print_err('Unable to find template file: ' + e.filename)
        elif e.errno == errno.EACCES:
            print_err("Insufficient permissions to read template file: " +
                      e.filename)
        elif e.errno == errno.EISDIR:
            print_err('Expected a template file, but found a directory: ' +
                      e.filename)
        else:
            # TODO raise e instead, or optionally provide the stack trace
            print_err(e)
        return 1

    # Save HTML string to disk
    # For now, always create the file in our package directory so we don't
    # take the chance of overwriting the user's files
    output_path = _module_path('fresh_tomatillos.html')
    try:
        with io.open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(page_content)
    except (IOError, OSError) as e:
        if e.errno == errno.EACCES:
            print_err("Fresh Tomatillos couldn't write the output file: " +
                      e.filename)
        # TODO raise e or optionally provide the stack trace
        print_err(e)
        return 1

    # Open the output file in the browser (in a new tab, if possible)
    print('Opening webpage for:')
    for movie in movies:
        print(str(movie))
    webbrowser.open_new_tab('file://' + output_path)
    return 0
