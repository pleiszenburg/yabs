# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_fonts.py: Fetches fonts

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
from typing import Dict

from typeguard import typechecked

from ..const import KEY_FONTS, KEY_OUT, KEY_SRC, FONT_SUFFIX_LIST

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: None = None):

    os.mkdir(context[KEY_OUT][KEY_FONTS])

    file_list = []
    for suffix in FONT_SUFFIX_LIST:
        file_list.extend(
            glob.glob(os.path.join(context[KEY_SRC][KEY_FONTS], f"*.{suffix:s}"))
        )

    for src_file_path in file_list:

        fn = os.path.basename(src_file_path)

        with open(src_file_path, "rb") as f:
            cnt_bin = f.read()

        with open(os.path.join(context[KEY_OUT][KEY_FONTS], fn), "wb") as f:
            f.write(cnt_bin)
