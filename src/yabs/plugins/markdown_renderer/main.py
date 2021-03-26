# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/markdown_renderer/main.py: Entry point

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

from typeguard import typechecked

from ...const import (
    KEY_BASE,
    KEY_CODE,
    KEY_FOOTNOTES,
    KEY_FORMULA,
    KEY_IMAGE,
    KEY_IMAGES,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_MARKDOWN,
    KEY_NAME,
    KEY_TEMPLATES,
    KEY_OUT,
    KEY_PLOT,
    KEY_ROOT,
    KEY_VIDEO,
)
from .markdown import YabsMarkdown

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Dict):

    if KEY_MARKDOWN not in context.keys():
        context[KEY_MARKDOWN] = {}

    assert isinstance(context[KEY_MARKDOWN], dict)
    assert options[KEY_NAME] not in context[KEY_MARKDOWN].keys()

    context[KEY_MARKDOWN][options[KEY_NAME]] = { # name of renderer
        language: YabsMarkdown.with_renderer(**{
            KEY_LANGUAGE: language,
            KEY_BASE: context[KEY_TEMPLATES][options[KEY_BASE]],
            KEY_IMAGE: context[KEY_TEMPLATES][options[KEY_IMAGE]],
            KEY_IMAGES: os.path.relpath(context[KEY_OUT][KEY_IMAGES], context[KEY_OUT][KEY_ROOT]),
            KEY_VIDEO: context[KEY_TEMPLATES][options[KEY_VIDEO]],
            KEY_PLOT: context[KEY_TEMPLATES][options[KEY_PLOT]],
            KEY_CODE: context[KEY_TEMPLATES][options[KEY_CODE]],
            KEY_FORMULA: context[KEY_TEMPLATES][options[KEY_FORMULA]],
            KEY_FOOTNOTES: context[KEY_TEMPLATES][options[KEY_FOOTNOTES]],
        })
        for language in context[KEY_LANGUAGES]
    }
