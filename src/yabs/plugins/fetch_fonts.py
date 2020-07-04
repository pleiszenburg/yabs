# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import KEY_FONTS, KEY_OUT, KEY_ROOT, KEY_SRC


def run(context, options=None):

    os.mkdir(context[KEY_OUT][KEY_FONTS])

    suffix_list = ["woff"]

    file_list = []
    for suffix in suffix_list:
        file_list.extend(
            glob.iglob(os.path.join(context[KEY_SRC][KEY_FONTS], "**/*.%s" % suffix))
        )

    for src_file_path in file_list:

        fn = os.path.basename(src_file_path)

        with open(src_file_path, "rb") as f:
            cnt_bin = f.read()

        with open(os.path.join(context[KEY_OUT][KEY_FONTS], fn), "wb") as f:
            f.write(cnt_bin)
