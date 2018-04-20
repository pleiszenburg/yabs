# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_HTML,
	KEY_JINJA,
	KEY_OUT,
	KEY_ROOT,
	KEY_SRC
	)


def run(context):

	for file_path in glob.glob(os.path.join(context[KEY_SRC][KEY_HTML], '*.htm?')):

		fn = os.path.basename(file_path)

		cnt = context[KEY_JINJA].get_template(fn).render()

		with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), 'w') as f:
			f.write(cnt)
