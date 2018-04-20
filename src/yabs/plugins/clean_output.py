# -*- coding: utf-8 -*-

import os
from pprint import pprint as pp
import shutil


from yabs.const import (
	KEY_OUTPUT,
	KEY_PATHS
	)


def run(context):

	for entry in os.listdir(context[KEY_PATHS][KEY_OUTPUT]):

		entry_path = os.path.join(context[KEY_PATHS][KEY_OUTPUT], entry)

		if os.path.isfile(entry_path):
			os.unlink(entry_path)
		elif os.path.isdir(entry_path):
			shutil.rmtree(entry_path)
		else:
			raise # TODO
