# -*- coding: utf-8 -*-


from logging import getLogger
import os
from subprocess import Popen, PIPE
from typing import Dict

from typeguard import typechecked

from yabs.const import (
    KEY_NAME,
    KEY_OUT,
    # KEY_PYGMENTS,
    KEY_STYLES,
    KEY_THEME,
    LOGGER,
)


_log = getLogger(LOGGER)


@typechecked
def run(context: Dict, options: Dict):

    theme = options[KEY_THEME]
    name = options[KEY_NAME]
    path = context[KEY_OUT][KEY_STYLES]

    proc = Popen([
        "pygmentize",
        "-S",
        theme,
        "-f",
        "html",
        "-a",
        ".highlight",
    ], stdout = PIPE, stderr = PIPE,)
    outs, errs = proc.communicate()

    if errs.decode("utf-8").strip() != "" or proc.returncode != 0:
        _log.error("pygmentize failed: %s", errs.decode("utf-8").strip())

    with open(
        os.path.join(path, f"{name:s}.css"),
        "w+",
        encoding = "utf-8",
    ) as f:
        f.write(outs.decode("utf-8"))
