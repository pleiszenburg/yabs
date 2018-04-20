# -*- coding: utf-8 -*-


import glob
import os


import jinja2


from yabs.const import (
	FLD_STYLES,
	KEY_OUTPUT,
	KEY_PATHS,
	KEY_STYLES
	)


def run(context):

	os.mkdir(os.path.join(context[KEY_PATHS][KEY_OUTPUT], FLD_STYLES))

	for src_file_path in glob.glob(os.path.join(context[KEY_PATHS][KEY_STYLES], '*.css')):

		fn = os.path.basename(src_file_path)

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		with open(os.path.join(context[KEY_PATHS][KEY_OUTPUT], FLD_STYLES, fn), 'w') as f:
			f.write(cnt)
