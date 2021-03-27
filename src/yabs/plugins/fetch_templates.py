# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_templates.py: Fetches jinja2 templates

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
import os
from typing import Dict

import jinja2
from typeguard import typechecked

from ..const import (
    KEY_DATA,
    KEY_DOMAIN,
    KEY_JINJA,
    KEY_SRC,
    KEY_TEMPLATES,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: None = None):

    context[KEY_JINJA] = jinja2.Environment(
        loader = jinja2.FileSystemLoader(
            context[KEY_SRC][KEY_TEMPLATES], encoding="utf-8", followlinks=False
        ),
        autoescape = False,  # jinja2.select_autoescape(enabled_extensions = ('html', 'xml', 'svg', 'jinja'))
    )
    context[KEY_JINJA].globals.update({
        KEY_DOMAIN: context[KEY_DOMAIN],
    })
    if KEY_DATA in context.keys():
        context[KEY_JINJA].globals.update({
            KEY_DATA: context[KEY_DATA],
        })

    context[KEY_TEMPLATES] = {
        name.rsplit(".", 1)[0]: context[KEY_JINJA].get_template(name)
        for name in [
            os.path.basename(fn)
            for fn in glob.glob(os.path.join(context[KEY_SRC][KEY_TEMPLATES], "*"))
            if os.path.isfile(fn)
        ]
    }
