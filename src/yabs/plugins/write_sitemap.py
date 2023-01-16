# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/write_sitemap.py: Writes sitemap xml file

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

from datetime import datetime, timezone
import glob
from logging import getLogger
import os
from typing import Dict

from bs4 import BeautifulSoup
from typeguard import typechecked

from .render_sequence.translation import Translation
from ..const import (
    KEY_DOMAIN,
    KEY_ENTRIES,
    KEY_FN,
    KEY_IGNORE,
    KEY_MTIME,
    KEY_OUT,
    KEY_PREFIX,
    KEY_ROOT,
    KEY_SEQUENCES,
    LOGGER,
)

_log = getLogger(LOGGER)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class _Sitemap:
    """
    Generates an XML sitemap file.

    Mutable, single use.
    """

    def __init__(self, context: Dict, options: Dict):

        ignore_prefix = options[f"{KEY_IGNORE:s}_{KEY_PREFIX:s}"] # list

        self._context = context
        self._sequence_names = list(context.get(KEY_SEQUENCES, {}).keys())

        files = []
        for file_path in glob.glob(os.path.join(self._context[KEY_OUT][KEY_ROOT], "*.htm*")):
            fn = os.path.basename(file_path)
            if not any(fn.startswith(prefix) for prefix in ignore_prefix):
                files.append(fn)

        cnt = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {entries}
        </urlset>
        """.format(
            entries = "\n".join([self._generate_entry(fn) for fn in files])
        )

        cnt = "\n".join([line.strip() for line in cnt.split("\n")])

        with open(os.path.join(context[KEY_OUT][KEY_ROOT], "sitemap.xml"), mode = "w", encoding = "utf-8") as f:
            f.write(cnt)


    def _find_translation(self, fn: str) -> Translation:

        for entry in self._context[KEY_SEQUENCES][self._get_sequence_name(fn)][KEY_ENTRIES]:
            for translation in entry.translations:
                if translation[KEY_FN] == fn:
                    return translation

        raise ValueError('sequence entry is None')


    def _generate_entry(self, fn: str) -> str:

        return """<url>
    	<loc>https://{domain:s}/{filename:s}</loc>
    	<lastmod>{lastmod:s}</lastmod>
    	<changefreq>weekly</changefreq>
    	<priority>{priority:0.2f}</priority>
    	</url>""".format(
            domain = self._context[KEY_DOMAIN],
            filename = fn,
            lastmod = self._get_lastmod(fn),
            priority = self._get_priority(fn),
        )


    def _get_lastmod(self, fn: str) -> str:

        with open(
            os.path.join(self._context[KEY_OUT][KEY_ROOT], fn),
            mode = "r",
            encoding="utf-8",
        ) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        mtime = soup.find("meta", property="og:modified_time")
        if mtime is not None:
            mtime = mtime["content"]
            return datetime.fromisoformat(mtime).isoformat()[:10]  # validation

        if self._is_in_sequence(fn):  # fallback to the above
            return datetime.fromisoformat(self._get_lastmod_translation(fn)).isoformat()[:10]  # validation

        _log.warning(f'No mtime, falling back to today: {fn:s}')
        return datetime.now().astimezone(timezone.utc).isoformat()[:10]


    def _get_lastmod_translation(self, fn: str) -> str:

        return self._find_translation(fn)[KEY_MTIME].split(" ")[0]


    def _get_priority(self, fn: str) -> float:

        if fn.startswith("index"):
            return 1.0
        if self._is_in_sequence(fn):
            return 0.75
        if fn.startswith("plot_") or fn.startswith("map_"):  # TODO expose to configuration
            return 0.25

        return 0.5  # default


    def _get_sequence_name(self, fn: str) -> str:

        assert self._is_in_sequence(fn)

        return next(
            sequence_name
            for sequence_name in self._sequence_names
            if fn.startswith(f"{sequence_name:s}_")
        )


    def _is_in_sequence(self, fn: str) -> bool:

        return any((
            fn.startswith(f"{sequence_name:s}_")
            for sequence_name in self._sequence_names
        ))


@typechecked
def run(context: Dict, options: Dict):

    _ = _Sitemap(context = context, options = options)
