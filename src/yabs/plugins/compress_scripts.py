# -*- coding: utf-8 -*-


import glob
import os
import subprocess


from bs4 import BeautifulSoup


from yabs.const import (
	KEY_OUT,
	KEY_ROOT,
	KEY_SCRIPTS
	)


def compress_scripts(cnt):

	proc = subprocess.Popen(
		['uglifyjs', '--compress', '--mangle'],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		)
	out, err = proc.communicate(
		input = cnt.encode(encoding = 'UTF-8')
		)

	if err.decode(encoding = 'UTF-8').strip() != '':
		print(err.decode(encoding = 'UTF-8'))

	return out.decode(encoding = 'UTF-8')


def compress_scripts_file(file_path):

	with open(file_path, 'r') as f:
		cnt = f.read()

	cnt = compress_scripts(cnt)

	with open(file_path, 'w') as f:
		f.write(cnt)


def compress_scripts_in_html_file(file_path):

	with open(file_path, 'r') as f:
		cnt = f.read()

	soup = BeautifulSoup(cnt, 'html.parser')
	for uncompressed_tag in soup.find_all('script'):
		if uncompressed_tag.has_attr('src'):
			continue
		uncompressed_str = uncompressed_tag.decode_contents()
		compressed_str = compress_scripts(uncompressed_str)
		cnt = cnt.replace(uncompressed_str, compressed_str)

	with open(file_path, 'w') as f:
		f.write(cnt)


def run(context, options = None):

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], '*.js')):
		compress_scripts_file(file_path)

	for file_path in glob.iglob(os.path.join(context[KEY_OUT][KEY_ROOT], '**/*.htm*'), recursive = True):
		compress_scripts_in_html_file(file_path)
