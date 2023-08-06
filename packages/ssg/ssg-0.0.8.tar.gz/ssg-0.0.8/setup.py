#! /usr/bin/env python

"""
Thai syllable segmentation using Conditional Random Fields
"""

from setuptools import setup

setup(
    name="ssg",
    packages=["ssg"],
    package_dir={"ssg": "ssg"},
    include_package_data=True,
    package_data={"ssg": ["artifacts/crf3_mix.crfsuite2"]},
    scripts=["scripts/ssg-cli"],
    version="0.0.8",
    install_requires=[
        'fire>=0.1.3',
        'python-crfsuite>=0.9.6',
        'tqdm>=4.32.2'
    ],
    description="Thai syllable segmentation using Conditional Random Fields",
    author="Ponrawee Prasertsom",
    author_email="ponrawee.pra@gmail.com",
    url="https://github.com/ponrawee/ssg",
    license="Apache Software License 2.0",
    download_url="https://github.com/ponrawee/ssg.git",
    keywords=["crf", "syllable", "tokenization", "thai"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Thai",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Linguistic"
    ],
)
