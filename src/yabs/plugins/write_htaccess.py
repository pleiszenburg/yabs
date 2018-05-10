# -*- coding: utf-8 -*-


import os


from yabs.const import (
	KEY_OUT,
	KEY_ROOT,
	)


def run(context, options = None):

	with open(os.path.join(context[KEY_OUT][KEY_ROOT], '.htaccess'), 'w') as f:
		f.write(options)
