# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_OUT,
	KEY_ROOT,
	KEY_SRC,
	KEY_STYLES
	)


def run(context, options = None):

	os.mkdir(context[KEY_OUT][KEY_STYLES])

	suffix_list = ['css', 'sass', 'scss']

	file_list = []
	for suffix in suffix_list:
		file_list.extend(glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '*.%s' % suffix)))

	for src_file_path in file_list:

		fn = os.path.basename(src_file_path)

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		with open(os.path.join(context[KEY_OUT][KEY_STYLES], fn), 'w') as f:
			f.write(cnt)
