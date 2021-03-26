# -*- coding: utf-8 -*-


import glob
import os
from typing import Dict, List

from typeguard import typechecked

from yabs.const import (
    KEY_EXTENDS,
    KEY_HTML,
    KEY_OUT,
    KEY_PLACEHOLDER,
    KEY_PREFIX,
    KEY_ROOT,
    KEY_SRC,
    KEY_STAGING,
    KEY_TEMPLATE,
)


@typechecked
def find_files(context: Dict) -> List[str]:

    files = []

    for src in (KEY_HTML, KEY_STAGING):
        files.extend(glob.glob(
            os.path.join(context[KEY_SRC][src], "**", "*.htm*"),
            recursive = True,
        ))

    return files


@typechecked
def run(context: Dict, options: Dict):

    for path in find_files(context):

        with open(path, "r", encoding = "utf-8") as f:
            cnt = f.read()

        fn = os.path.basename(path)

        if options[KEY_PLACEHOLDER] in cnt:
            for extends in options[KEY_EXTENDS]:
                out = cnt.replace(options[KEY_PLACEHOLDER], extends[KEY_TEMPLATE])
                with open(
                    os.path.join(context[KEY_OUT][KEY_ROOT], f"{extends[KEY_PREFIX]:s}{fn:s}"),
                    "w",
                    encoding = "utf-8",
                ) as f:
                    f.write(out)
        else:
            with open(os.path.join(context[KEY_OUT][KEY_ROOT], fn), "w", encoding = "utf-8") as f:
                f.write(cnt)
