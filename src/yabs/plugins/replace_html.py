# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/replace_html.py: Replace content in HTML files

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
import re
from subprocess import Popen
from tempfile import mkstemp
from typing import Dict

from typeguard import typechecked

from ..const import (
    KEY_JINJA,
    KEY_OUT,
    KEY_ROOT,
    KEY_SEQUENCES,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class _Replacer:

    def __init__(self, raw: str, old: str, new: str, node: str):

        self._raw = raw
        self._result = ''

        self._start = f'<{node:s}'
        self._end = f'</{node:s}>'
        self._use_node = False # self._start in self._raw and self._end in self._raw

        if self._use_node:
            self._before, tmp = self._raw.split(self._start, 1)
            self._relevant, self._after = tmp.split(self._end, 1)
            assert isinstance(self._before, str)
            assert isinstance(self._relevant, str)
            assert isinstance(self._after, str)
            assert self._relevant in self._raw
        else:
            self._before, self._after = '', ''
            self._relevant = self._raw

        self._relevant = self._replace(self._relevant, old, new)

        if self._use_node:
            self._result = f'{self._before:s}{self._start:s}{self._relevant:s}{self._end:s}{self._after:s}'
        else:
            self._result = self._relevant

    @staticmethod
    def _replace0(raw: str, old: str, new: str) -> str:
        return raw.replace(old, new)

    @staticmethod
    def _replace(raw: str, old: str, new: str) -> str:
        pattern = f'(?<!<[^>]*){old:s}(?<![^>]*<)'
        return re.sub(pattern, raw, new)

    @property
    def result(self) -> str:
        return self._result

    def diff(self):
        (_, a), (_, b) = mkstemp(), mkstemp()
        with open(a, mode = 'w', encoding = 'utf-8') as f:
            f.write(self._raw)
        with open(b, mode = 'w', encoding = 'utf-8') as f:
            f.write(self._result)
        proc = Popen(['git', '--no-pager', 'diff', '--no-index', a, b])
        proc.wait()
        os.unlink(a)
        os.unlink(b)


@typechecked
def run(context: Dict, options: Dict = None):

    if options is None:
        options = {}

    for file_path in glob.glob(
        os.path.join(context[KEY_OUT][KEY_ROOT], "**", "*.htm*"), recursive = True
    ):

        with open(os.path.join(file_path), "r", encoding = "utf-8") as f:
            cnt_before = f.read()

        if options['old'] not in cnt_before:
            cnt_after = cnt_before
        else:
            print( file_path, options['old'], options['new'], options['node'] )
            replacer = _Replacer(cnt_before, options['old'], options['new'], options['node'])
            replacer.diff()
            cnt_after = replacer.result

        with open(os.path.join(file_path), "w+", encoding = "utf-8") as f:
            f.write(cnt_after)
