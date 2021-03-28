## -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/include_scripts.py: Handles includes in JavaScript

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

import glob
from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict

from typeguard import typechecked

from ..const import KEY_OUT, KEY_SCRIPTS, LOGGER

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: None = None):

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], "*.js")):

        proc = Popen(
            ["browserify", file_path, "-o", file_path],
            stdout = PIPE,
            stderr = PIPE,
        )
        out, err = proc.communicate()

        if out.decode("utf-8").strip() != "":
            _log.info("browserify: %s", out.decode("utf-8"))
        if err.decode("utf-8").strip() != "":
            _log.error("browserify: %s", err.decode("utf-8"))
        if proc.returncode != 0:
            raise SystemError("browserify failed")
