# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compile_cards.py: Generates Twitter cards and og images (LinkedIn ...)

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
import os
from typing import Callable, Dict

from typeguard import typechecked

from yabs.const import (
    KEY_DELETE,
    KEY_HEIGHT,
    KEY_OUT,
    KEY_PREFIX,
    KEY_RENDERER,
    KEY_ROOT,
    KEY_SVG,
    KEY_WIDTH,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _render_img(fn: str, delete: bool, renderer: Callable, width: int, height: int):

    out_fn = f"{fn.rsplit('.', 1)[0]:s}.png"
    renderer(
        src = fn,
        dest = out_fn,
        width = width,
        height = height,
    )
    if delete:
        os.unlink(fn)

@typechecked
def run(context: Dict, options: Dict):

    for fn in glob.glob(
        os.path.join(context[KEY_OUT][KEY_ROOT], "**", f"{options[KEY_PREFIX]:s}*.svg*"),
        recursive = True,
    ):
        _render_img(
            fn = fn,
            delete = options.get(KEY_DELETE, True),
            renderer = context[KEY_SVG][options[KEY_RENDERER]],
            width = options.get(KEY_WIDTH, 1200),
            height = options.get(KEY_HEIGHT, 600)
        )
