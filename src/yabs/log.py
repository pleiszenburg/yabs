# -*- coding: utf-8 -*-


from functools import partial
import inspect
import logging
import os


class log_class:


	def __log__(self, level, msg):

		plugin_name = os.path.basename(inspect.getframeinfo(inspect.stack()[1][0]).filename)[:-3]
		logging.log(
			getattr(logging, level.upper()),
			'"%s": %s' % (plugin_name, msg)
			)


	def __getattr__(self, name):

		if name not in ['info', 'debug', 'warning', 'error', 'critical']:
			raise AttributeError()
		return partial(self.__log__, name)


log = log_class()
