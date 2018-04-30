# -*- coding: utf-8 -*-


import glob
import os


import sass


STYLE_SASS = 'sass'
STYLE_SCSS = 'scss'
STYLE_SUFFIX_LIST = [STYLE_SASS, STYLE_SCSS]


from yabs.const import (
	KEY_COLORS,
	KEY_OUT,
	KEY_STYLES
	)


def run(context, options = None):

	suffix_list = ['sass', 'scss']

	file_list = []
	for suffix in suffix_list:
		file_list.extend(glob.glob(os.path.join(context[KEY_OUT][KEY_STYLES], '*.%s' % suffix)))

	for file_path in file_list:

		with open(file_path, 'r') as f:
			cnt = f.read()

		cnt_color_list = []
		for color_index, color in enumerate(context[KEY_COLORS]):
			cnt_color_list.append('$color%d: rgb%s' % (color_index + 1, str(tuple(color))))
		cnt = '\n'.join(cnt_color_list) + '\n' + cnt
		print(cnt)

		os.unlink(file_path)

		cnt = sass.compile(
			string = cnt,
			output_style = 'compact',
			indented = file_path.endswith(STYLE_SASS)
			)

		for suffix in suffix_list:
			if file_path.endswith(suffix):
				file_path = file_path[:-1 * len(suffix)] + 'css'
				break

		with open(file_path, 'w') as f:
			f.write(cnt)
