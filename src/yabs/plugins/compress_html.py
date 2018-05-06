# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


import htmlmin


from yabs.const import (
	AJAX_PREFIX,
	AJAX_SEPARATOR,
	KEY_OUT,
	KEY_ROOT
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


def compress_html_file(file_path):

	with open(file_path, 'r') as f:
		cnt = f.read()

	fn = os.path.basename(file_path)

	if fn.startswith(AJAX_PREFIX):
		self_info_json, html_cnt = cnt.split(AJAX_SEPARATOR)
		cnt = '%s\n%s\n%s' % (
			self_info_json.strip(), AJAX_SEPARATOR, compress_html(html_cnt)
			)
	else:
		cnt = compress_html(cnt)

	with open(file_path, 'w') as f:
		f.write(cnt)


def run(context, options = None):

	for file_path in glob.iglob(os.path.join(context[KEY_OUT][KEY_ROOT], '**/*.htm*'), recursive = True):
		compress_html_file(file_path)
