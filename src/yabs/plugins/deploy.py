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

from distutils.dir_util import copy_tree
from logging import getLogger
import os
import shutil
from subprocess import Popen, PIPE
import time
from typing import Dict

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from typeguard import typechecked

from yabs.const import (
    KEY_HOSTNAME,
    KEY_MOUNTPOINT,
    KEY_OUT,
    KEY_PATH,
    KEY_PASSWORD,
    KEY_ROOT,
    KEY_TARGET,
    KEY_TARGETS,
    KEY_USER,
    LOGGER,
    YABS_FN,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _check_mountpoint(mountpoint: str) -> bool:

    proc = Popen(
        ["mountpoint", "-q", mountpoint],
        stdout = PIPE,
        stderr = PIPE,
    )
    out, err = proc.communicate()

    if out.decode(encoding="UTF-8").strip() != "":
        _log.info("mountpoint: %s", out.decode(encoding="UTF-8"))
    if err.decode(encoding="UTF-8").strip() != "":
        _log.error("mountpoint: %s", err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


@typechecked
def _copy_current_build(buildroot: str, mountpoint: str):

    copy_tree(buildroot, mountpoint, preserve_symlinks = 0)


@typechecked
def _load_passwords(path: str) -> Dict[str, str]:

    with open(path, "r", encoding = "utf-8") as f:
        config = load(f.read(), Loader = Loader) # dict

    return config[KEY_PASSWORD]


@typechecked
def _mount_sshfs(mountpoint: str, hostname: str, path: str, user: str, password: str) -> bool:

    cmd = [
        "sshfs",
        f"{user:s}@{hostname:s}:/{path:s}",
        mountpoint,
        "-o",
        "password_stdin",
        "-o",
        "compression=yes",
    ]

    proc = Popen(
        cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE,
    )
    out, err = proc.communicate(input = password.encode(encoding="UTF-8"))

    if out.decode(encoding="UTF-8").strip() != "":
        _log.info("sshfs: %s", out.decode(encoding="UTF-8"))
    if err.decode(encoding="UTF-8").strip() != "":
        _log.error("sshfs: %s", err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


@typechecked
def _remove_old_deployment(mountpoint: str):

    for entry in os.listdir(mountpoint):

        entry_path = os.path.join(mountpoint, entry)

        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            os.unlink(entry_path)
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
        else:
            raise ValueError(f"remote path {mountpoint:s} is not file, link or directory")


@typechecked
def _umount_sshfs(mountpoint: str) -> bool:

    proc = Popen(
        ["fusermount", "-u", mountpoint],
        stdout = PIPE,
        stderr = PIPE,
    )
    out, err = proc.communicate()

    if out.decode(encoding="UTF-8").strip() != "":
        _log.info("fusermount: %s", out.decode(encoding="UTF-8"))
    if err.decode(encoding="UTF-8").strip() != "":
        _log.error("fusermount: %s", err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


@typechecked
def run(context: Dict, options: Dict):

    _log.info("Loading credentials ...")
    passwords_dict = _load_passwords(os.path.join(os.environ.get("HOME"), YABS_FN))

    _log.info("Mounting remote ...")
    status = _mount_sshfs(
        options[KEY_MOUNTPOINT],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_HOSTNAME],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_PATH],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_USER],
        passwords_dict[options[KEY_TARGETS][options[KEY_TARGET]][KEY_USER]],
    )

    _log.info("Checking mount result ...")
    assert status
    assert _check_mountpoint(options[KEY_MOUNTPOINT])

    _log.info("Removing old content ...")
    _remove_old_deployment(options[KEY_MOUNTPOINT])

    _log.info("Uploading new content ...")
    _copy_current_build(context[KEY_OUT][KEY_ROOT], options[KEY_MOUNTPOINT])

    _log.info("Unmounting ...")
    umount_count = 0
    while True:
        if umount_count == 20:
            raise SystemError("failed to unmount")
        try:
            status = _umount_sshfs(options[KEY_MOUNTPOINT])
            assert status
            _log.info("... succeeded ...")
            break
        except AssertionError:
            _log.info("... failed, waiting for re-try ...")
            umount_count += 1
            time.sleep(0.25)

    _log.info("Checking umount result ...")
    assert not _check_mountpoint(options[KEY_MOUNTPOINT])

    _log.info("Deployed.")
