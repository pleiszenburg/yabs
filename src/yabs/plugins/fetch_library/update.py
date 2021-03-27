# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_library/update.py: Library update

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

from distutils.version import StrictVersion
import fnmatch
import glob
import io
from logging import getLogger
import os
from pprint import pformat as pf
from typing import List
import zipfile

import requests
from typeguard import typechecked

from ...const import (
    KEY_RELEASE,
    KEY_TAGS,
    KEY_VERSION,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _get_latest_version(version: str, github: str) -> str:

    if version == KEY_RELEASE:

        return requests.get(
            url = f"https://api.github.com/repos/{github:s}/releases/latest"
        ).json()["name"][1:]

    if version != KEY_TAGS:
        raise ValueError(f'Unknown version method for library: {version:s}')

    tags = requests.get(
        url = f"https://api.github.com/repos/{github:s}/tags"
    ).json()
    try:
        versions = [
            tag["name"].lstrip("v")
            for tag in tags
            if not any(item in tag["name"] for item in (
                "-", "rc", "RC", "beta", "BETA", "alpha", "ALPHA", "dev", "DEV",
            ))
        ]
    except:
        _log.exception("Failed to parse version from Github response: %s", pf(tags))
        raise
    versions.sort(key = StrictVersion)

    return versions[-1]


@typechecked
def update_library(
    name: str,
    github: str,
    library_path: str,
    src: List[str],
    version: str,
    font_path: str,
    style_path: str,
):

    library_path = os.path.join(library_path, name)

    if os.path.exists(library_path) and not os.path.isdir(library_path):
        raise ValueError(f"library path does not point to directory: {library_path:s}")
    if not os.path.exists(library_path):
        os.mkdir(library_path)

    new_library_version = _get_latest_version(
        version = version,
        github = github,
    )

    version_file_path = os.path.join(library_path, f".{KEY_VERSION:s}")
    if os.path.isfile(version_file_path):
        with open(version_file_path, "r", encoding = "utf-8") as f:
            old_library_version = f.read().strip()
        if old_library_version == new_library_version:
            _log.debug(
                "Library %s up to date at version %s ...",
                name,
                old_library_version,
            )
            return

    _log.info(
        "Updating library %s from version %s to version %s ...",
        name,
        old_library_version,
        new_library_version,
    )

    for src_file_path in glob.glob(os.path.join(library_path, "*.*")):
        os.unlink(src_file_path) # Remove library files of previous versions

    with open(version_file_path, "w+", encoding = "utf-8") as f:
        f.write(new_library_version)

    for url_pattern in src:

        url = url_pattern % new_library_version

        if url.startswith("http"):

            fn = url.split("/")[-1].split("?")[0]
            if new_library_version not in fn:
                fn = fn.replace(".min", f"-{new_library_version:s}.min")
            cnt = requests.get(url).text
            if fn.endswith(".css"): # katex fix
                cnt = cnt.replace(
                    "url(font/",
                    f"url({os.path.relpath(font_path, style_path):s}/",
                )
            with open(os.path.join(library_path, fn), "w+", encoding = "utf-8") as f:
                f.write(cnt)

        elif "@" in url:

            path_pattern, url = url.split("@")
            zip_bin = requests.get(url, stream=True)

            with zipfile.ZipFile(io.BytesIO(zip_bin.content)) as z:
                for fp in z.namelist():
                    if not fnmatch.fnmatch(fp, path_pattern):
                        continue
                    with open(
                        os.path.join(library_path, os.path.basename(fp)), "wb"
                    ) as f:
                        f.write(z.read(fp))

        else:

            raise ValueError(f'unhandled url pattern: {url_pattern:s}')

    _log.info("Library %s updated", name)
