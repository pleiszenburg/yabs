# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compile_favicon.py: Generates favicon images

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
from typing import Dict

from PIL import Image
from typeguard import typechecked

from yabs.const import (
    KEY_IMAGES,
    KEY_NAME,
    KEY_OUT,
    KEY_ROOT,
    KEY_SIZE,
    KEY_SRC,
    KEY_VARIANTS,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Dict):

    src = options[KEY_SRC]
    variants = options[KEY_VARIANTS]

    fn = os.path.join(context[KEY_OUT][KEY_IMAGES], src)

    favicon_base = Image.open(fn)
    favicon_base.load()
    os.unlink(fn)

    for variant in variants:

        path = os.path.join(context[KEY_OUT][KEY_ROOT], variant[KEY_NAME])

        if path.endswith('.ico'):

            favicon_base.save(
                path,
                sizes = [tuple(size) for size in variant[KEY_SIZE]],
            )

        else:

            favicon = favicon_base.resize(tuple(variant[KEY_SIZE]))
            favicon.save(path)
            favicon.close()

    favicon_base.close()
