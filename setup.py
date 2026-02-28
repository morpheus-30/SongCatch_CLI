from setuptools import setup, find_packages

setup(
    name='songcatch',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydub',
        'spotipy',
        'python-dotenv', 
        # ADD WHATEVER AUDIO LIBRARY YOU USED IN audio.py HERE (e.g., 'sounddevice', 'pyaudio')
    ],
    entry_points={
        'console_scripts': [
            'songcatch=songcatch.main:run_songcatch',
        ],
    },
)