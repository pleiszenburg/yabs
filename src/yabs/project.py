# -*- coding: utf-8 -*-


import importlib.util
import logging
import os
import sys
import time


from .const import (
	KEY_CWD,
	KEY_LOG,
	KEY_OUT,
	KEY_PROJECT,
	KEY_RECIPE,
	KEY_ROOT,
	KEY_SERVER,
	KEY_SRC,
	KEY_TIMER
	)


class PluginNotFound(Exception):

	pass


class project_class:


	def __init__(self, context):

		self.context = context
		self.context[KEY_PROJECT] = self
		self.context[KEY_TIMER] = timer_class()

		for group_id in [KEY_SRC, KEY_OUT]:
			self.__compile_paths__(group_id)
		self.context[KEY_LOG] = os.path.abspath(os.path.join(self.context[KEY_CWD], self.context[KEY_LOG]))


	def __init_logger__(self, logger_name = None, logger_level = logging.INFO):

		logging.basicConfig(
			filename = os.path.join(self.context[KEY_LOG], logger_name) if logger_name is not None else None,
			level = logger_level,
			format = '[%(asctime)s %(levelname)s] %(message)s',
			datefmt = '%H:%M:%S'
			)


	def __compile_paths__(self, group_id):

		group_root_key = '%s_%s' % (group_id, KEY_ROOT)

		for path_id in self.context[group_id]:
			self.context[group_id][path_id] = os.path.abspath(os.path.join(
				self.context[KEY_CWD], self.context[group_root_key], self.context[group_id][path_id]
				))

		self.context[group_id][KEY_ROOT] = os.path.abspath(os.path.join(self.context[KEY_CWD], self.context[group_root_key]))
		self.context.pop(group_root_key)


	def __get_plugin__(self, plugin_name):

		for pattern in ['yabs.plugins.%s', '%s']:
			try:
				return importlib.import_module(pattern % plugin_name)
			except ModuleNotFoundError as e:
				pass

		raise PluginNotFound('"%s": Plugin not found!' % plugin_name)


	def build(self):

		self.__init_logger__()

		for step in self.context[KEY_RECIPE]:

			if isinstance(step, str):
				plugin_name = step
				plugin_options = None
			elif isinstance(step, dict) and len(list(step.keys())) == 1:
				plugin_name = list(step.keys())[0]
				plugin_options = step[plugin_name]

			self.run_plugin(plugin_name, plugin_options)


	def run(self, plugin_list):

		self.__init_logger__()

		for plugin_name in plugin_list:

			self.run_plugin(plugin_name, None)


	def run_plugin(self, plugin_name, plugin_options):

		try:
			plugin = self.__get_plugin__(plugin_name)
		except PluginNotFound as e:
			logging.error(str(e))
			return

		self.context[KEY_TIMER]()

		logging.info('"%s": Running ...' % plugin_name)

		os.chdir(self.context[KEY_CWD])

		ret = plugin.run(self.context, plugin_options)

		logging.info('"%s": Done in %.2f sec.' % (
			plugin_name, self.context[KEY_TIMER]()[1]
			))

		return ret


	def serve(self):

		self.__init_logger__(KEY_SERVER)

		self.run_plugin(KEY_SERVER, self.context[KEY_SERVER])


class timer_class:


	def __init__(self):

		self.start = time.time()
		self.last = self.start


	def __call__(self):

		current = time.time() - self.start
		diff = current - self.last
		self.last = current
		return current, diff
