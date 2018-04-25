# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_HTML,
	KEY_JINJA,
	KEY_OUT,
	KEY_ROOT
	)


def run(context, options = None):

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '**', '*.htm*'), recursive = True):

		with open(os.path.join(file_path), 'r') as f:
			cnt = f.read()

		cnt = context[KEY_JINJA].from_string(cnt).render()

		with open(os.path.join(file_path), 'w+') as f:
			f.write(cnt)
