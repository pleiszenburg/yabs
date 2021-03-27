# -*- coding: utf-8 -*-


import glob
from logging import getLogger
import os
from typing import Dict

from typeguard import typechecked

from yabs.const import (
    KEY_OUT,
    KEY_SRC,
    KEY_STYLES,
    LOGGER,
)


_log = getLogger(LOGGER)


@typechecked
def run(context: Dict, options: None = None):

    try:
        os.mkdir(context[KEY_OUT][KEY_STYLES])
    except FileExistsError:
        _log.warning('Folder "%s" already exists.', context[KEY_OUT][KEY_STYLES])

    files = []
    for suffix in ("css", "sass", "scss"):
        files.extend(
            glob.glob(os.path.join(context[KEY_SRC][KEY_STYLES], f"*.{suffix:s}"))
        )

    for path in files:

        fn = os.path.basename(path)

        with open(path, "r", encoding = "utf-8") as f:
            cnt = f.read()

        with open(os.path.join(context[KEY_OUT][KEY_STYLES], fn), "w", encoding = "utf-8") as f:
            f.write(cnt)
