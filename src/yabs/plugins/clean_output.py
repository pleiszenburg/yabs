# -*- coding: utf-8 -*-

import os
from pprint import pprint as pp
import shutil


from yabs.const import (
	KEY_CWD,
	KEY_OUTPUT,
	KEY_PATHS
	)


class plugin:


	def __init__(self, **config):

		self.config = config


	def run(self):

		folder = os.path.join(self.config[KEY_CWD], self.config[KEY_PATHS][KEY_OUTPUT])

		for entry in os.listdir(folder):

			entry_path = os.path.join(folder, entry)

			if os.path.isfile(entry_path):
				os.unlink(entry_path)
			elif os.path.isdir(entry_path):
				shutil.rmtree(entry_path)
			else:
				raise # TODO
