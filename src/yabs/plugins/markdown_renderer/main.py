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
from typing import Any, Dict

from typeguard import typechecked

from ...const import (
    KEY_CODE,
    KEY_CONTEXT,
    KEY_FOOTNOTES,
    KEY_FORMULA,
    KEY_IMAGE,
    KEY_IMAGES,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_MAP,
    KEY_MAPFRAME,
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

    def _get_template(name: str) -> Any:
        option = options.get(name, None)
        if option is None:
            return None
        try:
            return context[KEY_TEMPLATES][option]
        except KeyError as e:
            raise ValueError(f'Markdown renderer missing specified template "{option:s}"') from e

    if KEY_MARKDOWN not in context.keys():
        context[KEY_MARKDOWN] = {}

    assert isinstance(context[KEY_MARKDOWN], dict)
    assert options[KEY_NAME] not in context[KEY_MARKDOWN].keys()

    templates = {
        name: _get_template(name)
        for name in (
            KEY_IMAGE,
            KEY_VIDEO,
            KEY_PLOT,
            KEY_CODE,
            KEY_FORMULA,
            KEY_FOOTNOTES,
            KEY_MAP,
            KEY_MAPFRAME,
        )
    }
    templates = {k: v for k, v in templates.items() if v is not None}

    context[KEY_MARKDOWN][options[KEY_NAME]] = { # name of renderer
        language: YabsMarkdown.with_renderer(**{
            KEY_CONTEXT: context,
            KEY_LANGUAGE: language,
            KEY_IMAGES: os.path.relpath(context[KEY_OUT][KEY_IMAGES], context[KEY_OUT][KEY_ROOT]),
        }, **templates)
        for language in context[KEY_LANGUAGES]
    }
