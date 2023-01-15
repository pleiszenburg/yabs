# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/write_robotstxt.py: Writes robots txt file

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
import random
from typing import Dict

from typeguard import typechecked

from ..const import (
    KEY_DOMAIN,
    KEY_OUT,
    KEY_PREFIX,
    KEY_ROOT,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

HASH_DIGITS = 8

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def run(context: Dict, options: Dict):

    disallow_prefix = options[f"disallow_{KEY_PREFIX:s}"] # list

    allow_files = []
    disallow_files = []

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], "*.htm*")):

        fn = os.path.basename(file_path)

        if any(fn.startswith(prefix) for prefix in disallow_prefix):
            disallow_files.append(fn)
        else:
            allow_files.append(fn)

    cnt = """# revision {revision}

	User-agent: Mediapartners-Google
	Disallow: /

	User-agent: *
	{allow_list}
	{disallow_list}
	Sitemap: https://{domain}/sitemap.xml
	""".format(
        revision = (
            (f"%0{HASH_DIGITS:d}x") % random.randrange(16 ** HASH_DIGITS)
        ),
        allow_list = "\n".join([f"Allow: /{item:s}" for item in allow_files]),
        disallow_list = "\n".join([f"Disallow: /{item:s}" for item in disallow_files]),
        domain = context[KEY_DOMAIN],
    )

    cnt = "\n".join([line.strip() for line in cnt.split("\n")])

    with open(os.path.join(context[KEY_OUT][KEY_ROOT], "robots.txt"), "w") as f:
        f.write(cnt)
