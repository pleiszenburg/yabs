# -*- coding: utf-8 -*-

import os

import click

from yaml import load, dump
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

from .const import CONFIG_FILE
from .project import project_class

@click.command()
def yabs_cli():

	with open(CONFIG_FILE, 'r') as f:
		config = load(f.read(), Loader = Loader)
	config['cwd'] = os.getcwd()

	print(config)
