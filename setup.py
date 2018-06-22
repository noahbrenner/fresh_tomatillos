from setuptools import setup

from fresh_tomatillos import __version__

setup(
    name='fresh_tomatillos',
    version=__version__,
    zip_safe=False,
    packages=['fresh_tomatillos'],
    package_data={'': ['templates/*', 'static/*']},
    entry_points={
        'console_scripts': [
            'fresh_tomatillos = fresh_tomatillos.__main__:main']}
)
