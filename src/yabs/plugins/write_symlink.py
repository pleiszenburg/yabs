# -*- coding: utf-8 -*-


import os


from yabs.const import (
	KEY_OUT,
	KEY_ROOT,
	)


def run(context, options = None):

	for target_path in options.keys():
		os.symlink(
			os.path.join(context[KEY_OUT][KEY_ROOT], options[target_path]),
			os.path.join(context[KEY_OUT][KEY_ROOT], target_path)
			)
