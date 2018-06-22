from setuptools import setup

setup(
    name='fresh_tomatillos',
    version='0.1.0',
    zip_safe=False,
    packages=['fresh_tomatillos'],
    package_data={'': ['templates/*', 'static/*']},
    entry_points={
        'console_scripts': [
            'fresh_tomatillos = fresh_tomatillos.__main__:main']}
)
