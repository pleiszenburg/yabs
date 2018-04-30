# -*- coding: utf-8 -*-


from distutils.version import StrictVersion
import fnmatch
import glob
import io
import os
from pprint import pformat as pf
import urllib.request
import zipfile


import bokeh
import requests


from yabs.const import (
	FONT_SUFFIX_LIST,
	KEY_FONTS,
	KEY_GITHUB,
	KEY_LIBRARIES,
	KEY_OUT,
	KEY_RELEASE,
	KEY_SCRIPTS,
	KEY_SRC,
	KEY_STYLES,
	KEY_TAGS,
	KEY_UPDATE,
	KEY_VERSION
	)
from yabs.log import log


VERSION_FN = '.version'

LIB_JQUERY = 'jquery'
LIB_PLOTLY = 'plotly'
LIB_BOKEH = 'bokeh'
LIB_KATEX = 'katex'

LIB_DICT = {
	'bokeh': {
		KEY_SRC: [
			'http://cdn.pydata.org/bokeh/release/bokeh-%s.min.js',
			'http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.js',
			'http://cdn.pydata.org/bokeh/release/bokeh-%s.min.css',
			'http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.css'
			]
		},
	'jquery': {
		KEY_GITHUB: 'jquery/jquery',
		KEY_VERSION: KEY_TAGS,
		KEY_SRC: [
			'https://code.jquery.com/jquery-%s.min.js'
			]
		},
	'normalize.css': {
		KEY_GITHUB: 'necolas/normalize.css',
		KEY_VERSION: KEY_TAGS,
		KEY_SRC: [
			'https://raw.githubusercontent.com/necolas/normalize.css/%s/normalize.css'
			]
		},
	'plotly': {
		KEY_GITHUB: 'plotly/plotly.js',
		KEY_VERSION: KEY_RELEASE,
		KEY_SRC: [
			'https://github.com/plotly/plotly.js/blob/v%s/dist/plotly.min.js?raw=true'
			]
		},
	'katex': {
		KEY_GITHUB: 'Khan/KaTeX',
		KEY_VERSION: KEY_RELEASE,
		KEY_SRC: [
			'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/%s/katex.min.css',
			'katex/fonts/*.*@https://github.com/Khan/KaTeX/releases/download/v%s/katex.zip'
			]
		}
	}


LIBRARY_LIST = list(LIB_DICT.keys())


def fetch_library(context, library):

	with open(os.path.join(context[KEY_SRC][KEY_LIBRARIES], library, VERSION_FN), 'r') as f:
		current_version = f.read().strip()

	file_list = []
	for ext in ['css', 'js'] + FONT_SUFFIX_LIST:
		file_list.extend(glob.glob(os.path.join(context[KEY_SRC][KEY_LIBRARIES], library, '*.%s' % ext)))

	for src_file_path in file_list:

		with open(src_file_path, 'rb') as f:
			cnt = f.read()

		fn = os.path.basename(src_file_path).replace(
			'-%s.min.' % current_version, '.min.'
			)

		if fn.endswith('.css'):
			deployment_path = context[KEY_OUT][KEY_STYLES]
		elif fn.endswith('.js'):
			deployment_path = context[KEY_OUT][KEY_SCRIPTS]
		elif any(fn.endswith('.%s' % ext) for ext in FONT_SUFFIX_LIST):
			deployment_path = context[KEY_OUT][KEY_FONTS]
		else:
			raise # TODO

		with open(os.path.join(deployment_path, fn), 'wb') as f:
			f.write(cnt)


def get_relevant_version(library):

	if library == 'bokeh':

		return bokeh.__version__

	elif LIB_DICT[library][KEY_VERSION] == KEY_TAGS:

		tags = requests.get(url = 'https://api.github.com/repos/%s/tags' % LIB_DICT[library][KEY_GITHUB]).json()
		try:
			versions = [tag['name'] for tag in tags if '-' not in tag['name']]
			versions = [tag.lstrip('v') for tag in versions]
		except:
			log.error('Failed to parse version from Github response.')
			log.error(pf(tags))
			raise # TODO
		versions.sort(key = StrictVersion)
		return versions[-1]

	elif LIB_DICT[library][KEY_VERSION] == KEY_RELEASE:

		return requests.get(
			url = 'https://api.github.com/repos/%s/releases/latest' % LIB_DICT[library][KEY_GITHUB]
			).json()['name'][1:]

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
			log.debug('%s up to date ...' % library)
			return

	log.info('Updating %s ...' % library)

	# Remove library files of previous versions
	for src_file_path in glob.glob(os.path.join(library_path, '*.*')):
		os.unlink(src_file_path)

	with open(version_file_path, 'w+') as f:
		f.write(new_library_version)

	for url_pattern in LIB_DICT[library][KEY_SRC]:

		url = url_pattern % new_library_version

		if url.startswith('http'):

			fn = url.split('/')[-1].split('?')[0]
			if new_library_version not in fn:
				fn = fn.replace('.min', '-%s.min' % new_library_version)

			fp = os.path.join(library_path, fn)
			urllib.request.urlretrieve(url, fp)

			if library == LIB_KATEX and fn.endswith('.css'):
				with open(fp, 'r') as f:
					cnt = f.read()
				cnt = cnt.replace(
					'url(fonts/',
					'url(%s/' % os.path.relpath(context[KEY_OUT][KEY_FONTS], context[KEY_OUT][KEY_STYLES])
					)
				with open(fp, 'w+') as f:
					f.write(cnt)

		elif '@' in url:

			path_pattern, url = url.split('@')
			zip_bin = requests.get(url, stream = True)

			with zipfile.ZipFile(io.BytesIO(zip_bin.content)) as z:
				for fp in z.namelist():
					if not fnmatch.fnmatch(fp, path_pattern):
						continue
					with open(os.path.join(library_path, os.path.basename(fp)), 'wb') as f:
						f.write(z.read(fp))

		else:

			raise


def run(context, options = None):

	for library in options[KEY_LIBRARIES]:

		if library not in LIBRARY_LIST:
			raise

		if options[KEY_UPDATE]:
			update_library(context, library)

		fetch_library(context, library)
