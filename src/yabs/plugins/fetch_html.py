# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_html.py: Fetches HTML

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
from typing import Dict, List

from typeguard import typechecked

from yabs.const import (
    KEY_EXTENDS,
    KEY_EXTENSION,
    KEY_HTML,
    KEY_OUT,
    KEY_PLACEHOLDER,
    KEY_PREFIX,
    KEY_ROOT,
    KEY_SRC,
    KEY_STAGING,
    KEY_TEMPLATE,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _find_files(context: Dict) -> List[str]:

    files = []

    for src in (KEY_HTML, KEY_STAGING):
        for ext in ('htm', 'svg'):
            files.extend(glob.glob(
                os.path.join(context[KEY_SRC][src], "**", f"*.{ext:s}*"),
                recursive = True,
            ))

    return files

@typechecked
def run(context: Dict, options: Dict):

    for path in _find_files(context):

        with open(path, "r", encoding = "utf-8") as f:
            raw = f.read()

        fn = os.path.basename(path)

        if options[KEY_PLACEHOLDER] in raw:
            for extends in options[KEY_EXTENDS]:

                cnt = raw.replace(options[KEY_PLACEHOLDER], extends[KEY_TEMPLATE])

                extension = extends.get(KEY_EXTENSION, 'htm')

                extension_placeholder = options.get(KEY_EXTENSION, None)
                if extension_placeholder is not None:
                    cnt = cnt.replace(extension_placeholder, extension)

                extended_fn = f"{extends.get(KEY_PREFIX, ''):s}{fn.rsplit('.', 1)[0]:s}.{extension:s}"

                with open(
                    os.path.join(context[KEY_OUT][KEY_ROOT], extended_fn),
                    "w",
                    encoding = "utf-8",
                ) as f:
                    f.write(cnt)
        else:
            with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), "w", encoding = "utf-8") as f:
                f.write(raw)
