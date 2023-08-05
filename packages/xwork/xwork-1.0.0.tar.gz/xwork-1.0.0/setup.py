from setuptools import setup, find_packages
import pathlib


readme = pathlib.Path(__file__).parent.resolve()
long_description = (readme / 'README.md').read_text(encoding = "utf-8")



setup(

	name= "xwork",
	version = '1.0.0',
	description="A sample python distribution package",
	long_description = "long_description",
	author = "harshithlaxman",
	author_email = "harshu8310@gmail.com",
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',

	]

	# refer the tutorial  repo at https://github.com/pypa/sampleproject/edit/main/setup.py
	#  pretty good reference for myself



	)
