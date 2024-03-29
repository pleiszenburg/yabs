# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/markdown_renderer/renderer.py: Markdown renderer

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

from logging import getLogger
import os

from bs4 import BeautifulSoup
from mistune import Renderer, Markdown
import requests
from typeguard import typechecked

from ...const import (
    IMAGE_SUFFIX_LIST,
    KEY_CODE,
    KEY_CONTEXT,
    KEY_FIGURE,
    KEY_FOOTNOTES,
    KEY_FORMULA,
    KEY_IMAGE,
    KEY_IMAGES,
    KEY_LANGUAGE,
    KEY_PLOT,
    KEY_SRC,
    KEY_VIDEO,
    LOGGER,
)
from .katex import render_formula
from .pygments import render_code

_log = getLogger(LOGGER)

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

        self._counters = {
            key: 0
            for key in (
                KEY_FIGURE,
                KEY_PLOT,
                KEY_VIDEO,
                KEY_FORMULA,
                KEY_CODE,
            )
        }

    def reset_counters(self):

        self._counters = {key: 0 for key in self._counters.keys()}

    def block_code(self, code: str, lang: str) -> str:
        """
        Renders a block of code as a figure
        """

        if not lang:
            # return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
            raise ValueError('no language specified')

        self._counters[KEY_CODE] += 1

        text = ''
        lines = code.rstrip().rsplit('\n', 1)
        if lines[-1].startswith('"""') and lines[-1].endswith('"""'):
            text = lines.pop(-1)[3:-3]
            if '\n' in text:
                raise ValueError('new lines in code caption not supported')
            text = Markdown()(text).strip()[3:-4] # HACK
            code = '\n'.join(lines)

        return self.options[KEY_CODE].render(
            **{KEY_CODE: render_code(code, lang)},
            alt_html=text,
            number=self._counters[KEY_CODE],
            language=self.options[KEY_LANGUAGE],
        )

    def block_math(self, text: str) -> str:
        """
        Renders a formula as a figure
        """

        self._counters[KEY_FORMULA] += 1

        return self.options[KEY_FORMULA].render(
            formula = render_formula(text),
            number = self._counters[KEY_FORMULA],
        )

    def footnotes(self, text: str) -> str:
        """
        Renders footnotes below text
        """

        return self.options[KEY_FOOTNOTES].render(footnotes=text)

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
            return self.options[KEY_IMAGE].render(
                alt_attr=text,
                alt_html=text,
                number=self._counters[KEY_FIGURE],
                src=os.path.join(self.options[KEY_IMAGES], src)
                if not src.startswith("http")
                else src,
                title=title,
                language=self.options[KEY_LANGUAGE],
            )

        if src.startswith("youtube:"):

            video_id = src.split(":")[1]

            img_fn = os.path.join(
                self.options[KEY_CONTEXT][KEY_SRC][KEY_IMAGES],
                f'youtube_{video_id:s}.jpg'
            )
            if not os.path.exists(img_fn):
                _log.info('youtube thumbnail missing, loading "%s"', video_id)
                rq = requests.get(f'https://img.youtube.com/vi/{video_id:s}/hqdefault.jpg')
                if rq.status_code != 200:
                    raise ValueError(f'loading youtube thumbnail for "{video_id:s}" failed, code', rq.status_code)
                with open(img_fn, mode = 'wb') as f:
                    f.write(rq.content)

            self._counters[KEY_VIDEO] += 1
            return self.options[KEY_VIDEO].render(
                alt_html=text,
                number=self._counters[KEY_VIDEO],
                video_id=video_id,
                language=self.options[KEY_LANGUAGE],
            )

        if src.startswith("plot:"):

            self._counters[KEY_PLOT] += 1
            return self.options[KEY_PLOT].render(
                alt_html=text,
                number=self._counters[KEY_PLOT],
                plot_id=src.split(":")[1],
                language=self.options[KEY_LANGUAGE],
            )

        raise ValueError('unknown type of figure', src)
