# -*- coding: utf-8 -*-


import importlib.util
import os

from .const import (
	KEY_CONTEXT,
	KEY_CWD,
	KEY_RECIPE
	)


class project_class:


	def __init__(self, **config):

		self.config = config
		self.config[KEY_CONTEXT] = self


	def build(self):

		for step in self.config[KEY_RECIPE]:

			os.chdir(self.config[KEY_CWD])

			try:

				plugin_spec = importlib.util.spec_from_file_location(
					'plugins.%s' % step, os.path.join(os.path.dirname(__file__), 'plugins/%s.py' % step)
					)
				plugin = importlib.util.module_from_spec(plugin_spec)
				plugin_spec.loader.exec_module(plugin)

			except FileNotFoundError:

				print('Plugin "%s" not found!' % step)
				continue

			current_plugin = plugin.plugin(**self.config)
			current_plugin.run()
			del current_plugin
