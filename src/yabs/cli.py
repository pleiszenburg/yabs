# -*- coding: utf-8 -*-


import os

import click
from daemonocle.cli import DaemonCLI

from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

from .const import (
	CONFIG_FILE,
	KEY_CWD,
	PID_FN
	)
from .project import project_class


def __get_project__():

	with open(CONFIG_FILE, 'r') as f:
		config = load(f.read(), Loader = Loader)
	config[KEY_CWD] = os.path.abspath(os.getcwd())

	return project_class(config)


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

	__get_project__().build()


@yabs_cli.command()
@click.argument('plugins', nargs = -1)
def run(plugins):
	"""YABS run

	Runs any given plugin or list of plugins with default options
	"""

	__get_project__().run(plugins)


@yabs_cli.command(cls = DaemonCLI,
	daemon_params = {
		'workdir': os.getcwd(),
		'pidfile': os.path.join(os.getcwd(), PID_FN)
		})
def server():
	"""YABS server

	Serves website via HTTP (default server plugin)
	"""

	__get_project__().serve()
