# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import IMAGE_SUFFIX_LIST, KEY_IMAGES, KEY_OUT, KEY_ROOT, KEY_SRC


def run(context, options=None):

    os.mkdir(context[KEY_OUT][KEY_IMAGES])

    file_list = []
    for suffix in IMAGE_SUFFIX_LIST:
        file_list.extend(
            glob.glob(
                os.path.join(context[KEY_SRC][KEY_IMAGES], "**", "*.%s" % suffix),
                recursive=True,
            )
        )

    for src_file_path in file_list:

        fn = os.path.basename(src_file_path)

        with open(src_file_path, "rb") as f:
            cnt_bin = f.read()

        with open(os.path.join(context[KEY_OUT][KEY_IMAGES], fn), "wb") as f:
            f.write(cnt_bin)
