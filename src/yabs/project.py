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
	KEY_SRC
	)


class project_class:


	def __init__(self, context):

		self.context = context
		self.context[KEY_PROJECT] = self

		for group_id in [KEY_SRC, KEY_OUT]:
			self.__compile_paths__(group_id)
		self.context[KEY_LOG] = os.path.abspath(os.path.join(self.context[KEY_CWD], self.context[KEY_LOG]))


	def __init_logger__(self, logger_name = None):

		logging.basicConfig(
			filename = os.path.join(self.context[KEY_LOG], logger_name) if logger_name is not None else None,
			level = logging.DEBUG,
			format = '%(asctime)s [%(levelname)s] %(message)s',
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

		try:

			plugin_spec = importlib.util.spec_from_file_location(
				'plugins.%s' % plugin_name,
				os.path.join(os.path.dirname(__file__), 'plugins/%s.py' % plugin_name)
				)
			plugin = importlib.util.module_from_spec(plugin_spec)
			plugin_spec.loader.exec_module(plugin)

		except FileNotFoundError:

			print('Plugin "%s" not found!' % plugin_name)
			return None

		return plugin


	def build(self):

		timer = timer_class()

		for step in self.context[KEY_RECIPE]:

			os.chdir(self.context[KEY_CWD])

			if isinstance(step, str):
				plugin_name = step
				plugin_options = None
			elif isinstance(step, dict) and len(list(step.keys())) == 1:
				plugin_name = list(step.keys())[0]
				plugin_options = step[plugin_name]

			plugin = self.__get_plugin__(plugin_name)

			sys.stdout.write('[%03.2f sec] Plugin "%s" ... ' % (timer()[0], plugin_name))
			sys.stdout.flush()

			plugin.run(self.context, plugin_options)

			sys.stdout.write('done in %.2f sec.\n' % timer()[1])
			sys.stdout.flush()


	def run(self, plugin_list):

		print(plugin_list)

		for plugin_name in plugin_list:

			plugin = self.__get_plugin__(plugin_name)

			plugin.run(self.context, options = None)


	def serve(self):

		self.__init_logger__(KEY_SERVER)
		server = self.__get_plugin__(KEY_SERVER)
		server.run(self.context, self.context[KEY_SERVER])


class timer_class:


	def __init__(self):

		self.start = time.time()
		self.last = self.start


	def __call__(self):

		current = time.time() - self.start
		diff = current - self.last
		self.last = current
		return current, diff
