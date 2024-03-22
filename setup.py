from setuptools import setup, find_packages

setup(
    name='twitter_obsidian',
    version='0.1',
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    entry_points={
        'console_scripts': [
            'twitter_obsidian = twitter_obsidian.__main__:main',
        ],
    },
)