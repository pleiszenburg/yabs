# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
	KEY_OUT,
	KEY_ROOT
	)


def run(context):

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '**/*.htm?')):

		with open(file_path, 'r') as f:
			cnt = f.read()

		print(cnt)

		with open(file_path, 'w') as f:
			f.write(cnt)
