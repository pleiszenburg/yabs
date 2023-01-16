# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/times.py: Get ctime/mtime from git and/or file system

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
from logging import getLogger
import os
from subprocess import Popen, PIPE

from typeguard import typechecked

from .const import LOGGER

class NoGitTime(Exception):
    pass

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@typechecked
def _iso2dt(raw: str) -> datetime:
    raw = raw.replace(' ', 'T', 1).replace(' ', '')
    return datetime.fromisoformat(f'{raw[:-2]:s}:{raw[-2:]:s}')

@typechecked
def get_git_ctime(fn: str) -> datetime:

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
def get_git_mtime(fn: str) -> datetime:

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
def get_fs_ctime(fn: str) -> datetime:

    return datetime.fromtimestamp(os.stat(fn).st_ctime)

@typechecked
def get_fs_mtime(fn: str) -> datetime:

    return datetime.fromtimestamp(os.stat(fn).st_mtime)
