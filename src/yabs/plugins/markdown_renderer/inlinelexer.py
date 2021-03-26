# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/markdown/inlinelexer.py: Inline lexer

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

import re
from typing import Union

from mistune import InlineLexer, InlineGrammar
from typeguard import typechecked

from .inlinegrammar import YabsInlineGrammar

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class YabsInlineLexer(InlineLexer):
    """
    This interprets the content of LaTeX style math objects using the rules
	defined by the YabsInlineGrammar.

	In particular this grabs ``$$...$$``, ``\\[...\\]``, ``\\(...\\)``, ``$...$``,
	and ``\begin{foo}...\end{foo}`` styles for declaring mathematics. It strips
	delimiters from all these varieties, and extracts the type of environment
	in the last case (``foo`` in this example).
	"""

    default_rules = [
        "block_math",
        "inline_math",
        "latex_environment",
    ] + InlineLexer.default_rules

    def __init__(self, renderer, rules: Union[InlineGrammar, None] = None, **kwargs):

        if rules is None:
            rules = YabsInlineGrammar()

        super().__init__(renderer, rules, **kwargs)

    def output_inline_math(self, m: re.Match) -> str:

        return self.renderer.inline_math(m.group(1) or m.group(2))

    def output_block_math(self, m: re.Match) -> str:

        return self.renderer.block_math(m.group(1) or m.group(2) or "")

    def output_latex_environment(self, m: re.Match) -> str:

        return self.renderer.latex_environment(m.group(1), m.group(2))
