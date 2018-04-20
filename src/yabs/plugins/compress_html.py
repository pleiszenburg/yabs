# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


import htmlmin


from yabs.const import (
	KEY_PATHS,
	KEY_OUTPUT
	)


def compress_html(content):

	return htmlmin.minify(
		content,
		remove_comments = True,
		remove_empty_space = True,
		remove_all_empty_space = False,
		reduce_empty_attributes = True,
		reduce_boolean_attributes = False,
		remove_optional_attribute_quotes = False,
		keep_pre = True,
		pre_tags = ('pre', 'textarea', 'nomin'),
		pre_attr = 'pre'
		)


def compress_html_file(fn):

	with open(fn, 'r') as f:
		cnt = f.read()

	cnt = compress_html(cnt)

	with open(fn, 'w') as f:
		f.write(cnt)


def run(context):

	for fn in glob.iglob(os.path.join(context[KEY_PATHS][KEY_OUTPUT], '**/*.htm?'), recursive = True):
		compress_html_file(fn)
