# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/include_svgcss.py: Include external CSS into SVG files

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
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from typeguard import typechecked

from ..const import (
    KEY_DELETE,
    KEY_OUT,
    KEY_ROOT,
    KEY_STYLES,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _include_css_in_svg_file(path: str, context: Dict) -> List[str]:

    included = []

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    soup = BeautifulSoup(cnt, "xml")

    for uncompressed_tag in soup.find_all("style"):

        raw = uncompressed_tag.decode_contents()
        fn = raw.strip()  # potential file name

        if '\n' in fn or '{' in fn:
            continue
        fn = os.path.join(context[KEY_OUT][KEY_STYLES], fn)
        if not os.path.exists(fn.strip()):
            continue
        with open(fn, mode = 'r', encoding='utf-8') as f:
            css = f.read()
        included.append(fn)

        cnt = cnt.replace(raw, css)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)

    return included

@typechecked
def run(context: Dict, options: Optional[Dict] = None):

    if options is None:
        options = {}

    included = []

    for file_path in glob.iglob(
        os.path.join(context[KEY_OUT][KEY_ROOT], "**/*.svg*"), recursive=True
    ):
        included.extend(_include_css_in_svg_file(file_path, context))

    if not options.get(KEY_DELETE, False):
        return

    print(included)
    for fn in set(included):
        os.unlink(fn)
