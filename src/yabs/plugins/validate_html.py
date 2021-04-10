# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/validate_html.py: Checks HTML with VNU/validator

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
import io
import json
from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict, List
import zipfile

import requests
from typeguard import typechecked

from ..const import (
    KEY_IGNORE,
    KEY_OUT,
    KEY_PREFIX,
    KEY_ROOT,
    KEY_UPDATE,
    KEY_WARNING,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

BIN_FLD = "bin"
DIST_FLD = "dist"
GITHUB = "https://api.github.com/repos/validator/validator/releases/latest"
SHARE_FLD = "share"
VALIDATOR_FN = "vnu.jar"
VERSION_FN = ".vnu_version"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def _update_validator():

    latest_dict = requests.get(url = GITHUB).json()
    latest_version = latest_dict["tag_name"]

    latest_path = os.path.join(os.environ["VIRTUAL_ENV"], SHARE_FLD, VERSION_FN)

    if os.path.isfile(latest_path):
        _log.info("Validator installed ... ")
        with open(latest_path, "r", encoding = "utf-8") as f:
            current_version = f.read().strip()
        _log.info("Installed validator version: %s", current_version)
        if current_version == latest_version:
            _log.info("Validator up to date ... ")
            return

    _log.info("Updating validator to version: %s", latest_version)

    latest_url = None
    for item in latest_dict["assets"]:
        if item["name"].startswith(VALIDATOR_FN) and item["name"].endswith(".zip"):
            latest_url = item["browser_download_url"]
    if latest_url is None:
        raise ValueError("no url found")

    latest_zip_bin = requests.get(latest_url, stream=True)

    validator_path = os.path.join(os.environ["VIRTUAL_ENV"], BIN_FLD, VALIDATOR_FN)
    if os.path.isfile(validator_path):
        os.unlink(validator_path)

    with zipfile.ZipFile(io.BytesIO(latest_zip_bin.content)) as z:
        with open(validator_path, "wb") as f:
            f.write(z.read(os.path.join(DIST_FLD, VALIDATOR_FN)))

    with open(latest_path, "w+", encoding = "utf-8") as f:
        f.write(latest_version)


@typechecked
def _validate_files(files: List[str], ignore: List[str]):

    vnu_cmd = [
        "java",
        "-jar",
        os.path.join(os.environ["VIRTUAL_ENV"], BIN_FLD, VALIDATOR_FN),
        "--format",
        "json",
    ] + files

    proc = Popen(vnu_cmd, stdout = PIPE, stderr = PIPE)
    out, err = proc.communicate()
    if out.decode("utf-8").strip() != "":
        _log.error(out.decode("utf-8"))
    vnu_out = json.loads(err.decode("utf-8"))

    vnu_by_file = {}

    for key, value in vnu_out.items():

        if key != "messages":
            _log.error("Unknown VNU JSON key: %s", key)
            continue

        for vnu_problem in value:

            if any(
                ignore_item in vnu_problem["message"] for ignore_item in ignore
            ):
                continue

            vnu_file = vnu_problem["url"]
            if vnu_file not in vnu_by_file.keys():
                vnu_by_file.update({vnu_file: []})
            vnu_by_file[vnu_file].append(
                f"\"{vnu_problem['type']:s}\": {vnu_problem['message']:s}"
            )
            vnu_by_file[vnu_file].append(
                f"[...]{vnu_problem['extract']:s}[...]"
                if "extract" in vnu_problem.keys()
                else "???"
            )

    vnu_files = list(vnu_by_file.keys())
    vnu_files.sort()
    for vnu_file in vnu_files:
        _log.warning("In file: %s", vnu_file.split('/')[-1])
        for line in vnu_by_file[vnu_file]:
            _log.warning(" %s", line)


@typechecked
def run(context: Dict, options: Dict):

    if any(
        [
            options.get(KEY_UPDATE, True),
            not os.path.isfile(
                os.path.join(os.environ["VIRTUAL_ENV"], SHARE_FLD, VERSION_FN)
            ),
        ]
    ):
        _update_validator()

    files = [
        fn
        for fn in glob.glob(
            os.path.join(context[KEY_OUT][KEY_ROOT], "**", "*.htm*"),
            recursive = True,
        )
        if not any(
            os.path.basename(fn).startswith(prefix)
            for prefix in options.get(f"{KEY_IGNORE:s}_{KEY_PREFIX:s}", [])
        )
    ]

    _validate_files(
        files, options.get(f"{KEY_IGNORE:s}_{KEY_WARNING:s}", [])
    )
