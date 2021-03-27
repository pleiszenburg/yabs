# -*- coding: utf-8 -*-


import glob
import os
from typing import Dict


import sass
from typeguard import typechecked


STYLE_SASS = "sass"
STYLE_SCSS = "scss"
STYLE_SUFFIX_LIST = [STYLE_SASS, STYLE_SCSS]


from yabs.const import KEY_COLORS, KEY_OUT, KEY_STYLES


@typechecked
def run(context: Dict, options: None = None):

    colors = "\n".join([
        f"${name:s}: rgb({r:d}, {g:d}, {b:d})"
        for name, (r, g, b) in context[KEY_COLORS].items()
    ])

    suffixes = ("sass", "scss")

    files = []
    for suffix in suffixes:
        files.extend(
            glob.glob(os.path.join(context[KEY_OUT][KEY_STYLES], f"*.{suffix}"))
        )

    for path in files:

        with open(path, "r", encoding = "utf-8") as f:
            cnt = f.read()
        os.unlink(path)

        cnt = sass.compile(
            string = f"{colors:s}\n{cnt:s}",
            output_style = "compact",
            indented = path.endswith(STYLE_SASS),
        )

        for suffix in suffixes:
            if path.endswith(suffix):
                path = path[: -1 * len(suffix)] + "css"
                break

        with open(path, "w", encoding = "utf-8") as f:
            f.write(cnt)
