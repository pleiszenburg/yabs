# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/__init__.py: Package root

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

import importlib.util
from logging import getLogger
import os
from types import ModuleType
from typing import Dict, List, Union

from typeguard import typechecked

from .abc import ProjectABC
from .const import (
    KEY_CWD,
    KEY_DEPLOY,
    KEY_LOG,
    KEY_MOUNTPOINT,
    KEY_OUT,
    KEY_PROJECT,
    KEY_RECIPE,
    KEY_ROOT,
    KEY_SERVER,
    KEY_SRC,
    KEY_TARGET,
    KEY_TIMER,
    LOGGER,
)
from .error import PluginNotFound
from .timer import Timer

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Project(ProjectABC):
    """
    Website project. Core class of YABS.

    Mutable.
    """

    def __init__(self, context: Dict):

        self._context = context

        self._context[KEY_PROJECT] = self
        self._context[KEY_TIMER] = Timer()

        self._log = getLogger(LOGGER)

        for group_id in [KEY_SRC, KEY_OUT]:
            self._compile_paths(group_id)
        self._context[KEY_LOG] = os.path.abspath(
            os.path.join(self._context[KEY_CWD], self._context[KEY_LOG])
        )
        self._context[KEY_DEPLOY][KEY_MOUNTPOINT] = os.path.abspath(
            os.path.join(
                self._context[KEY_CWD], self._context[KEY_DEPLOY][KEY_MOUNTPOINT]
            )
        )

    def _compile_paths(self, group_id: str):

        group_root_key = "%s_%s" % (group_id, KEY_ROOT)

        for path_id in self._context[group_id]:
            self._context[group_id][path_id] = os.path.abspath(
                os.path.join(
                    self._context[KEY_CWD],
                    self._context[group_root_key],
                    self._context[group_id][path_id],
                )
            )

        self._context[group_id][KEY_ROOT] = os.path.abspath(
            os.path.join(self._context[KEY_CWD], self._context[group_root_key])
        )
        self._context.pop(group_root_key)

    def _get_plugin(self, plugin_name: str) -> ModuleType:

        try:
            return importlib.import_module(f"yabs.plugins.{plugin_name:s}")
        except ModuleNotFoundError as err:
            raise PluginNotFound(f'"{plugin_name:s}": Plugin not found!') from err

    def build(self):

        for step in self._context[KEY_RECIPE]:

            if isinstance(step, str):
                plugin_name = step
                plugin_options = None
            elif isinstance(step, dict) and len(list(step.keys())) == 1:
                plugin_name = list(step.keys())[0]
                plugin_options = step[plugin_name]

            self.run_plugin(plugin_name, plugin_options)

    def deploy(self, target: str):

        self._context[KEY_DEPLOY][KEY_TARGET] = target
        self.run_plugin(KEY_DEPLOY, self._context[KEY_DEPLOY])

    def run(self, plugin_list: List[str]):

        for plugin_name in plugin_list:

            self.run_plugin(plugin_name, None)

    def run_plugin(self, plugin_name: str, plugin_options: Union[Dict, None] = None):

        try:
            plugin = self._get_plugin(plugin_name)
        except PluginNotFound as e:
            self._log.error(str(e))
            return

        self._context[KEY_TIMER]()

        self._log.info('"%s": Running ...', plugin_name)

        os.chdir(self._context[KEY_CWD])

        plugin.run(self._context, plugin_options)

        self._log.info(
            '"%s": Done in %.2f sec.', plugin_name, self._context[KEY_TIMER]()[1]
        )

    def serve(self):

        self.run_plugin(KEY_SERVER, self._context[KEY_SERVER])
