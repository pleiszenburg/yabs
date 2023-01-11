# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/compress_scripts.py: Compresses JavaScript

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

from concurrent.futures import ThreadPoolExecutor
import glob
from multiprocessing import cpu_count
from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict

from bs4 import BeautifulSoup
from typeguard import typechecked

from yabs.const import KEY_OUT, KEY_ROOT, KEY_SCRIPTS, LOGGER

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _compress_scripts(cnt: str) -> str:

    proc = Popen(
        ["uglifyjs", "--compress", "--mangle"],
        stdin = PIPE,
        stdout = PIPE,
        stderr = PIPE,
    )
    out, err = proc.communicate(input = cnt.encode(encoding="UTF-8"))

    if err.decode(encoding="UTF-8").strip():
        _log.error(err.decode(encoding="UTF-8"))
    if proc.returncode != 0:
        raise SystemError("uglifyjs failed", err.decode(encoding="UTF-8"))

    return out.decode(encoding="UTF-8")


@typechecked
def _compress_scripts_file(path: str):

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    cnt = _compress_scripts(cnt)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)


@typechecked
def _compress_scripts_in_html_file(path: str):

    with open(path, "r", encoding = "utf-8") as f:
        cnt = f.read()

    soup = BeautifulSoup(cnt, "html.parser")
    for uncompressed_tag in soup.find_all("script"):
        if uncompressed_tag.has_attr("src"):
            continue
        uncompressed_str = uncompressed_tag.decode_contents()
        compressed_str = _compress_scripts(uncompressed_str).strip()
        cnt = cnt.replace(uncompressed_str, compressed_str)

    with open(path, "w", encoding = "utf-8") as f:
        f.write(cnt)


@typechecked
def run(context: Dict, options: None = None):

    with ThreadPoolExecutor(max_workers = cpu_count()) as pool:

        for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], "*.js")):
            pool.submit(_compress_scripts_file, file_path)

        for file_path in glob.iglob(
            os.path.join(context[KEY_OUT][KEY_ROOT], "**/*.htm*"), recursive=True
        ):
            pool.submit(_compress_scripts_in_html_file, file_path)
