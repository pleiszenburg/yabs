# -*- coding: utf-8 -*-


import os
import shutil
from typing import Dict

from typeguard import typechecked

from yabs.const import KEY_OUT, KEY_ROOT, KEY_SRC, KEY_STAGING


@typechecked
def clean_folder(path: str):

    for entry in os.listdir(path):

        entry_path = os.path.join(path, entry)

        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            os.unlink(entry_path)
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
        else:
            raise SystemError("not file, link or directory")


@typechecked
def run(context: Dict, options: None = None):

    for path in (context[KEY_OUT][KEY_ROOT], context[KEY_SRC][KEY_STAGING]):
        clean_folder(path)
