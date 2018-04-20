# -*- coding: utf-8 -*-


import glob
import os


import jinja2


from yabs.const import (
	KEY_HTML,
	KEY_OUT,
	KEY_ROOT,
	KEY_SRC
	)


def run(context):

	for src_file_path in glob.iglob(os.path.join(context[KEY_SRC][KEY_HTML], '**/*.htm?'), recursive = True):

		fn = os.path.basename(src_file_path)

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), 'w') as f:
			f.write(cnt)
