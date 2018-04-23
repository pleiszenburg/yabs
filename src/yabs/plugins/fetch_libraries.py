# -*- coding: utf-8 -*-


from distutils.version import StrictVersion
import glob
import os
import urllib.request


import bokeh
import requests


from yabs.const import (
	KEY_LIBRARIES,
	KEY_OUT,
	KEY_SCRIPTS,
	KEY_SRC,
	KEY_STYLES,
	KEY_UPDATE
	)


VERSION_FN = '.version'

LIB_JQUERY = 'jquery'
LIB_PLOTLY = 'plotly'
LIB_BOKEH = 'bokeh'

LIB_URL_DICT = {
	LIB_BOKEH: [
		'http://cdn.pydata.org/bokeh/release/bokeh-%s.min.js',
		'http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.js',
		'http://cdn.pydata.org/bokeh/release/bokeh-%s.min.css',
		'http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.css'
		],
	LIB_JQUERY: [
		'https://code.jquery.com/jquery-%s.min.js'
		],
	LIB_PLOTLY: [
		'https://github.com/plotly/plotly.js/blob/v%s/dist/plotly.min.js?raw=true'
		]
	}

LIBRARY_LIST = list(LIB_URL_DICT.keys())


def fetch_library(context, library):

	with open(os.path.join(context[KEY_SRC][KEY_LIBRARIES], library, VERSION_FN), 'r') as f:
		current_version = f.read().strip()

	file_list = []
	for ext in ['css', 'js']:
		file_list.extend(glob.glob(os.path.join(context[KEY_SRC][KEY_LIBRARIES], library, '*.%s' % ext)))

	for src_file_path in file_list:

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		fn = os.path.basename(src_file_path).replace(
			'-%s.min.' % current_version, '.min.'
			)

		if fn.endswith('.css'):
			deployment_path = context[KEY_OUT][KEY_STYLES]
		elif fn.endswith('.js'):
			deployment_path = context[KEY_OUT][KEY_SCRIPTS]
		else:
			raise # TODO

		with open(os.path.join(deployment_path, fn), 'w') as f:
			f.write(cnt)


def get_relevant_version(library):

	if library == LIB_BOKEH:

		return bokeh.__version__

	elif library == LIB_PLOTLY:

		return requests.get(
			url = 'https://api.github.com/repos/plotly/plotly.js/releases/latest'
			).json()['name'][1:]

	elif library == LIB_JQUERY:

		tags = requests.get(url = 'https://api.github.com/repos/jquery/jquery/tags').json()
		versions = [tag['name'] for tag in tags if '-' not in tag['name']]
		versions.sort(key = StrictVersion)
		return versions[-1]

	else:

		raise # TODO


def update_library(context, library):

	library_path = os.path.join(context[KEY_SRC][KEY_LIBRARIES], library)

	# Checks on library folder. Create it if required.
	if os.path.exists(library_path) and not os.path.isdir(library_path):
		raise # TODO
	if not os.path.exists(library_path):
		os.mkdir(library_path)

	new_library_version = get_relevant_version(library)
	version_file_path = os.path.join(library_path, VERSION_FN)

	# check last version
	if os.path.isfile(version_file_path):
		with open(version_file_path, 'r') as f:
			old_library_version = f.read().strip()
		if old_library_version == new_library_version:
			print('Up-to-date: "%s"' % library)
			return

	print('Requires update: "%s"' % library)

	# Remove library files of previous versions
	for src_file_path in glob.glob(os.path.join(library_path, '*.*')):
		os.unlink(src_file_path)

	with open(version_file_path, 'w+') as f:
		f.write(new_library_version)

	for url_pattern in LIB_URL_DICT[library]:

		url = url_pattern % new_library_version

		fn = url.split('/')[-1].split('?')[0]
		if new_library_version not in fn:
			fn = fn.replace('.min', '-%s.min' % new_library_version)

		print('Loading: "%s"' % fn)
		urllib.request.urlretrieve(url, os.path.join(library_path, fn))


def run(context, options = None):

	for library in options[KEY_LIBRARIES]:

		if library not in LIBRARY_LIST:
			raise

		if options[KEY_UPDATE]:
			update_library(context, library)

		fetch_library(context, library)
