# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/render_plots.py: Renders plotly and bokeh plots

    Copyright (C) 2018-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/yabs/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import glob
import importlib
from logging import getLogger
import os
import sys
from typing import Any, Dict

from bs4 import BeautifulSoup
from typeguard import typechecked

from ..const import (
    KEY_CTIME,
    KEY_HTML,
    KEY_ID,
    KEY_LANGUAGE,
    KEY_MTIME,
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
    LOGGER,
)
from ..times import get_isotime

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _get_plotly_id(html: str) -> str:

    soup_list = list(BeautifulSoup(html, "html.parser"))

    if soup_list[0].name != "div":
        raise ValueError("no div-tag found")

    return soup_list[0].attrs["id"]


@typechecked
def _render(context: Dict, plot_name: str, plot_dict: Dict):

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
            _get_plotly_id(plot_languages[language_id][KEY_HTML])
            if plot_type == KEY_PLOTLY
            else ""
        )

        plot_out = context[KEY_TEMPLATES][f"{KEY_PLOT:s}_{plot_type:s}"].render(
            **{KEY_SCRIPTS: scripts_path, KEY_STYLES: styles_path, KEY_ID: plot_id, KEY_LANGUAGE: language_id},
            **plot_languages[language_id],
            **plot_dict
        )

        with open(
            os.path.join(
                context[KEY_OUT][KEY_ROOT],
                f"{KEY_PLOT:s}_{plot_name:s}_{language_id:s}.htm",
            ),
            "w",
            encoding = "utf-8",
        ) as f:
            f.write(plot_out)


@typechecked
def run(context: Dict, options: Any = None):

    sys.path.insert(0, context[KEY_SRC][KEY_PLOTS])

    for file_path in glob.glob(os.path.join(context[KEY_SRC][KEY_PLOTS], "*.py*")):

        plot_fn = os.path.basename(file_path)
        plot_name = plot_fn.rsplit(".", 1)[0]

        try:
            plot_module = importlib.import_module(plot_name)
        except ModuleNotFoundError:
            _log.warning('File "%s" can not be imported for rendering a plot.', plot_fn)
            continue

        try:
            plot_dict = plot_module.run(context, options)
        except:
            _log.exception('File "%s" caused an error while trying to plot.', plot_fn)
            continue

        plot_dict.update({
            f'og_{KEY_CTIME:s}': get_isotime(
                fn = file_path,
                tf = KEY_CTIME,
                warn = True
            ),
            f'og_{KEY_MTIME:s}': get_isotime(
                fn = file_path,
                tf = KEY_MTIME,
                warn = True
            ),
        })

        _render(context, plot_name, plot_dict)

    sys.path.pop(0)
