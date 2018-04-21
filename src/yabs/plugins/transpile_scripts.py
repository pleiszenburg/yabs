# -*- coding: utf-8 -*-


import glob
import json
import os
import subprocess


from yabs.const import (
	KEY_OUT,
	KEY_SCRIPTS,
	KEY_SRC
	)


def run(context, options = None):

	babelrc_fn = '.babelrc'

	with open(babelrc_fn, 'w') as f:
		json.dump(options, f, indent = 4, sort_keys = True, separators=(',', ': '))

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], '*.js')):

		proc = subprocess.Popen(
			['babel', file_path, '-o', file_path],
			stdout = subprocess.PIPE, stderr = subprocess.PIPE
			)
		out, err = proc.communicate()

		if out.decode('utf-8').strip() != '':
			print(out.decode('utf-8'))
		if err.decode('utf-8').strip() != '':
			print(err.decode('utf-8'))

	os.unlink(babelrc_fn)
