# -*- coding: utf-8 -*-


from pprint import pprint as pp


class project_class:


	def __init__(self, **config):
		self.config = config

	def build(self):
		pp(self.config)
