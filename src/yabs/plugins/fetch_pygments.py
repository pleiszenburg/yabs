# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_pygments.py: Fetches / generates pygments CSS

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

from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict

from typeguard import typechecked

from ..const import (
    KEY_NAME,
    KEY_OUT,
    KEY_STYLES,
    KEY_THEME,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Dict):

    theme = options[KEY_THEME]
    name = options[KEY_NAME]
    path = context[KEY_OUT][KEY_STYLES]

    proc = Popen([
        "pygmentize",
        "-S",
        theme,
        "-f",
        "html",
        "-a",
        f".{name:s}",
    ], stdout = PIPE, stderr = PIPE,)
    outs, errs = proc.communicate()

    if errs.decode("utf-8").strip() != "" or proc.returncode != 0:
        _log.error("pygmentize failed: %s", errs.decode("utf-8").strip())

    with open(
        os.path.join(path, f"{name:s}.css"),
        "w+",
        encoding = "utf-8",
    ) as f:
        f.write(outs.decode("utf-8"))
