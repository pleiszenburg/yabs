# -*- coding: utf-8 -*-


import glob
import os


import sass


from yabs.const import (
	KEY_OUT,
	KEY_ROOT
	)


def run(context, options = None):

	suffix_list = ['sass', 'scss']

	file_list = []
	for suffix in suffix_list:
		file_list.extend(glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '*.%s' % suffix)))

	for file_path in file_list:

		with open(file_path, 'r') as f:
			cnt = f.read()

		os.unlink(file_path)

		cnt = sass.compile(string = cnt)

		for suffix in suffix_list:
			if file_path.endswith(suffix):
				file_path = file_path[:-1 * len(suffix)] + 'css'
				break

		with open(file_path, 'w') as f:
			f.write(cnt)
