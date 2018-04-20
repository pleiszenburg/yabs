# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_OUT,
	KEY_SCRIPTS,
	KEY_SRC
	)


def run(context):

	os.mkdir(context[KEY_OUT][KEY_SCRIPTS])

	for src_file_path in glob.glob(os.path.join(context[KEY_SRC][KEY_SCRIPTS], '*.js')):

		fn = os.path.basename(src_file_path)

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		with open(os.path.join(context[KEY_SRC][KEY_SCRIPTS], fn), 'w') as f:
			f.write(cnt)
