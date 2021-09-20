"""
setup.py
Setup
"""

import setuptools

setuptools.setup(
	name="PyChess",
	version="v0.0.4",
	author="Daniel M",
	author_email="danielmiao2019@icloud.com",
	description="A Chess library in Python 3",
	long_description=open("README.md", "r").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/DanielMiao1/PyChess",
	classifiers=["Programming Language :: Python 3"],
	package_dir={"": "."},
	py_modules=["chess"],
	packages=["./"],
	python_requires=">=3",
)
