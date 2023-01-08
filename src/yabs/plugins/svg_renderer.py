# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/svg_renderer.py: Render SVG to raster

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

from logging import getLogger
from subprocess import Popen, PIPE
from typing import Dict, Optional

from typeguard import typechecked

from ..const import (
    KEY_NAME,
    KEY_SVG,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _svg_to_raster(
    src: str,
    dest: str,
    background_color: str = 'FFFFFF',
    background_opacity: int = 0,
    width: Optional[int] = None,
    height: Optional[int] = None,
    dpi: Optional[int] = None,
):
    """
    Convert SVG to raster via Inkscape
    """

    cmd = [
        'inkscape',
        src,  # source
        f'--export-filename={dest:s}',  # destination
        '-C',  # export entire drawing area
        f'--export-background={background_color:s}',
        f'--export-background-opacity={background_opacity:d}',
    ]

    if width is not None:
        cmd.append(f'--export-width={width:d}')
    if height is not None:
        cmd.append(f'--export-height={height:d}')
    if dpi is not None:
        cmd.append(f'--export-dpi={dpi:d}')

    proc = Popen(
        cmd,
        stdout = PIPE,
        stderr = PIPE,
    )
    out, err = proc.communicate()

    for name, msg in (
        ('stdout', out.decode('utf-8')),
        ('stderr', err.decode('utf-8')),
    ):
        for line in msg.split('\n'):
            if len(line.strip()) == 0:
                continue
            if line.strip() == "Background RRGGBBAA: ffffff00":
                continue
            if line.lstrip().startswith('Area ') and ' exported to ' in line:
                continue
            _log.info(f'inkscape/{name:s}: {line:s}')

@typechecked
def run(context: Dict, options: Dict):

    if KEY_SVG not in context.keys():
        context[KEY_SVG] = {}

    assert isinstance(context[KEY_SVG], dict)
    assert options[KEY_NAME] not in context[KEY_SVG].keys()

    context[KEY_SVG][options[KEY_NAME]] = _svg_to_raster