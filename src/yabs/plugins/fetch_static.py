# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_fonts.py: Fetches static files

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
from shutil import copytree
from typing import Dict, Union

from typeguard import typechecked

from ..const import KEY_STATIC, KEY_OUT, KEY_SRC, KEY_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Union[Dict, None] = None):

    if options is None:
        options = {}

    src_path = options.get(
        KEY_SRC,
        context[KEY_SRC][KEY_STATIC],
    )
    out_root = context[f'{KEY_OUT:s}_{KEY_ROOT:s}']

    try:
        out_path = os.path.join(out_root, options[KEY_OUT])
    except KeyError:
        out_path = context[KEY_OUT][KEY_STATIC]

    copytree(
        src = src_path,
        dst = out_path,
        dirs_exist_ok = True,
    )
