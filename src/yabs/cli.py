# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/cli.py: Command line interface

    Copyright (C) 2018-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/yabs/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

import click
from daemonocle.cli import DaemonCLI

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .const import CONFIG_FILE, KEY_CWD, PID_FN
from .project import Project

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def _get_project():

    with open(CONFIG_FILE, "r") as f:
        config = load(f.read(), Loader=Loader)
    config[KEY_CWD] = os.path.abspath(os.getcwd())

    return Project(config)


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

    _get_project().build()


@yabs_cli.command()
@click.argument("target", nargs=1)
def deploy(target):
    """YABS build

	Deploy website to target
	"""

    _get_project().deploy(target)


@yabs_cli.command()
@click.argument("plugins", nargs=-1)
def run(plugins):
    """YABS run

	Runs any given plugin or list of plugins with default options
	"""

    _get_project().run(plugins)


@yabs_cli.command(
    cls=DaemonCLI,
    daemon_params={
        "work_dir": os.getcwd(),
        "pid_file": os.path.join(os.getcwd(), PID_FN),
    },
)
def server():
    """YABS server

	Serves website via HTTP (default server plugin)
	"""

    _get_project().serve()
