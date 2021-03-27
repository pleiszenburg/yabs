# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compress_html.py: Compresses HTML

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

from logging import getLogger
import glob
import os
from typing import Dict

import htmlmin
from typeguard import typechecked

from ..const import (
    AJAX_PREFIX,
    AJAX_SEPARATOR,
    KEY_OUT,
    KEY_ROOT,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _compress_html(content: str) -> str:

    return htmlmin.minify(
        content,
        remove_comments=True,
        remove_empty_space=True,
        remove_all_empty_space=False,
        reduce_empty_attributes=True,
        reduce_boolean_attributes=False,
        remove_optional_attribute_quotes=False,
        keep_pre=True,
        pre_tags=("pre", "textarea", "nomin"),
        pre_attr="pre",
    )


@typechecked
def _compress_html_file(path: str):

    _log.debug("Compressing %s", path)

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    fn = os.path.basename(path)

    if fn.startswith(AJAX_PREFIX) and AJAX_SEPARATOR in cnt:

        self_info_json, html_cnt = cnt.split(AJAX_SEPARATOR)
        cnt = "%s\n%s\n%s" % (
            self_info_json.strip(),
            AJAX_SEPARATOR,
            _compress_html(html_cnt),
        )

    else:

        cnt = _compress_html(cnt)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)


@typechecked
def run(context: Dict, options: None = None):

    for file_path in glob.iglob(
        os.path.join(context[KEY_OUT][KEY_ROOT], "**/*.htm*"), recursive=True
    ):
        _compress_html_file(file_path)
