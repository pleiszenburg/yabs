# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/server.py: Simple HTTP server

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

from http.server import HTTPServer, SimpleHTTPRequestHandler
from logging import getLogger
import os
from typing import Any, Dict

from typeguard import typechecked

from ..const import KEY_HOSTNAME, KEY_OUT, KEY_PORT, KEY_ROOT, LOGGER

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class _Handler(SimpleHTTPRequestHandler):

    def log_message(self, format: str, *args: Any):

        _log.info(format, *args)

@typechecked
def run(context: Dict, options: Dict):

    os.chdir(context[KEY_OUT][KEY_ROOT])

    _Handler.extensions_map.update({".mf": "text/cache-manifest"})
    httpd = HTTPServer((options[KEY_HOSTNAME], options[KEY_PORT]), _Handler)
    httpd.serve_forever()
