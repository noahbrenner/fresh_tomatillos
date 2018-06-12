import webbrowser
from os.path import abspath

# The main page layout and title bar
with open('template.html', 'r') as f:
    main_page_content = f.read()

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{movie.youtube_id}" data-toggle="modal" data-target="#trailer">
    <img alt="" src="{movie.poster_image_url}" width="220" height="342">
    <h2>{movie.title}</h2>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(movie=movie)
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    webbrowser.open_new_tab('file://' + abspath(output_file.name))
