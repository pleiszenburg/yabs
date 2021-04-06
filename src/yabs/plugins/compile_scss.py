# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compile_scss.py: Compiles SCSS and SASS down to CSS

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

import sass
from typeguard import typechecked

from ..const import KEY_COLORS, KEY_OUT, KEY_SRC, KEY_STYLES, LOGGER

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

STYLE_SASS = "sass"
STYLE_SCSS = "scss"
STYLE_SUFFIX_LIST = [STYLE_SASS, STYLE_SCSS]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: None = None):

    colors = "\n".join([
        f"${name:s}: rgb({r:d}, {g:d}, {b:d})"
        for name, (r, g, b) in context[KEY_COLORS].items()
    ])

    suffixes = ("sass", "scss")

    files = []
    for suffix in suffixes:
        files.extend(
            glob.glob(os.path.join(context[KEY_OUT][KEY_STYLES], f"*.{suffix}"))
        )

    _log.debug('Inlcuding from %s', context[KEY_SRC][KEY_STYLES])

    for path in files:

        with open(path, "r", encoding = "utf-8") as f:
            cnt = f.read()
        os.unlink(path)

        cnt = sass.compile(
            string = f"{colors:s}\n{cnt:s}",
            output_style = "compact",
            indented = path.endswith(STYLE_SASS),
            include_paths = [context[KEY_SRC][KEY_STYLES]],
        )

        for suffix in suffixes:
            if path.endswith(suffix):
                path = path[: -1 * len(suffix)] + "css"
                break

        with open(path, "w", encoding = "utf-8") as f:
            f.write(cnt)
