# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/markdown/__init__.py: Markdown root

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
from typing import Any, Dict

from typeguard import typechecked

from ...const import (
    KEY_IMAGES,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_MARKDOWN,
    KEY_NAME,
    KEY_TEMPLATES,
    KEY_OUT,
    KEY_ROOT,
)
from .markdown import YabsMarkdown

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Any = None):

    if KEY_MARKDOWN not in context.keys():
        context[KEY_MARKDOWN] = {}

    assert isinstance(context[KEY_MARKDOWN], dict)
    assert options[KEY_NAME] not in context[KEY_MARKDOWN].keys()

    context[KEY_MARKDOWN][KEY_NAME] = {}

    for language in context[KEY_LANGUAGES]:
        context[KEY_MARKDOWN][KEY_NAME][language] = YabsMarkdown.with_renderer(**{
            KEY_TEMPLATES: context[KEY_TEMPLATES],
            KEY_LANGUAGE: language,
            KEY_IMAGES: os.path.relpath(context[KEY_OUT][KEY_IMAGES], context[KEY_OUT][KEY_ROOT]),
        })
