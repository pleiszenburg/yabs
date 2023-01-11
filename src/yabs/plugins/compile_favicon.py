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
from typing import Callable, Dict, List, Optional, Union

from PIL import Image
from typeguard import typechecked

from yabs.const import (
    KEY_DELETE,
    KEY_IMAGES,
    KEY_NAME,
    KEY_OUT,
    KEY_RENDERER,
    KEY_ROOT,
    KEY_SIZE,
    KEY_SRC,
    KEY_SVG,
    KEY_VARIANTS,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _find_base(context: Dict, options: Dict) -> str:

    for key in (KEY_IMAGES, KEY_ROOT):
        fn = os.path.join(context[KEY_OUT][key], options[KEY_SRC])
        if os.path.exists(fn):
            return fn

    raise ValueError('no favicon base found')

@typechecked
def _import_img(fn: str, delete: bool, renderer: Optional[Callable] = None) -> Image:

    if fn.lower().endswith('.svg'):

        tmp_fn = f'{fn:s}_tmp.png'
        renderer(
            src = fn,
            dest = tmp_fn,
            width = 1024,
            height = 1024,
        )
        base = Image.open(tmp_fn)
        base.load()
        os.unlink(tmp_fn)

    else:

        base = Image.open(fn)
        base.load()

    if delete:
        os.unlink(fn)

    return base

@typechecked
def _export_img(fn: str, img: Image, sizes: Union[List[int], List[List[int]]]):

    if fn.lower().endswith('.ico'):
        img.save(
            fn,
            sizes = [tuple(size) for size in sizes],
        )
        return

    resized = img.resize(tuple(sizes))
    resized.save(fn)
    resized.close()

@typechecked
def run(context: Dict, options: Dict):

    renderer = None
    renderers = context.get(KEY_SVG, None)
    if renderers is not None:
        renderer = renderers.get(options.get(KEY_RENDERER, None), None)

    base = _import_img(
        fn = _find_base(context, options),
        delete = options.get(KEY_DELETE, True),
        renderer = renderer,
    )

    for variant in options[KEY_VARIANTS]:
        _export_img(
            fn = os.path.join(context[KEY_OUT][KEY_ROOT], variant[KEY_NAME]),
            img = base,
            sizes = variant[KEY_SIZE],
        )

    base.close()
