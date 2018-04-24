# -*- coding: utf-8 -*-


import glob
import os


import jinja2


from yabs.const import (
	KEY_JINJA,
	KEY_HTML,
	KEY_SRC,
	KEY_TEMPLATES
	)


def run(context, options = None):

	context[KEY_JINJA] = jinja2.Environment(
		loader = jinja2.ChoiceLoader([
			jinja2.FileSystemLoader(context[KEY_SRC][path_key], encoding = 'utf-8', followlinks = False) for path_key in [KEY_TEMPLATES, KEY_HTML]
			]),
		autoescape = jinja2.select_autoescape(['html', 'xml'])
		)
	context[KEY_TEMPLATES] = {
		name.rsplit('.', 1)[0]: context[KEY_JINJA].get_template(name) for name in [
			os.path.basename(fn) for fn in glob.glob(os.path.join(context[KEY_SRC][KEY_TEMPLATES], '*')) if os.path.isfile(fn)
			]
		}
