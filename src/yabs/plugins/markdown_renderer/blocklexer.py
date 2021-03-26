# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/markdown_renderer/blocklexer.py: Block lexer

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

from mistune import BlockLexer, BlockGrammar
from typeguard import typechecked

from .blockgrammar import YabsBlockGrammar

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class YabsBlockLexer(BlockLexer):
    """
    This acts as a pass-through to the YabsInlineLexer. It is needed in
	order to avoid other block level rules splitting math sections apart.
	"""

    default_rules = ["multiline_math"] + BlockLexer.default_rules

    def __init__(self, rules: Union[BlockGrammar, None] = None, **kwargs):

        if rules is None:
            rules = YabsBlockGrammar()

        super().__init__(rules, **kwargs)

    def parse_multiline_math(self, m: re.Match):
        """
        Add token to pass through mutiline math.
        """

        self.tokens.append({"type": "multiline_math", "text": m.group(0)})
