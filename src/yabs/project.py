# -*- coding: utf-8 -*-


import importlib.util
import os


from .const import (
	KEY_CWD,
	KEY_OUT,
	KEY_PROJECT,
	KEY_RECIPE,
	KEY_ROOT,
	KEY_SRC
	)


class project_class:


	def __init__(self, context):

		self.context = context
		self.context[KEY_PROJECT] = self

		for group_id in [KEY_SRC, KEY_OUT]:
			self.__compile_paths__(group_id)


	def __compile_paths__(self, group_id):

		group_root_key = '%s_%s' % (group_id, KEY_ROOT)

		for path_id in self.context[group_id]:
			self.context[group_id][path_id] = os.path.abspath(os.path.join(
				self.context[KEY_CWD], self.context[group_root_key], self.context[group_id][path_id]
				))

		self.context[group_id][KEY_ROOT] = os.path.abspath(os.path.join(self.context[KEY_CWD], self.context[group_root_key]))
		self.context.pop(group_root_key)


	def build(self):

		for step in self.context[KEY_RECIPE]:

			os.chdir(self.context[KEY_CWD])

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
