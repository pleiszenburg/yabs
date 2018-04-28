# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_DOMAIN,
	KEY_HTML,
	KEY_JINJA,
	KEY_NAME,
	KEY_NAVIGATION,
	KEY_OUT,
	KEY_ROOT,
	KEY_URL
	)


def __fix_navigation__(context):

	for nav_block in context[KEY_NAVIGATION].keys():
		for nav_lang in context[KEY_NAVIGATION][nav_block].keys():
			lang_block_list = []
			for nav_item_name in context[KEY_NAVIGATION][nav_block][nav_lang].keys():
				lang_block_list.append({
					KEY_NAME: nav_item_name,
					KEY_URL: context[KEY_NAVIGATION][nav_block][nav_lang][nav_item_name]
					})
			context[KEY_NAVIGATION][nav_block][nav_lang] = lang_block_list


def run(context, options = None):

	__fix_navigation__(context)

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '**', '*.htm*'), recursive = True):

		with open(os.path.join(file_path), 'r') as f:
			cnt = f.read()

		cnt = context[KEY_JINJA].from_string(cnt).render(
			**{KEY_DOMAIN: context[KEY_DOMAIN]},
			**context[KEY_NAVIGATION]
			)

		with open(os.path.join(file_path), 'w+') as f:
			f.write(cnt)
