# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/markdown/renderer.py: Markdown renderer

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
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

from bs4 import BeautifulSoup
from mistune import Renderer
from typeguard import typechecked

from .katex import render_formula
from .pygments import render_code
from ..const import (
    IMAGE_SUFFIX_LIST,
    KEY_CODE,
    KEY_FIGURE,
    KEY_FORMULA,
    KEY_IMAGES,
    KEY_LANGUAGE,
    KEY_PLOT,
    KEY_TEMPLATES,
    KEY_VIDEO,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class YabsRenderer(Renderer):
    """
    Injects custom blocks and features
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._counters = {KEY_FIGURE: 0, KEY_PLOT: 0, KEY_VIDEO: 0, KEY_FORMULA: 0}

    def block_code(self, code: str, lang: str) -> str:
        """
        Renders a block of code as a figure
        """

        if not lang:
            # return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
            raise ValueError('no language specified')

        return self.options[KEY_TEMPLATES]["figure_code"].render(
            **{KEY_CODE: render_code(code, lang)}
        ) # TODO template hard code

    def block_math(self, text: str) -> str:
        """
        Renders a formula as a figure
        """

        self._counters[KEY_FORMULA] += 1

        return self.options[KEY_TEMPLATES][KEY_FORMULA].render(
            formula = render_formula(text),
            number = self._counters[KEY_FORMULA],
        ) # TODO template hard code

    def footnotes(self, text: str) -> str:
        """
        Renders footnotes below text
        """

        return self.options[KEY_TEMPLATES]["footnotes"].render(footnotes=text) # TODO template hard code

    def latex_environment(self, name: str, text: str) -> str:
        """
        Wrap text in LaTeX block
        """

        return fr"\begin{{{name:s}}}{text:s}\end{{{name:s}}}"

    def inline_math(self, text: str) -> str:
        """
        Translates LaTeX formula into HTML/SVG
        """

        return render_formula(text)

    def paragraph(self, text: str) -> str:
        """
        Renders paragraph, dispatches to figure renderers
        """

        text_strip = text.strip(" ")
        test_soup_list = list(BeautifulSoup(text_strip, "html.parser"))

        if len(test_soup_list) == 1 and test_soup_list[0].name == "img":

            return self._figure(
                src = test_soup_list[0].attrs["src"],
                title = test_soup_list[0].attrs["title"]
                if "title" in test_soup_list[0].attrs.keys()
                else "",
                text = test_soup_list[0].attrs["alt"],
            )

        return "<p>%s</p>\n" % text_strip

    def _figure(self, src: str, title: str, text: str) -> str:
        """
        Applies figure templates
        """

        if any(src.endswith(item) for item in IMAGE_SUFFIX_LIST):

            self._counters[KEY_FIGURE] += 1
            return self.options[KEY_TEMPLATES]["figure_image"].render(
                alt_attr=text,
                alt_html=text,
                number=self._counters[KEY_FIGURE],
                src=os.path.join(self.options[KEY_IMAGES], src)
                if not src.startswith("http")
                else src,
                title=title,
                language=self.options[KEY_LANGUAGE],
            ) # TODO template hard code

        if src.startswith("youtube:"):

            self._counters[KEY_VIDEO] += 1
            return self.options[KEY_TEMPLATES]["figure_video"].render(
                alt_html=text,
                number=self._counters[KEY_VIDEO],
                video_id=src.split(":")[1],
                language=self.options[KEY_LANGUAGE],
            ) # TODO template hard code

        if src.startswith("plot:"):

            self._counters[KEY_PLOT] += 1
            return self.options[KEY_TEMPLATES]["figure_plot"].render(
                alt_html=text,
                number=self._counters[KEY_PLOT],
                plot_id=src.split(":")[1],
                language=self.options[KEY_LANGUAGE],
            ) # TODO template hard code

        raise  # handle youtube, plots, etc HERE!
