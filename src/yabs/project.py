# -*- coding: utf-8 -*-


import importlib.util
import os

from .const import (
	KEY_CWD,
	KEY_PATHS,
	KEY_PROJECT,
	KEY_RECIPE
	)


class project_class:


	def __init__(self, context):

		self.context = context
		self.context[KEY_PROJECT] = self


	def build(self):

		for step in self.context[KEY_RECIPE]:

			os.chdir(self.context[KEY_PATHS][KEY_CWD])

			try:

				plugin_spec = importlib.util.spec_from_file_location(
					'plugins.%s' % step, os.path.join(os.path.dirname(__file__), 'plugins/%s.py' % step)
					)
				plugin = importlib.util.module_from_spec(plugin_spec)
				plugin_spec.loader.exec_module(plugin)

			except FileNotFoundError:

				print('Plugin "%s" not found!' % step)
				continue

			plugin.run(self.context)
