from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="jsonDB2",
    version="0.1.0",
    author="Musker.Chao",
    author_email="aery_mzc9123@163.com",
    description="A memory-level non-relational database",
    long_description=open("README.md").read(),
    license="MIT",
    keywords= "jsondb memdb db",
    url="https://github.com/spdir/jsonDB2",
    packages=['jsonDB2.jsonDB2'],
    classifiers=[
        "Environment :: DB Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)