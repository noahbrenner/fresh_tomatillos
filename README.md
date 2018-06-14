Fresh Tomatillos
================

> Generate a single-page movie trailer website

Fresh Tomatillos will generate the HTML, CSS, and JavaScript to display a page showing movie posters and trailers, then automatically open the page in your default browser. The set of movies their descriptions, posters, and trailers (YouTube videos) are all easily customizable.

Fresh Tomatillos comes with a sample list of movies. The usage described in this section makes use of that sample list. To customize the list of movies, see the [Config File](#config-file) section.

To use this program (effectively), you must have an active internet connection, since images and YouTube videos will not be displayed otherwise. Without an internet connection, you can absolutely run the program to generate the HTML file, you'll just need to view the result later when you *do* have internet access.

Setup
-----

### 1. Make sure Python is installed

Fresh Tomatillos requires a Python interpreter to be installed in order to run. Both **Python 2** and **Python 3** are supported, though version 3 is recommended. Python 2.6.0 is the minimum compatible version.

If you're running Linux or Mac, you likely already have a version of Python installed. You can check the version from a terminal by running:

```bash
python --version
```

If you do not already have Python installed, you can get a copy from <https://www.python.org/downloads/>.

Alternatively, you can install Python using a package manager, if you have one, for example:

```bash
# Using Chocolatey on Windows
choco install python3

# Using Homebrew on Mac
brew install python

# Using apt on Linux
sudo apt install python3
```

There are other package managers for Linux as well, but if you're running Linux, you're probably comfortable working with them. If you run into problems, though, feel free to open an issue!

### 2. Download Fresh Tomatillos

#### Option 1

Clone this repo by running the following in your terminal:

```bash
git clone https://github.com/noahbrenner/fresh_tomatillos.git
```

#### Option 2

Download the [zip file][download] and extract the contents.

Usage
-----

First, open up your terminal and switch to the directory where you cloned or unzipped the Fresh Tomatillo code:

```bash
cd path/to/fresh_tomatillos
```

Then run the `entertainment_center.py` file using Python:

```bash
python entertainment_center.py
```

Or if your Python executable is called `python3`, you can run this instead:

```bash
python3 entertainment_center.py
```

Running these commands will generate a file called `fresh_tomatillos.html` in the same directory and display the page in your default browser. In the browser, you can see the poster image and name of each movie. You can click on any poster to play the trailer for it without leaving that webpage (unless you've disabled JavaScript in your browser).

Config File
-----------

To change this list of movies displayed on the generated page, you can edit the `test.cfg` file with any text editor. The basic format of each movie listed in that file looks like this:

```ini
[Movie Title]
summary: Brief description of the plot.
poster: URL of an image file which will be displayed as the poster
youtube: YouTube video ID
```

### Config Parameters

**All parameters are required for each movie.** If any are missing or if there are extra parameters not defined here (including typos), you will get an error message and the webpage will not be generated. Within the section defined by the movie title, the other parameters may be defined in any order.

* **`[Movie Title]`** - The title must be enclosed in square brackets (`[Name of Movie]`) and on its own line. The brackets designate a section of the config file. All parameters below this line apply to this movie until another movie title is reached.

* **`summary`** - This line starts with `summary:` and is followed by your own brief summary of the movie. Any extra spaces at the beginning and end of your summary will be removed.

* **`poster`** - This line starts with `poster:` and is followed by a URL of an image file. The image file should have approximately the proportions of a standard movie poster One sheet, about 1.5 times as tall as it is wide.

* **`youtube`** - This line starts with `youtube:` and is followed by a YouTube video ID.

  You can find the YouTube video ID in the URL itself. It will be after the characters `v=` and will end before reaching a `&` character, if there is one. The `v=` will immediately follow either a `?` or a `&`. Currently, all YouTube video IDs have 11 characters.

  All of the URLs below point to the same video, which has the ID **`kAG39jKi0lI`**:

  <pre>
  <code>https://www.youtube.com/watch?v=<strong>kAG39jKi0lI</strong>
  https://www.youtube.com/watch?v=<strong>kAG39jKi0lI</strong>&feature=youtu.be
  https://www.youtube.com/watch?feature=youtu.be&v=<strong>kAG39jKi0lI</strong></code>
  </pre>

  YouTube video IDs are case sensitive, so I recommend copying and pasting them rather than typing them out manually.

### Other Technical Details

* After making a change to the config file, you'll need to run the `entertainment_center.py` again to generate a new HTML file.

* The config file must be saved using [UTF-8 encoding][utf-8], which any decent text editor should be able to do. This allows you to use just about any Unicode character in the config file (é ñ א).

* Comments may be included in the config file. They must be on their own line and start with the `#` character.

  ```ini
  # This is a valid comment

  [Some Movie] # NOT a valid comment
  summary: A thing happens! # NOT a valid comment
  # This is a valid comment
  ```

* If you define the same **parameter** more than once for a given movie, the definition of that parameter that is found latest in the file will be the one used.

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
    # Equivalent (capitalization of keys doesn't matter)
    summary: A thing happens!
    SuMmArY: A thing happens!

    # Not equivalent (capitalization of values is respected)
    summary: A THING HAPPENS!
    summary: a thing happens!

    # Also not equivalent (capitalization of movie titles is respected)
    # These would be two separate movie entries
    [My Awesome Movie]
    [mY aWeSoMe MoViE]
    ```

* A `=` character may be used instead of `:` to set movie parameters (except for the title). The following lines are equivalent:

    ```ini
    summary: A thing happens!
    summary=A thing happens!

    # Leading and trailing whitespace is removed, so these
    # lines are treated the same as the examples above
    # (and yes, there is evil trailing whitespace here):
    summary :    A thing happens!  
    summary = A thing happens!  
    ```

[download]: https://github.com/noahbrenner/fresh_tomatillos/archive/master.zip
[utf-8]: https://en.wikipedia.org/wiki/UTF-8

To Do
-----

* Implement `__repr__`, maybe others
* Parse URL to get YouTube ID
    * Check if it's already the ID
    * Validate the calculated URL
* Validate image URLs (no 404) (Check if it's an image format?)
* README: The user must have an active internet connection to verify and display images and YouTube videos
* README: Starter code from Udacity, almost everything modified at this point
* Change directory structure (lib, build)
* GitHub Pages example
* Email GitHub about this not being a fork
* HTML responsive design
* JavaScript adjustments
* Add a CLI?
