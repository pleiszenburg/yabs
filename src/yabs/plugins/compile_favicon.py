# -*- coding: utf-8 -*-


import glob
import os


from PIL import Image


from yabs.const import IMAGE_SUFFIX_LIST, KEY_IMAGES, KEY_OUT, KEY_ROOT


def run(context, options=None):

    file_list = []
    for suffix in IMAGE_SUFFIX_LIST:
        file_list.extend(
            glob.iglob(
                os.path.join(context[KEY_OUT][KEY_IMAGES], "**", "favicon.%s" % suffix),
                recursive=True,
            )
        )
    if len(file_list) > 1:
        raise
    elif len(file_list) == 0:
        return

    favicon_base = Image.open(file_list[0])
    favicon_base.save(
        os.path.join(context[KEY_OUT][KEY_ROOT], "favicon.ico"),
        sizes=[(16, 16), (32, 32), (128, 128)],
    )
    favicon = favicon_base.resize((96, 96))
    favicon.save(os.path.join(context[KEY_OUT][KEY_ROOT], "favicon.png"),)
    favicon_touch = favicon_base.resize((152, 152))
    favicon_touch.save(os.path.join(context[KEY_OUT][KEY_ROOT], "favicon_touch.png"),)
    favicon_base.close()

    os.unlink(file_list[0])
