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
        # (Keep whatever linux audio library you used here)
    ],
    # 🚨 This tells pip to only install the WASAPI patch on Windows machines
    extras_require={
        ':sys_platform == "win32"': ['pyaudiowpatch'],
    },
    entry_points={
        'console_scripts': [
            'songcatch=songcatch.main:run_songcatch',
        ],
    },
)