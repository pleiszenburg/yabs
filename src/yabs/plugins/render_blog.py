# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


from yabs.const import (
	KEY_BLOG,
	KEY_CODE,
	KEY_MARKDOWN,
	KEY_MATH,
	KEY_PROJECT,
	KEY_SRC,
	KEY_TEMPLATES,
	KEY_VOCABULARY
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


	def create_renderer(self, plugin_func, render_plugins, templates, vocabulary):

		self.renderer_dict = {entry_type: {
			language: plugin_func(
				render_plugins[entry_type], {
					KEY_CODE: plugin_func(render_plugins[KEY_CODE]),
					KEY_MATH: plugin_func(render_plugins[KEY_MATH]),
					KEY_VOCABULARY: vocabulary[language],
					KEY_TEMPLATES: templates
					}
				) for language in self.language_set
			} for entry_type in KNOWN_ENTRY_TYPES}


	def render_entries(self):

		for entry in self.entry_list:
			entry.render(self.renderer_dict)


class blog_entry_class:


	def __init__(self, src_file_path):

		fn = os.path.basename(src_file_path)

		self.id = fn.rsplit('.', 1)[0].rsplit('_', 1)[0]
		self.language = fn.rsplit('.', 1)[0].rsplit('_', 1)[1]
		self.type = fn.rsplit('.', 1)[1]

		with open(src_file_path, 'r') as f:
			self.raw = f.read()


	def __preprocess_md__(self):

		meta, self.content = self.raw.split('\n\n', 1)
		self.meta_dict = load(meta, Loader = Loader)


	def render(self, renderer_dict):

		getattr(self, '__preprocess_%s__' % self.type)()

		html = renderer_dict[self.type][self.language](self.content)
		print(html)


def run(context, options = None):

	blog = blog_class(context[KEY_SRC][KEY_BLOG])
	blog.create_renderer(
		context[KEY_PROJECT].run_plugin, options, context[KEY_TEMPLATES], context[KEY_VOCABULARY]
		)
	blog.render_entries()
