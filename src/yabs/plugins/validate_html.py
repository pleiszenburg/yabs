# -*- coding: utf-8 -*-


import glob
import io
import json
from logging import getLogger
import os
import subprocess
import zipfile


import requests


from yabs.const import AJAX_PREFIX, KEY_IGNORE, KEY_OUT, KEY_ROOT, KEY_UPDATE, LOGGER


BIN_FLD = "bin"
DIST_FLD = "dist"
SHARE_FLD = "share"
VALIDATOR_FN = "vnu.jar"
VERSION_FN = ".vnu_version"


_log = getLogger(LOGGER)


def update_validator():

    latest_dict = requests.get(
        url="https://api.github.com/repos/validator/validator/releases/latest"
    ).json()
    latest_version = latest_dict["tag_name"]

    version_file_path = os.path.join(os.environ["VIRTUAL_ENV"], SHARE_FLD, VERSION_FN)

    if os.path.isfile(version_file_path):
        with open(version_file_path, "r") as f:
            current_version = f.read().strip()
        if current_version == latest_version:
            _log.debug("Validator up to date ... ")
            return

    _log.info("Updating validator ... ")

    latest_url = None
    for item in latest_dict["assets"]:
        if item["name"].startswith(VALIDATOR_FN) and item["name"].endswith(".zip"):
            latest_url = item["browser_download_url"]
    if latest_url is None:
        raise  # TODO

    latest_zip_bin = requests.get(latest_url, stream=True)

    validator_path = os.path.join(os.environ["VIRTUAL_ENV"], BIN_FLD, VALIDATOR_FN)
    if os.path.isfile(validator_path):
        os.unlink(validator_path)

    with zipfile.ZipFile(io.BytesIO(latest_zip_bin.content)) as z:
        with open(validator_path, "wb") as f:
            f.write(z.read(os.path.join(DIST_FLD, VALIDATOR_FN)))

    with open(version_file_path, "w+") as f:
        f.write(latest_version)


def validate_files(file_list, ignore_list):

    vnu_cmd = [
        "java",
        "-jar",
        os.path.join(os.environ["VIRTUAL_ENV"], BIN_FLD, VALIDATOR_FN),
        "--format",
        "json",
    ] + file_list

    vnu_proc = subprocess.Popen(vnu_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = vnu_proc.communicate()

    if out.decode("utf-8").strip() != "":
        _log.error(out.decode("utf-8"))

    vnu_out = json.loads(err.decode("utf-8"))
    vnu_by_file = {}

    for key in vnu_out.keys():

        if key != "messages":
            _log.error("Unknown VNU JSON key: %s", key)
            continue

        for vnu_problem in vnu_out[key]:

            if any(
                ignore_item in vnu_problem["message"] for ignore_item in ignore_list
            ):
                continue

            vnu_file = vnu_problem["url"]
            if vnu_file not in vnu_by_file.keys():
                vnu_by_file.update({vnu_file: []})
            vnu_by_file[vnu_file].append(
                '"%s": %s' % (vnu_problem["type"], vnu_problem["message"])
            )
            vnu_by_file[vnu_file].append(
                "[...]%s[...]" % vnu_problem["extract"]
                if "extract" in vnu_problem.keys()
                else "???"
            )

    vnu_files = list(vnu_by_file.keys())
    vnu_files.sort()
    for vnu_file in vnu_files:
        _log.warning("In file: %s", vnu_file.split("/")[-1])
        for line in vnu_by_file[vnu_file]:
            _log.warning(" %s", line)


def run(context, options=None):

    if options is None:
        options = {}

    if any(
        [
            KEY_UPDATE in options.keys() and options[KEY_UPDATE],
            KEY_UPDATE not in options.keys(),
            not os.path.isfile(
                os.path.join(os.environ["VIRTUAL_ENV"], SHARE_FLD, VERSION_FN)
            ),
        ]
    ):
        update_validator()

    file_list = glob.glob(
        os.path.join(context[KEY_OUT][KEY_ROOT], "**", "*.htm*"), recursive=True
    )
    file_list = [
        fn for fn in file_list if not os.path.basename(fn).startswith(AJAX_PREFIX)
    ]

    validate_files(
        file_list, options[KEY_IGNORE] if KEY_IGNORE in options.keys() else []
    )
