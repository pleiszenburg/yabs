# -*- coding: utf-8 -*-


import os
# import stat


from yabs.const import (
    KEY_OUT,
    KEY_ROOT,
)


def run(context, options=None):

    out_path = os.path.join(context[KEY_OUT][KEY_ROOT], ".htaccess")

    with open(out_path, "w") as f:
        f.write(options)

    # BUG 1und1 ...
    # os.chmod(out_path, stat.S_IWUSR | stat.S_IRUSR)
