# -*- coding: utf-8 -*-


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from setuptools import (
	find_packages,
	setup
	)
import os
from glob import glob
from sys import platform


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

setup(
	author = 'Sebastian M. Ernst',
	author_email = 'ernst@pleiszenburg.de',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Topic :: Utilities'
		],
	description = 'Yet Another Build System',
	download_url = 'https://github.com/pleiszenburg/yabs',
	entry_points = '''
		[console_scripts]
		yabs = yabs:yabs_cli
		''',
	extras_require = {},
	include_package_data = True,
	install_requires = [],
	keywords = [],
	license = 'NONE',
	long_description = '',
	name = 'yabs',
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	url = 'https://github.com/pleiszenburg/yabs',
	version = '0.0.0',
	zip_safe = False
	)
