# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


from yabs.const import (
	KEY_BLOG,
	KEY_CODE,
	KEY_MARKDOWN,
	KEY_MATH,
	KEY_PROJECT,
	KEY_SRC
	)
from yabs.log import log


KNOWN_ENTRY_TYPES = [KEY_MARKDOWN]


class blog_class:


	def __init__(self, src_fld):

		src_file_list = []
		for suffix in KNOWN_ENTRY_TYPES:
			src_file_list.extend(glob.glob(
				os.path.join(src_fld, '**', '*.%s' % suffix),
				recursive = True
				))

		self.entry_list = [blog_entry_class(file_path) for file_path in src_file_list]
		self.language_set = set([entry.language for entry in self.entry_list])


	def create_renderer(self, plugin_func, options):

		self.renderer_dict = {entry_type: {
			language: plugin_func(
				options[entry_type], {
					KEY_CODE: plugin_func(options[KEY_CODE]),
					KEY_MATH: plugin_func(options[KEY_MATH])
					}
				) for language in self.language_set
			} for entry_type in KNOWN_ENTRY_TYPES}


class blog_entry_class:


	def __init__(self, src_file_path):

		fn = os.path.basename(src_file_path)

		self.id = fn.rsplit('.', 1)[0].rsplit('_', 1)[0]
		self.language = fn.rsplit('.', 1)[0].rsplit('_', 1)[1]
		self.type = fn.rsplit('.', 1)[1]

		with open(src_file_path, 'r') as f:
			self.raw = f.read()


	def render(self, renderer):

		pass


def run(context, options = None):

	blog = blog_class(context[KEY_SRC][KEY_BLOG])
	blog.create_renderer(context[KEY_PROJECT].run_plugin, options)
