# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_library/main.py: Fetch library main

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
from typing import Dict

from typeguard import typechecked

from ...const import (
    FONT_SUFFIX_LIST,
    KEY_FONTS,
    KEY_GITHUB,
    KEY_NAME,
    KEY_LIBRARIES,
    KEY_OUT,
    KEY_SCRIPTS,
    KEY_SRC,
    KEY_STYLES,
    KEY_UPDATE,
    KEY_VERSION,
    LOGGER,
)
from .update import update_library

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Dict):

    name = options[KEY_NAME]
    github = options[KEY_GITHUB]
    version = options[KEY_VERSION]
    update = options[KEY_UPDATE]
    src = options[KEY_SRC]

    if update:
        update_library(
            name = name,
            github = github,
            library_path = context[KEY_SRC][KEY_LIBRARIES],
            src = src,
            version = version,
            font_path = context[KEY_OUT][KEY_FONTS],
            style_path = context[KEY_OUT][KEY_STYLES],
        )

    with open(
        os.path.join(context[KEY_SRC][KEY_LIBRARIES], name, f".{KEY_VERSION:s}"), "r", encoding = "utf-8",
    ) as f:
        current_version = f.read().strip()

    files = []
    for ext in ["css", "js"] + FONT_SUFFIX_LIST:
        files.extend(
            glob.glob(
                os.path.join(context[KEY_SRC][KEY_LIBRARIES], name, f"*.{ext:s}")
            )
        )

    for src_path in files:

        with open(src_path, "rb") as f:
            cnt = f.read()

        fn = os.path.basename(src_path).replace(
            f"-{current_version:s}.min.", ".min."
        )

        if fn.endswith(".css"):
            deployment_path = context[KEY_OUT][KEY_STYLES]
        elif fn.endswith(".js"):
            deployment_path = context[KEY_OUT][KEY_SCRIPTS]
        elif any(fn.endswith(f".{ext:s}") for ext in FONT_SUFFIX_LIST):
            deployment_path = context[KEY_OUT][KEY_FONTS]
        else:
            raise ValueError("unknown file extension")

        with open(os.path.join(deployment_path, fn), "wb") as f:
            f.write(cnt)
