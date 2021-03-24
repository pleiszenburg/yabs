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
import logging
import os
from typing import Dict

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

        self.context = context
        self.context[KEY_PROJECT] = self
        self.context[KEY_TIMER] = Timer()

        for group_id in [KEY_SRC, KEY_OUT]:
            self.__compile_paths__(group_id)
        self.context[KEY_LOG] = os.path.abspath(
            os.path.join(self.context[KEY_CWD], self.context[KEY_LOG])
        )
        self.context[KEY_DEPLOY][KEY_MOUNTPOINT] = os.path.abspath(
            os.path.join(
                self.context[KEY_CWD], self.context[KEY_DEPLOY][KEY_MOUNTPOINT]
            )
        )

    def __init_logger__(self, logger_name=None, logger_level=logging.INFO):

        logging.basicConfig(
            filename=os.path.join(self.context[KEY_LOG], logger_name)
            if logger_name is not None
            else None,
            level=logger_level,
            format="[%(asctime)s %(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
        )

    def __compile_paths__(self, group_id):

        group_root_key = "%s_%s" % (group_id, KEY_ROOT)

        for path_id in self.context[group_id]:
            self.context[group_id][path_id] = os.path.abspath(
                os.path.join(
                    self.context[KEY_CWD],
                    self.context[group_root_key],
                    self.context[group_id][path_id],
                )
            )

        self.context[group_id][KEY_ROOT] = os.path.abspath(
            os.path.join(self.context[KEY_CWD], self.context[group_root_key])
        )
        self.context.pop(group_root_key)

    def __get_plugin__(self, plugin_name):

        for pattern in ["yabs.plugins.%s", "%s"]:
            try:
                return importlib.import_module(pattern % plugin_name)
            except ModuleNotFoundError:
                pass

        raise PluginNotFound('"%s": Plugin not found!' % plugin_name)

    def build(self):

        self.__init_logger__()

        for step in self.context[KEY_RECIPE]:

            if isinstance(step, str):
                plugin_name = step
                plugin_options = None
            elif isinstance(step, dict) and len(list(step.keys())) == 1:
                plugin_name = list(step.keys())[0]
                plugin_options = step[plugin_name]

            self.run_plugin(plugin_name, plugin_options)

    def deploy(self, target):

        self.__init_logger__(KEY_DEPLOY)

        self.context[KEY_DEPLOY][KEY_TARGET] = target
        self.run_plugin(KEY_DEPLOY, self.context[KEY_DEPLOY])

    def run(self, plugin_list):

        self.__init_logger__()

        for plugin_name in plugin_list:

            self.run_plugin(plugin_name, None)

    def run_plugin(self, plugin_name, plugin_options=None):

        try:
            plugin = self.__get_plugin__(plugin_name)
        except PluginNotFound as e:
            logging.error(str(e))
            return

        self.context[KEY_TIMER]()

        logging.info('"%s": Running ...' % plugin_name)

        os.chdir(self.context[KEY_CWD])

        ret = plugin.run(self.context, plugin_options)

        logging.info(
            '"%s": Done in %.2f sec.' % (plugin_name, self.context[KEY_TIMER]()[1])
        )

        return ret

    def serve(self):

        self.__init_logger__(KEY_SERVER)

        self.run_plugin(KEY_SERVER, self.context[KEY_SERVER])
