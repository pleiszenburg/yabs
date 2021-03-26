# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/markdown_renderer/markdown.py: Core markdown class

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

import os
from typing import Dict

from mistune import Markdown
from typeguard import typechecked

from .blocklexer import YabsBlockLexer
from .inlinelexer import YabsInlineLexer
from .renderer import YabsRenderer

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class YabsMarkdown(Markdown):
    """
    Injects custom lexers
    """

    def __init__(self, renderer, **kwargs):

        if "inline" not in kwargs:
            kwargs["inline"] = YabsInlineLexer
        if "block" not in kwargs:
            kwargs["block"] = YabsBlockLexer

        super().__init__(renderer, **kwargs)

    def output_multiline_math(self):

        return self.inline(self.token["text"])

    @classmethod
    def with_renderer(cls, **options) -> Markdown:

        return cls(renderer = YabsRenderer(**options))
