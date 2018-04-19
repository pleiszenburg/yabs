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

# @click.command()

@click.group()
def yabs_cli():
	"""YABS

	Yet Another Build System
	"""
	pass


@yabs_cli.command()
def build():

	with open(CONFIG_FILE, 'r') as f:
		config = load(f.read(), Loader = Loader)
	config['cwd'] = os.getcwd()

	current_project = project_class(**config)
	current_project.build()
