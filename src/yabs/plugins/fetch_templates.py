# -*- coding: utf-8 -*-


import glob
import os
from pprint import pprint as pp


import jinja2


from yabs.const import (
	KEY_CWD,
	KEY_PATHS,
	KEY_TEMPLATES
	)


def run(context):

	jinja_env = jinja2.Environment(
		loader = jinja2.FileSystemLoader(
			context[KEY_PATHS][KEY_TEMPLATES], encoding = 'utf-8', followlinks = False
			),
		autoescape = jinja2.select_autoescape(['html', 'xml'])
		)
	context[KEY_TEMPLATES] = {
		name: jinja_env.get_template(name) for name in [
			os.path.basename(fn) for fn in glob.glob(os.path.join(context[KEY_PATHS][KEY_TEMPLATES], '*')) if os.path.isfile(fn)
			]
		}
