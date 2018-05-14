# -*- coding: utf-8 -*-


import json
import glob
import os


from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


from yabs.const import (
	KEY_DATA,
	KEY_SRC
	)


def load_data_file(file_path):

	fn = os.path.basename(file_path)
	data_key, file_type = fn.rsplit('.')

	with open(file_path, 'r') as f:
		data = f.read()

	if file_type == 'yaml':
		return data_key, load(data, Loader = Loader)
	elif file_type == 'json':
		return data_key, json.loads(data)
	else:
		raise # TODO


def run(context, options = None):

	data_dict = {}

	for file_path in glob.iglob(os.path.join(context[KEY_SRC][KEY_DATA], '**/*.*'), recursive = True):
		data_key, data_obj = load_data_file(file_path)
		data_dict[data_key] = data_obj

	context[KEY_DATA] = data_dict
