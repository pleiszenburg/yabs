# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compress_css.py: Compresses CSS

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

from bs4 import BeautifulSoup
import csscompressor
from typeguard import typechecked

from ..const import KEY_OUT, KEY_ROOT, KEY_STYLES

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _compress_css(cnt: str) -> str:

    return csscompressor.compress(cnt)


@typechecked
def _compress_css_file(path: str):

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    cnt = _compress_css(cnt)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)


@typechecked
def _compress_css_in_html_file(path: str):

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    if path.lower().endswith('svg'):
        soup = BeautifulSoup(cnt, "xml")
    else:
        soup = BeautifulSoup(cnt, "html.parser")

    for uncompressed_tag in soup.find_all("style"):
        uncompressed_str = uncompressed_tag.decode_contents()
        compressed_str = _compress_css(uncompressed_str)
        cnt = cnt.replace(uncompressed_str, compressed_str)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)


@typechecked
def run(context: Dict, options: None = None):

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_STYLES], "*.css")):
        _compress_css_file(file_path)

    for ext in ('htm', 'svg'):
        for file_path in glob.iglob(
            os.path.join(context[KEY_OUT][KEY_ROOT], f"**/*.{ext:s}*"), recursive=True
        ):
            _compress_css_in_html_file(file_path)
