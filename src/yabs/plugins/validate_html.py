# -*- coding: utf-8 -*-


import io
import os
import sys
import zipfile


import requests


from yabs.const import KEY_UPDATE


BIN_FLD = 'bin'
DIST_FLD = 'dist'
SHARE_FLD = 'share'
VALIDATOR_FN = 'vnu.jar'
VERSION_FN = '.vnu_version'


def update_validator(context):

	latest_dict = requests.get(
		url = 'https://api.github.com/repos/validator/validator/releases/latest'
		).json()
	latest_version = latest_dict['tag_name']

	version_file_path = os.path.join(os.environ['VIRTUAL_ENV'], SHARE_FLD, VERSION_FN)

	if os.path.isfile(version_file_path):
		with open(version_file_path, 'r') as f:
			current_version = f.read().strip()
		if current_version == latest_version:
			sys.stdout.write('validator up to date ... ')
			sys.stdout.flush()
			return

	sys.stdout.write('updating validator ... ')
	sys.stdout.flush()

	latest_url = None
	for item in latest_dict['assets']:
		if item['name'].startswith(VALIDATOR_FN) and item['name'].endswith('.zip'):
			latest_url = item['browser_download_url']
	if latest_url is None:
		raise # TODO

	latest_zip_bin = requests.get(latest_url, stream = True)

	validator_path = os.path.join(os.environ['VIRTUAL_ENV'], BIN_FLD, VALIDATOR_FN)
	if os.path.isfile(validator_path):
		os.unlink(validator_path)

	with zipfile.ZipFile(io.BytesIO(latest_zip_bin.content)) as z:
		with open(validator_path, 'wb') as f:
			f.write(z.read(os.path.join(DIST_FLD, VALIDATOR_FN)))

	with open(version_file_path, 'w+') as f:
		f.write(latest_version)


def run(context, options = None):

	if options[KEY_UPDATE]:
		update_validator(context)
