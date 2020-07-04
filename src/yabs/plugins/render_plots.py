# -*- coding: utf-8 -*-


import glob
import importlib
import os
import sys
import traceback


from bs4 import BeautifulSoup


from yabs.const import (
    KEY_HTML,
    KEY_ID,
    KEY_JINJA,
    KEY_OUT,
    KEY_PLOT,
    KEY_PLOTS,
    KEY_PLOTLY,
    KEY_ROOT,
    KEY_SCRIPTS,
    KEY_SRC,
    KEY_STYLES,
    KEY_TEMPLATES,
    KEY_TYPE,
)
from yabs.log import log


def get_plotly_id(in_str):

    soup_list = list(BeautifulSoup(in_str, "html.parser"))

    if soup_list[0].name != "div":
        raise  # TODO

    return soup_list[0].attrs["id"]


def render(context, options, plot_name, plot_dict):

    plot_languages = plot_dict.pop(KEY_OUT)
    plot_type = plot_dict.pop(KEY_TYPE)

    scripts_path = os.path.relpath(
        context[KEY_OUT][KEY_SCRIPTS], context[KEY_OUT][KEY_ROOT]
    )
    if scripts_path not in ["", "."]:
        scripts_path += "/"
    styles_path = os.path.relpath(
        context[KEY_OUT][KEY_STYLES], context[KEY_OUT][KEY_ROOT]
    )
    if styles_path not in ["", "."]:
        styles_path += "/"

    for language_id in plot_languages.keys():

        plot_id = (
            get_plotly_id(plot_languages[language_id][KEY_HTML])
            if plot_type == KEY_PLOTLY
            else ""
        )

        plot_out = context[KEY_TEMPLATES]["%s_%s" % (KEY_PLOT, plot_type)].render(
            **{KEY_SCRIPTS: scripts_path, KEY_STYLES: styles_path, KEY_ID: plot_id},
            **plot_languages[language_id],
            **plot_dict
        )

        with open(
            os.path.join(
                context[KEY_OUT][KEY_ROOT],
                "%s_%s_%s.htm" % (KEY_PLOT, plot_name, language_id),
            ),
            "w",
        ) as f:
            f.write(plot_out)


def run(context, options=None):

    sys.path.insert(0, context[KEY_SRC][KEY_PLOTS])

    for file_path in glob.glob(os.path.join(context[KEY_SRC][KEY_PLOTS], "*.py*")):

        plot_fn = os.path.basename(file_path)
        plot_name = plot_fn.rsplit(".", 1)[0]

        try:
            plot_module = importlib.import_module(plot_name)
        except ModuleNotFoundError:
            log.warning('File "%s" can not be imported for rendering a plot.' % plot_fn)
            continue

        try:
            plot_dict = plot_module.run(context, options)
        except:
            log.error('File "%s" caused an error while trying to plot.' % plot_fn)
            log.error(traceback.format_exc())
            continue

        render(context, options, plot_name, plot_dict)

    sys.path.pop(0)
