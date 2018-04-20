# -*- coding: utf-8 -*-


import glob
import os


from bs4 import BeautifulSoup
import csscompressor


from yabs.const import (
	KEY_OUT,
	KEY_ROOT,
	KEY_STYLES
	)


def compress_css(cnt):

	return csscompressor.compress(cnt)


def compress_css_file(file_path):

	with open(file_path, 'r') as f:
		cnt = f.read()

	cnt = compress_css(cnt)

	with open(file_path, 'w') as f:
		f.write(cnt)


def compress_css_in_html_file(file_path):

	with open(file_path, 'r') as f:
		cnt = f.read()

	soup = BeautifulSoup(cnt, 'html.parser')
	for uncompressed_tag in soup.find_all('style'):
		uncompressed_str = uncompressed_tag.decode_contents()
		compressed_str = compress_css(uncompressed_str)
		cnt = cnt.replace(uncompressed_str, compressed_str)

	with open(file_path, 'w') as f:
		f.write(cnt)


def run(context):

	for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], '*.css')):
		compress_css_file(file_path)

	for file_path in glob.iglob(os.path.join(context[KEY_OUT][KEY_ROOT], '**/*.htm*'), recursive = True):
		compress_css_in_html_file(file_path)
