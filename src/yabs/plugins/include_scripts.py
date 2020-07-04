# -*- coding: utf-8 -*-


import glob
import os
import subprocess


from yabs.const import KEY_OUT, KEY_SCRIPTS


def run(context, options=None):

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_SCRIPTS], "*.js")):

        proc = subprocess.Popen(
            ["browserify", file_path, "-o", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()

        if out.decode("utf-8").strip() != "":
            print(out.decode("utf-8"))
        if err.decode("utf-8").strip() != "":
            print(err.decode("utf-8"))
