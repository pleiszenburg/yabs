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

from datetime import timezone
import glob
from logging import getLogger
import os
from typing import Dict, Generator

from typeguard import typechecked

from ..const import (
    KEY_CTIME,
    KEY_EXTENDS,
    KEY_EXTENSION,
    KEY_HTML,
    KEY_MTIME,
    KEY_OUT,
    KEY_PLACEHOLDER,
    KEY_PREFIX,
    KEY_ROOT,
    KEY_SRC,
    KEY_STAGING,
    KEY_TEMPLATE,
    LOGGER,
)
from ..times import (
    get_fs_ctime,
    get_fs_mtime,
    get_git_ctime,
    get_git_mtime,
    NoGitTime,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _find_files(context: Dict) -> Generator[str, None, None]:

    for src in (KEY_HTML, KEY_STAGING):
        for ext in ('htm', 'svg'):
            yield from glob.glob(
                os.path.join(context[KEY_SRC][src], "**", f"*.{ext:s}*"),
                recursive = True,
            )

@typechecked
def run(context: Dict, options: Dict):

    for path in _find_files(context):

        with open(path, "r", encoding = "utf-8") as f:
            raw = f.read()

        try:
            ctime = get_git_ctime(path).astimezone(timezone.utc).isoformat()
        except NoGitTime:
            if not path.startswith(os.path.abspath(context[KEY_SRC][KEY_STAGING])):
                _log.info(f'not git ctime: {path:s}')
            ctime = get_fs_ctime(path).astimezone(timezone.utc).isoformat()

        try:
            mtime = get_git_mtime(path).astimezone(timezone.utc).isoformat()
        except NoGitTime:
            if not path.startswith(os.path.abspath(context[KEY_SRC][KEY_STAGING])):
                _log.info(f'not git mtime: {path:s}')
            mtime = get_fs_mtime(path).astimezone(timezone.utc).isoformat()

        if ctime > mtime:
            raise ValueError('ctime > mtime', path)

        fn = os.path.basename(path)

        for a, b in (
            (options.get(KEY_CTIME, None), ctime),
            (options.get(KEY_MTIME, None), mtime),
        ):
            if a is None:
                continue
            raw = raw.replace(a, b)

        if options[KEY_PLACEHOLDER] not in raw:

            with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), "w", encoding = "utf-8") as f:
                f.write(raw)

            continue

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
