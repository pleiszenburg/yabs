# -*- coding: utf-8 -*-


from distutils.dir_util import copy_tree
import os
import shutil
import subprocess
import time


from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


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
    YABS_FN,
)


def check_mountpoint(mountpoint):

    proc = subprocess.Popen(
        ["mountpoint", "-q", mountpoint],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()

    if out.decode(encoding="UTF-8").strip() != "":
        print(out.decode(encoding="UTF-8"))
    if err.decode(encoding="UTF-8").strip() != "":
        print(err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


def copy_current_build(buildroot, mountpoint):

    copy_tree(buildroot, mountpoint, preserve_symlinks=0)


def load_passwords(cfp_path):

    with open(cfp_path, "r") as f:
        cfg_dict = load(f.read(), Loader=Loader)

    return cfg_dict[KEY_PASSWORD]


def mount_sshfs(mountpoint, hostname, path, user, password):

    cmd = [
        "sshfs",
        "%s@%s:/%s" % (user, hostname, path),
        mountpoint,
        "-o",
        "password_stdin",
        "-o",
        "compression=yes",
    ]

    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    out, err = proc.communicate(input=password.encode(encoding="UTF-8"))

    if out.decode(encoding="UTF-8").strip() != "":
        print(out.decode(encoding="UTF-8"))
    if err.decode(encoding="UTF-8").strip() != "":
        print(err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


def remove_old_deployment(mountpoint):

    for entry in os.listdir(mountpoint):

        entry_path = os.path.join(mountpoint, entry)

        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            os.unlink(entry_path)
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
        else:
            raise  # TODO


def umount_sshfs(mountpoint):

    proc = subprocess.Popen(
        ["fusermount", "-u", mountpoint],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()

    if err.decode(encoding="UTF-8").strip() != "":
        print(err.decode(encoding="UTF-8"))

    return not bool(proc.returncode)


def run(context, options=None):

    passwords_dict = load_passwords(os.path.join(os.environ.get("HOME"), YABS_FN))

    status = mount_sshfs(
        options[KEY_MOUNTPOINT],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_HOSTNAME],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_PATH],
        options[KEY_TARGETS][options[KEY_TARGET]][KEY_USER],
        passwords_dict[options[KEY_TARGETS][options[KEY_TARGET]][KEY_USER]],
    )
    assert status
    assert check_mountpoint(options[KEY_MOUNTPOINT])

    remove_old_deployment(options[KEY_MOUNTPOINT])
    copy_current_build(context[KEY_OUT][KEY_ROOT], options[KEY_MOUNTPOINT])

    umount_count = 0
    while True:
        if umount_count == 10:
            raise  #
        try:
            status = umount_sshfs(options[KEY_MOUNTPOINT])
            assert status
            break
        except AssertionError:
            umount_count += 1
            time.sleep(0.25)
    assert not check_mountpoint(options[KEY_MOUNTPOINT])
    print("Good umount.")
