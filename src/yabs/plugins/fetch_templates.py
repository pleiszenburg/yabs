# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


import jinja2


from yabs.const import (
	KEY_CONTEXT,
	KEY_CWD,
	KEY_PATHS,
	KEY_TEMPLATES
	)


class plugin:


	def __init__(self, config):

		self.config = config


	def run(self):

		template_path = os.path.join(self.config[KEY_PATHS][KEY_CWD], self.config[KEY_PATHS][KEY_TEMPLATES])
		jinja_env = jinja2.Environment(
			loader = jinja2.FileSystemLoader(
				template_path, encoding = 'utf-8', followlinks = False
				),
			autoescape = jinja2.select_autoescape(['html', 'xml'])
			)
		self.config[KEY_TEMPLATES] = {
			name: jinja_env.get_template(name) for name in [
				os.path.basename(fn) for fn in glob.glob(os.path.join(template_path, '*')) if os.path.isfile(fn)
				]
			}
