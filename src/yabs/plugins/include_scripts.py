# -*- coding: utf-8 -*-


import glob
import os
import subprocess


from yabs.const import (
	KEY_OUT,
	KEY_SCRIPTS,
	KEY_SRC
	)


def run(context, options = None):

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], '*.js')):

		print(file_path)

		proc = subprocess.Popen(
			['browserify', file_path, '-o', file_path],
			stdout = subprocess.PIPE, stderr = subprocess.PIPE
			)
		_, _ = proc.communicate()
