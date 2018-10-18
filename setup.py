try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bingtts',
    packages=['bingtts'],
    install_requires=[
        'six'
    ],
    version='0.1.6',
    description='Python library to access Microsoft Bing Text to Speech API',
    author='jpattWPC',
    author_email='jpatten@westparkcom.net',
    url='https://github.com/westparkcom/Python-Bing-TTS',
    download_url='https://github.com/westparkcom/Python-Bing-TTS/tarball/master',
    keywords=['microsoft', 'bing', 'text to speech', 'cognitive'],
    classifiers=[],
)
