# -*- coding: utf-8 -*-

import os

import click

from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

from .const import CONFIG_FILE
from .project import project_class

# @click.command()

@click.group()
def yabs_cli():
	"""YABS

	Yet Another Build System
	"""
	pass


@yabs_cli.command()
def build():
	"""YABS build

	Builds website from recipe
	"""

	with open(CONFIG_FILE, 'r') as f:
		config = load(f.read(), Loader = Loader)
	config['cwd'] = os.getcwd()

	current_project = project_class(**config)
	current_project.build()
