Fresh Tomatillos
================

> Create a single-page website to display your favorite movies' trailers

Fresh Tomatillos will generate a webpage displaying movie posters and trailers, then automatically open the page in your default browser. It is easy to customize the set of movies on the generated page, including descriptions, poster images, and trailers (YouTube videos). From that page, you can click on any poster to play the trailer for it.

Fresh Tomatillos comes with a sample list of movies so that you can test it out right away. To customize the list of movies, see the [Config File](#config-file) section of this README.

To make good use of this program, you must have an active internet connection, since images and YouTube videos will not be displayed otherwise. Even without an internet connection, you can run the program to generate the webpage source file, you'll just need to view the result later when you *do* have internet access.

Setup
-----

### 1. Make sure Python is installed

In order to run Fresh Tomatillos, you will need a Python interpreter installed on your computer. Both **Python 2** and **Python 3** are supported (I recommend Python 3). Python versions of at least 2.7 or 3.3 should work fine. Some earlier versions may also work, but they are not tested.

If you're running Linux or Mac, you probably have a version of Python already installed. You can check the version from a terminal by running:

```bash
python --version
```

* If you do not yet have Python installed, you can get a copy from <https://www.python.org/downloads>.

* Alternatively, you can install Python using a package manager, if you have one, for example:

  ```bash
  # Using Chocolatey on Windows
  choco install python3

  # Using Homebrew on Mac
  brew install python

  # Using apt on Linux
  sudo apt install python3
  ```

  There are plenty of other package managers for Linux as well, but if you're running Linux, you're probably comfortable with the process for using your preferred one. If you run into problems, feel free to open an issue!

### 2. Install Fresh Tomatillos

#### Option 1: `pip`

Run this command in your terminal to install using Python's built-in package manager, `pip`:

```bash
pip install --user git+https://github.com/noahbrenner/fresh_tomatillos.git@master#egg=fresh_tomatillos
```

You can also include the `-e` (editable) flag in that command if you'd like to be able to make local changes to the source code and have those changes reflected immediately when you run the program again.

#### Option 2: `git clone`

Clone this repo by running the following in your terminal:

```bash
git clone https://github.com/noahbrenner/fresh_tomatillos.git
```

Then install using `pip`. I recommend using the `-e` flag so that your installation will reflect any changes you make to the code without reinstalling, but you can leave that flag out if you just want a regular installation. Don't forget the `.` at the end of the `pip` command (specify the current directory):

```bash
cd fresh_tomatillos
pip install --user -e .
```

Usage
-----

### Option 1: After `pip` Install

* Use the sample config file

  ```bash
  fresh_tomatillos
  ```

* Use your own config file (after [creating one](#config-file))

  ```bash
  fresh_tomatillos my_movies.cfg
  ```

* Display usage info

  ```bash
  fresh_tomatillos -h
  fresh_tomatillos --help
  ```

* Display version

  ```bash
  fresh_tomatillos -v
  fresh_tomatillos --version
  ```

### Option 2: Running From a Git Clone

If you cloned the repo, you also have the option of running Fresh Tomatillos from the repo directory. Make sure your working directory is at the top level of the repo first:

```bash
cd path/to/fresh_tomatillos
```

Then run the program using Python explicitly:

```bash
python3 -m fresh_tomatillos
# To run in Python 2 instead, replace `python3` with `python`
```

All of the same arguments can be passed as after a `pip` install, for example:

```bash
python3 -m fresh_tomatillos my_movies.cfg
```

Config File
-----------

To make your own list of movies to display on the generated page, you can create a config file using any plain text editor, then [pass `fresh_tomatillos` the path to your file](#usage). Your config file can have any file extention, but I recommend `.cfg` or `.ini` so that text editors providing syntax highlighting can make use of that feature (e.g. `my_movies.cfg`).

A config file can list any number of movies. The format for each listed movie is:

```ini
[Movie Title]
summary: Brief description of the plot.
poster: URL of an image file which will be displayed as the poster
youtube: YouTube video ID or full URL
```

### Config Parameters

**All 4 parameters are required for each movie.** If any are missing or if there are extra parameters not defined here (including typos), you will get an error message and the webpage will not be generated. Within the section defined by a given movie's title, its other parameters (`key: value` pairs) may be defined in any order.

#### `[Movie Title]`

The title must be enclosed in square brackets (`[Name of Movie]`) and on its own line. These brackets designate a section of the config file. All parameters below the movie title line, but before the next title, apply to this movie.

#### `summary`

This line starts with `summary:` and is followed by a brief summary of the movie. Any extra spaces at the beginning or end of your summary will be removed.

#### `poster`

This line starts with `poster:` and is followed by a URL of an image file. The image file should have approximately the proportions of a standard movie poster [one sheet][one-sheet], about 1.5 times as tall as it is wide.

#### `youtube`

This line starts with `youtube:` and is followed by either a YouTube video ID or a YouTube video URL. YouTube's video IDs are case sensitive and can contain characters that look similar (`1lIi`), so I recommend copying and pasting IDs and URLs rather than typing them out manually.

* Using a **Video ID**:

  You can find the YouTube video ID in the URL itself. It is a string of characters which may contain letters, numbers, underscores, and dashes.

  * In a **long URL** (`youtube.com`), the ID will start after the characters `v=` and end before reaching a `&` character (if there is one). Either a `?` or a `&` will be immediately before the `v=` (so: `?v=` or `&v=`).
  * In a **short URL** (`youtu.be`), it will follow the last `/` character. Currently, all YouTube video IDs have 11 characters.

  All of the URLs below point to the same video, which has the ID **`kAG39jKi0lI`**:

  <pre>
  <code>https://www.youtube.com/watch?v=<strong>kAG39jKi0lI</strong>
  https://www.youtube.com/watch?v=<strong>kAG39jKi0lI</strong>&feature=youtu.be
  https://www.youtube.com/watch?feature=youtu.be&v=<strong>kAG39jKi0lI</strong></code>
  <code>https://youtu.be/<strong>kAG39jKi0lI</strong></code>
  </pre>

* Using a **Video URL**:

  The URL must have one of the following hosts:

    ```
    www.youtube.com   - long URL
    m.youtube.com     - long URL
    youtube.com       - long URL
    youtu.be          - short URL
    ```

### Other Config-related Details

* After making a change to a config file, you'll need to run `fresh_tomatillos` again to generate a new HTML file.

* A config file must be saved using [UTF-8 encoding][utf-8], which any decent text editor should be able to do. This allows you to include just about any Unicode character in the file (é ñ א).

* Comments may be included in config files. Comments must be on their own line and start with a `#` or `;` character. Comments will not affect the generated webpage.

  ```ini
  # This is a valid comment

  [Some Movie] # NOT a valid comment
  summary: A thing happens! # NOT a valid comment
  ; This is a valid comment
  ```

* If you define the same **key** more than once for a given movie, the definition of that parameter that is found latest in the file will be the one used.

  If you define the same **movie** more than once, the movie definition will be treated as though all parameters for it were in a single section (either adding to or overriding previous values). This means that a *new* movie record is not created. Thus, you can't define multiple movies with exactly the same title. One way to include movies with identical names is to use their release year as part of the title (`[The Reboot Reloaded (2000)]`).

  As an example of the parameter overriding described above, this sloppy config file...

  ```ini
  # Don't do any of this! It works, but don't.
  [A]
  summary: one
  youtube: oneoneone11

  [B]
  summary: blah
  poster: http://blah.com/blah.png
  youtube: blahblahbla
  summary: OTHER BLAH
  [A]
  poster: http://two.com/two.jpg
  summary: TWO
  ```

  ...is equivalent to this one:

  ```ini
  [A]
  summary: TWO
  poster: http://two.com/two.jpg
  youtube: oneoneone11

  [B]
  summary: OTHER BLAH
  poster: http://blah.com/blah.png
  youtube: blahblahbla
  ```

  Even though neither of the sections for **A** included all three parameters in the sloppy config file, this would not cause an error since all three parameters *are* defined by the end of the file.

* All *values* are case sensitive, but keys are not.

    ```ini
    # Equivalent (and valid, though weird) - Capitalization of keys doesn't matter
    summary: A thing happens!
    SuMmArY: A thing happens!

    # NOT Equivalent - Capitalization of values is respected
    # The last entery would apply (lowercase version)
    summary: A THING HAPPENS!
    summary: a thing happens!

    # NOT Equivalent - Capitalization of movie titles is respected
    # These would be two separate movie entries
    [My Awesome Movie]
    [mY aWeSoMe MoViE]
    ```

* A `=` character may be used instead of `:` to separate keys and values (this doesn't apply to the title). The following lines are equivalent:

    ```ini
    summary: A thing happens!
    summary=A thing happens!
    ```

    Leading and trailing whitespace is removed, so these lines are treated the same as the examples above (and yes, there is evil trailing whitespace here):

    ```ini
    summary :    A thing happens!  
    summary = A thing happens!  
    ```

About
-----

This project was built starting from Udacity's [ud036_StarterCode][udacity-repo] repo, though almost all of the code in Fresh Tomatillos is new or has been modified from that template.

[one-sheet]: https://en.wikipedia.org/wiki/One_sheet
[udacity-repo]: https://github.com/udacity/ud036_StarterCode
[utf-8]: https://en.wikipedia.org/wiki/UTF-8

To Do
-----

* Validate YouTube video ID
* Validate image URLs (no 404) (Check if it's an image format?)
* README: The user must have an active internet connection to verify images and YouTube videos
* GitHub Pages example
* HTML responsive design
* JavaScript adjustments
