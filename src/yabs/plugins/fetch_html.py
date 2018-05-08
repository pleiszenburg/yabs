# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	AJAX_PREFIX,
	KEY_BASE,
	KEY_HTML,
	KEY_OUT,
	KEY_ROOT,
	KEY_SRC,
	TEMPLATE_PLACEHOLDER
	)


def run(context, options = None):

	for src_file_path in glob.glob(os.path.join(context[KEY_SRC][KEY_HTML], '**', '*.htm*'), recursive = True):

		fn = os.path.basename(src_file_path)

		with open(src_file_path, 'r') as f:
			cnt = f.read()

		if TEMPLATE_PLACEHOLDER in cnt:
			for prefix in ['', AJAX_PREFIX]:
				with open(os.path.join(context[KEY_OUT][KEY_ROOT], '%s%s' % (prefix, fn)), 'w') as f:
					f.write(cnt.replace(TEMPLATE_PLACEHOLDER, '%s%s' % (prefix, KEY_BASE)))
		else:
			with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), 'w') as f:
				f.write(cnt)
