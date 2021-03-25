# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/markdown/inlinegrammar.py: Inline grammar

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

from mistune import InlineGrammar
from typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class YabsInlineGrammar(InlineGrammar):
    """
    This defines different ways of declaring math objects that should be
	passed through to mathjax unaffected. These are used by the YabsInlineLexer.
	"""

    inline_math = re.compile(r"^\$(.+?)\$|^\\\\\((.+?)\\\\\)", re.DOTALL)

    block_math = re.compile(r"^\$\$(.*?)\$\$|^\\\\\[(.*?)\\\\\]", re.DOTALL)

    latex_environment = re.compile(
        r"^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}", re.DOTALL
    )

    text = re.compile(r"^[\s\S]+?(?=[\\<!\[_*`~$]|https?://| {2,}\n|$)")
