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

from datetime import datetime
import glob
from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict, List, Optional

from typeguard import typechecked

from yabs.const import (
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

class NoGitTime(Exception):
    pass

_log = getLogger(LOGGER)

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
def _iso2dt(raw: str) -> datetime:
    raw = raw.replace(' ', 'T', 1).replace(' ', '')
    return datetime.fromisoformat(f'{raw[:-2]:s}:{raw[-2:]:s}')

@typechecked
def _get_git_ctime(fn: str) -> Optional[datetime]:
    proc = Popen([
        'git',
        'log',
        '--diff-filter=A',
        '--follow',
        r'--format=%ci',
        '-1',
        '--',
        fn,
    ], stdout = PIPE)
    out, _ = proc.communicate()
    if len(out.strip()) == 0:
        raise NoGitTime('failed to retrieve git ctime')
    return _iso2dt(out.decode('utf-8').strip())

@typechecked
def _get_git_mtime(fn: str) -> Optional[datetime]:
    proc = Popen([
        'git',
        'log',
        '-1',
        r'--pretty=%ci',
        fn,
    ], stdout = PIPE)
    out, _ = proc.communicate()
    if len(out.strip()) == 0:
        raise NoGitTime('failed to retrieve git mtime')
    return _iso2dt(out.decode('utf-8').strip())

@typechecked
def run(context: Dict, options: Dict):

    for path in _find_files(context):

        with open(path, "r", encoding = "utf-8") as f:
            raw = f.read()

        try:
            ctime = _get_git_ctime(path)
        except NoGitTime:
            if not path.startswith(os.path.abspath(context[KEY_SRC][KEY_STAGING])):
                _log.info(f'not git ctime: {path:s}')
            ctime = datetime.fromtimestamp(os.stat(path).st_ctime)

        try:
            mtime = _get_git_mtime(path)
        except NoGitTime:
            if not path.startswith(os.path.abspath(context[KEY_SRC][KEY_STAGING])):
                _log.info(f'not git mtime: {path:s}')
            mtime = datetime.fromtimestamp(os.stat(path).st_mtime)

        ctime, mtime = ctime.isoformat(), mtime.isoformat()

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
