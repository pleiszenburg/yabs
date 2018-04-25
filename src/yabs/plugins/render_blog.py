# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


from bs4 import BeautifulSoup

from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


from yabs.const import (
	KEY_ABSTRACT,
	KEY_AUTHORS,
	KEY_BLOG,
	KEY_CONTENT,
	KEY_CODE,
	KEY_EMAIL,
	KEY_FIRSTNAME,
	KEY_LASTNAME,
	KEY_MARKDOWN,
	KEY_MATH,
	KEY_OUT,
	KEY_PROJECT,
	KEY_ROOT,
	KEY_SRC,
	KEY_SUBTITLE,
	KEY_TEMPLATES,
	KEY_TITLE,
	KEY_VOCABULARY
	)
from yabs.log import log


KNOWN_ENTRY_TYPES = [KEY_MARKDOWN]


class blog_class:


	def __init__(self, context):

		self.context = context

		src_file_list = []
		for suffix in KNOWN_ENTRY_TYPES:
			src_file_list.extend(glob.glob(
				os.path.join(self.context[KEY_SRC][KEY_BLOG], '**', '*.%s' % suffix),
				recursive = True
				))

		self.entry_list = [blog_entry_class(context, file_path) for file_path in src_file_list]
		self.language_set = set([entry.language for entry in self.entry_list])


	def create_renderer(self, options):

		self.renderer_dict = {entry_type: {
			language: self.context[KEY_PROJECT].run_plugin(
				options[entry_type], {
					KEY_CODE: self.context[KEY_PROJECT].run_plugin(options[KEY_CODE]),
					KEY_MATH: self.context[KEY_PROJECT].run_plugin(options[KEY_MATH]),
					KEY_VOCABULARY: self.context[KEY_VOCABULARY][language],
					KEY_TEMPLATES: self.context[KEY_TEMPLATES]
					}
				) for language in self.language_set
			} for entry_type in KNOWN_ENTRY_TYPES}


	def render_entries(self):

		for entry in self.entry_list:
			entry.render(self.renderer_dict)


class blog_entry_class:


	def __init__(self, context, src_file_path):

		self.context = context

		fn = os.path.basename(src_file_path)

		self.id = fn.rsplit('.', 1)[0].rsplit('_', 1)[0]
		self.language = fn.rsplit('.', 1)[0].rsplit('_', 1)[1]
		self.type = fn.rsplit('.', 1)[1]

		with open(src_file_path, 'r') as f:
			self.raw = f.read()


	def __preprocess_md__(self):

		def process_author(in_data):

			if isinstance(in_data, str):
				lastname, firstname = in_data.split(',')
				email = ''
			elif isinstance(in_data, dict):
				lastname, firstname = list(in_data.keys())[0].split(',')
				email = list(in_data.values())[0].strip()
			else:
				raise # TODO

			return {
				KEY_LASTNAME: lastname.strip(),
				KEY_FIRSTNAME: firstname.strip(),
				KEY_EMAIL: email
				}

		meta, self.content = self.raw.split('\n\n', 1)
		self.meta_dict = load(meta, Loader = Loader)
		self.meta_dict[KEY_AUTHORS] = [
			process_author(author) for author in self.meta_dict[KEY_AUTHORS]
			]


	def __postprocess_md__(self, html):

		soup = BeautifulSoup(html, 'html.parser')

		for h_level in range(5, 0, -1):
			for h_tag in soup.find_all('h%d' % h_level):
				h_tag.name = 'h%d' % (h_level + 2)

		return str(soup) # soup.prettify()


	def render(self, renderer_dict):

		getattr(self, '__preprocess_%s__' % self.type)()

		content = renderer_dict[self.type][self.language](self.content)
		self.meta_dict[KEY_ABSTRACT] = renderer_dict[self.type][self.language](self.meta_dict[KEY_ABSTRACT])

		content = getattr(self, '__postprocess_%s__' % self.type)(content)

		self.meta_dict[KEY_CONTENT] = content

		html = self.context[KEY_TEMPLATES]['blog_article'].render(**self.meta_dict)

		for template_prefix, fn_pattern in [
			('base', 'blog_%s.htm'),
			('ajax_base', 'ajax_%s.htm')
			]:
			with open(os.path.join(
				self.context[KEY_OUT][KEY_ROOT],
				fn_pattern % self.meta_dict[KEY_TITLE].replace(' ', '-')
				), 'w+') as f:
				f.write('{%% extends "%s.htm" %%}\n{%% block %s %%}%s{%% endblock %%}' % (
					template_prefix, KEY_CONTENT, html
					))


def run(context, options = None):

	blog = blog_class(context)
	blog.create_renderer(options)
	blog.render_entries()
