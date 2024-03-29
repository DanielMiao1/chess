# -*- coding: utf-8 -*-

import setuptools
import sys

if sys.version_info < (2, 5):
	raise ImportError("This library requires Python 2.5 or later.")

setuptools.setup(
	name="chess",
	version="1.1.2",
	author="Daniel M",
	author_email="danielmiao2019@icloud.com",
	description="Chess Library for Python 3 and Python 2",
	long_description=open("README.md", "r").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/DanielMiao1/chess",
	classifiers=[
		"Programming Language :: Python 3",
		"Operating System :: OS Independent"
	],
	zip_safe=False,
	packages=["chess"],
	package_data={"chess": ["py.typed"]},
	package_dir={"": "."},
	python_requires=">=2.5",
)
