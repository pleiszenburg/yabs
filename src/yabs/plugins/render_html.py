# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/render_html.py: Renders HTML files

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

from ..const import (
    KEY_DOMAIN,
    KEY_JINJA,
    KEY_OUT,
    KEY_ROOT,
    KEY_SEQUENCES,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: None = None):

    for ext in ('htm', 'svg'):

        root_path = os.path.abspath(context[KEY_OUT][KEY_ROOT])
        shift = len(root_path)

        for file_path in glob.glob(
            os.path.join(root_path, "**", f"*.{ext:s}*"), recursive = True
        ):

            with open(os.path.join(file_path), "r", encoding = "utf-8") as f:
                cnt = f.read()

            og_url = f'https://{context[KEY_DOMAIN]:s}{file_path[shift:]:s}'

            cnt = context[KEY_JINJA].from_string(cnt).render(
                sequences = context.get(KEY_SEQUENCES, {}),
                og_url = og_url,
            )

            with open(os.path.join(file_path), "w+", encoding = "utf-8") as f:
                f.write(cnt)
