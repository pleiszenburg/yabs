# -*- coding: utf-8 -*-


import importlib.util
import os
from pprint import pprint as pp


class project_class:


	def __init__(self, **config):

		self.config = config
		self.config['context'] = self


	def build(self):

		for step in self.config['recipe']:

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
