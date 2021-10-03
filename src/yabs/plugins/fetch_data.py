# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/fetch_data.py: Fetches data from YAML and JSON files

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

import json
import glob
import os
from typing import Any, Dict, List, Tuple

from typeguard import typechecked
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from yabs.const import KEY_DATA, KEY_SRC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _load_csv(raw: str, sep: str = ';') -> List[Dict[str, str]]:

    lines = [
        line.strip()
        for line in raw.split()
        if len(line.split()) > 0
    ]

    header = [name.strip() for name in lines.pop(0).split(sep)]

    rec = [
        {
            name: value
            for name, value in zip(
                header,
                (value_.strip() for value_ in line.split(sep)),
            )
        }
        for line in lines
    ]

    return rec


@typechecked
def _load_data_file(file_path: str) -> Tuple[str, Any]:

    fn = os.path.basename(file_path)
    data_key, file_type = fn.rsplit(".")

    with open(file_path, "r", encoding = "utf-8") as f:
        data = f.read()

    if file_type == "yaml":
        return data_key, load(data, Loader=Loader)
    elif file_type == "json":
        return data_key, json.loads(data)
    elif file_type == 'csv':
        return data_key, _load_csv(data)
    else:
        raise ValueError(f"unknown file type: {file_type:s}")


@typechecked
def run(context: Dict, options: None = None):

    data_dict = {}

    for file_path in glob.iglob(
        os.path.join(context[KEY_SRC][KEY_DATA], "**/*.*"), recursive=True
    ):
        data_key, data_obj = _load_data_file(file_path)
        data_dict[data_key] = data_obj

    context[KEY_DATA] = data_dict
