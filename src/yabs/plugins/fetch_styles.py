# -*- coding: utf-8 -*-


import glob
import os
import subprocess


from yabs.const import KEY_OUT, KEY_PYGMENTS, KEY_SRC, KEY_STYLES, KEY_THEME
from yabs.log import log


def __pygmentize__(context):

    cmd_list = [
        "pygmentize",
        "-S",
        context[KEY_PYGMENTS][KEY_THEME],
        "-f",
        "html",
        "-a",
        ".highlight",
    ]

    proc = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()

    if errs.decode("utf-8").strip() != "":
        log.error(errs.decode("utf-8").strip())

    with open(
        os.path.join(context[KEY_OUT][KEY_STYLES], "%s.css" % KEY_PYGMENTS), "w+"
    ) as f:
        f.write(outs.decode("utf-8"))


def run(context, options=None):

    try:
        os.mkdir(context[KEY_OUT][KEY_STYLES])
    except FileExistsError:
        log.warning('Folder "%s" already exists.' % context[KEY_OUT][KEY_STYLES])

    suffix_list = ["css", "sass", "scss"]

    file_list = []
    for suffix in suffix_list:
        file_list.extend(
            glob.glob(os.path.join(context[KEY_SRC][KEY_STYLES], "*.%s" % suffix))
        )

    for src_file_path in file_list:

        fn = os.path.basename(src_file_path)

        with open(src_file_path, "r") as f:
            cnt = f.read()

        with open(os.path.join(context[KEY_OUT][KEY_STYLES], fn), "w") as f:
            f.write(cnt)

    __pygmentize__(context)
