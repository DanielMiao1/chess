"""
setup.py
Setup
"""

import setuptools
import sys
import os

if sys.version_info < (2, 7):
	raise ImportError("This library requires Python 2.7 or later.")

setuptools.setup(
	name="chess",
	version="v0.2.2-dev4",
	author="Daniel M",
	author_email="danielmiao2019@icloud.com",
	description="Chess Library for Python 3 and Python 2",
	long_description=open("README.md", "r").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/DanielMiao1/PyChess",
	classifiers=[
		"Programming Language :: Python 3",
		"Operating System :: OS Independent"
	],
	zip_safe=False,
	packages=["chess"],
	package_data={"chess": ["py.typed"]},
	package_dir={"": "."},
	python_requires=">=2.7",
)
