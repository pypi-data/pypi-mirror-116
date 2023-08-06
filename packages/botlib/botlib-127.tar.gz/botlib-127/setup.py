# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='127',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    py_modules=["trm"],
    packages=["bot"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
        (
            "share/botlib/",
            [
                "files/bot.1.md",
                "files/botctl.8.md",
                "files/botd.8.md",
                "files/botd.service",
                "files/botd",
            ],
        ),
    ],
    scripts=["bin/bot", "bin/botc", "bin/botd", "bin/botctl"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
