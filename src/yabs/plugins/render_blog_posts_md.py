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
	AJAX_PREFIX,
	BLOG_PREFIX,
	KEY_ABSTRACT,
	KEY_AUTHORS,
	KEY_BASE,
	KEY_BLOG,
	KEY_CONTENT,
	KEY_CODE,
	KEY_CTIME,
	KEY_EMAIL,
	KEY_FIRSTNAME,
	KEY_FN,
	KEY_ID,
	KEY_LANGUAGE,
	KEY_LANGUAGES,
	KEY_LASTNAME,
	KEY_MARKDOWN,
	KEY_MATH,
	KEY_MTIME,
	KEY_OUT,
	KEY_PROJECT,
	KEY_ROOT,
	KEY_SLUG,
	KEY_SRC,
	KEY_SUBTITLE,
	KEY_TEMPLATE,
	KEY_TEMPLATES,
	KEY_TITLE,
	KEY_VOCABULARY
	)
from yabs.log import log


class blog_class:


	def __init__(self, context, options):

		self.context = context
		self.slug = self.context[KEY_PROJECT].run_plugin(options[KEY_SLUG])

		src_file_list = glob.glob(
			os.path.join(self.context[KEY_SRC][KEY_BLOG], '**', '*.%s' % KEY_MARKDOWN),
			recursive = True
			)

		self.entry_list = [blog_entry_class(context, file_path, self.slug) for file_path in src_file_list]
		self.language_set = set([entry.meta_dict[KEY_LANGUAGE] for entry in self.entry_list])
		self.__match_language_versions__()

		self.renderer_dict = {
			language: self.context[KEY_PROJECT].run_plugin(
				options[KEY_MARKDOWN], {
					KEY_CODE: self.context[KEY_PROJECT].run_plugin(options[KEY_CODE]),
					KEY_MATH: self.context[KEY_PROJECT].run_plugin(options[KEY_MATH]),
					KEY_VOCABULARY: self.context[KEY_VOCABULARY][language],
					KEY_TEMPLATES: self.context[KEY_TEMPLATES],
					KEY_LANGUAGE: language
					}
				) for language in self.language_set
			}


	def __match_language_versions__(self):

		self.entry_dict = {}

		for entry in self.entry_list:
			if entry.meta_dict[KEY_ID] not in self.entry_dict.keys():
				self.entry_dict[entry.meta_dict[KEY_ID]] = []
			self.entry_dict[entry.meta_dict[KEY_ID]].append((entry.meta_dict[KEY_LANGUAGE], entry.meta_dict[KEY_FN]))

		languages_set = set(self.context[KEY_LANGUAGES])
		for entry_key in self.entry_dict.keys():
			entry_languages = set([lang for lang, _ in self.entry_dict[entry_key]])
			missing_translations = languages_set - entry_languages
			for lang in missing_translations:
				self.entry_dict[entry_key].append((lang, str(None)))
			self.entry_dict[entry_key].sort()


	def render_entries(self):

		for entry in self.entry_list:
			entry.render(self.renderer_dict, self.entry_dict[entry.meta_dict[KEY_ID]])


class blog_entry_class:


	def __init__(self, context, src_file_path, slug_func):

		def get_entry_segments():
			with open(src_file_path, 'r') as f:
				raw = f.read()
			return raw.split('\n\n', 1)

		self.context = context
		self.slug_func = slug_func

		meta, self.content = get_entry_segments()
		self.meta_dict = self.__process_blog_post_meta__(src_file_path, meta)


	def __process_blog_post_meta__(self, src_file_path, meta):

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

		fn = os.path.basename(src_file_path)

		meta_dict = {
			KEY_LANGUAGE: fn.rsplit('.', 1)[0].rsplit('_', 1)[1],
			KEY_ID: fn.rsplit('.', 1)[0].rsplit('_', 1)[0],
			**load(meta, Loader = Loader)
			}

		meta_dict[KEY_AUTHORS] = [
			process_author(author) for author in meta_dict[KEY_AUTHORS]
			]

		for time_key in [KEY_CTIME, KEY_MTIME]:
			if time_key not in meta_dict.keys():
				continue
			meta_dict['%s_datetime' % time_key] = meta_dict[time_key].replace(' ', 'T')

		meta_dict[KEY_FN] = '%s%s.htm' % (BLOG_PREFIX, self.slug_func(meta_dict[KEY_TITLE]))

		return meta_dict


	def __postprocess_md__(self, html):

		soup = BeautifulSoup(html, 'html.parser')

		for h_level in range(5, 0, -1):
			for h_tag in soup.find_all('h%d' % h_level):
				h_tag.name = 'h%d' % (h_level + 1)

		return str(soup) # soup.prettify()


	def render(self, renderer_dict, entry_language_list):

		content = renderer_dict[self.meta_dict[KEY_LANGUAGE]](self.content)
		self.meta_dict[KEY_ABSTRACT] = renderer_dict[self.meta_dict[KEY_LANGUAGE]](self.meta_dict[KEY_ABSTRACT])

		content = self.__postprocess_md__(content)

		self.meta_dict[KEY_CONTENT] = content

		for template_prefix, prefix in [
			(KEY_BASE, ''),
			('%s%s' % (AJAX_PREFIX, KEY_BASE), AJAX_PREFIX)
			]:

			with open(os.path.join(
				self.context[KEY_OUT][KEY_ROOT], prefix + self.meta_dict[KEY_FN]
				), 'w+') as f:

				f.write(self.context[KEY_TEMPLATES]['blog_article'].render(
					**{
						KEY_LANGUAGES: str(entry_language_list),
						KEY_TEMPLATE: template_prefix
						},
					**self.meta_dict
					))


def run(context, options = None):

	blog = blog_class(context, options)
	blog.render_entries()
