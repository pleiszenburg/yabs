# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/render_sequence/translation.py: An entry translation

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
from typing import Any, Callable, Dict, List, Tuple

from bs4 import BeautifulSoup
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from typeguard import typechecked

from ...const import (
    KEY_ABSTRACT,
    KEY_AUTHORS,
    KEY_CONTENT,
    KEY_CTIME,
    KEY_EMAIL,
    KEY_FIRSTNAME,
    KEY_FN,
    KEY_ID,
    KEY_MARKDOWN,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_LASTNAME,
    KEY_MTIME,
    KEY_TITLE,
    META_DELIMITER,
)
from ...slugify import slugify

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Translation:
    """
    The translation of a post / entry.

    Immutable.
    """

    def __init__(self, context: Dict, path: str, sequence: str):

        self._context = context
        self._sequence = sequence

        with open(path, "r", encoding = "utf-8") as f:
            raw = f.read()
        meta, abstract, content = raw.split(META_DELIMITER)

        self._meta = load(meta, Loader = Loader)
        self._meta[KEY_AUTHORS] = [self._process_author(author) for author in self._meta[KEY_AUTHORS]]
        self._meta[KEY_MTIME] = self._meta.get(KEY_MTIME, self._meta[KEY_CTIME])
        for key in (KEY_CTIME, KEY_MTIME):
            self._meta[f"{key:s}_datetime"] = self._meta[KEY_MTIME].replace(" ", "T")
        self._meta[KEY_FN] = f"{self._sequence:s}_{slugify(self._meta[KEY_TITLE]):s}.htm"

        self._abstract = abstract.strip()
        self._abstract_rendered = None
        self._content = content.strip()
        self._content_rendered = None

        fn = os.path.basename(path)
        self._id, self._language, ext = fn.rsplit(".")
        assert ext == KEY_MARKDOWN


    def __eq__(self, other: Any) -> bool:

        assert isinstance(other, type(self))

        return self.id == other.id


    def __getitem__(self, key: str) -> Any:

        return self._meta[key]


    @property
    def abstract(self) -> str:

        return self._abstract


    @property
    def abstract_rendered(self) -> str:

        if self._abstract_rendered is None:
            raise ValueError('abstract has not been rendered')

        return self._abstract_rendered


    @property
    def id(self) -> str:

        return self._id


    @property
    def language(self) -> str:

        return self._language


    @property
    def content(self) -> str:

        return self._content


    @property
    def content_rendered(self) -> str:

        if self._content_rendered is None:
            raise ValueError('content has not been rendered')

        return self._content_rendered


    @staticmethod
    def _process_author(raw: str) -> Dict[str, str]:

        lastname, firstname, email = raw.split(',')

        return {
            KEY_LASTNAME: lastname.strip(),
            KEY_FIRSTNAME: firstname.strip(),
            KEY_EMAIL: email.strip(),
        }


    @staticmethod
    def _fix_h_levels(html: str) -> str:

        soup = BeautifulSoup(html, "html.parser")

        for h_level in range(5, 0, -1):
            for h_tag in soup.find_all(f"h{h_level:d}"):
                h_tag.name = f"h{h_level+1:d}"

        return str(soup)  # soup.prettify()


    def render(
        self,
        renderers: Dict, # markdown
        languages: List[Tuple[str, str]], # available translations and URLs
        path: str,
        template: Callable, # jinja
    ):

        renderer = renderers[self._language]

        self._abstract_rendered = renderer(self._abstract)
        self._content_rendered = self._fix_h_levels(renderer(self._content))

        with open(os.path.join(path, self._meta[KEY_FN]), "w+", encoding = "utf-8") as f:

            f.write(template(**{
                KEY_ID: self._id,
                KEY_LANGUAGE: self._language,
                KEY_LANGUAGES: str(languages),
                KEY_ABSTRACT: self._abstract_rendered,
                KEY_CONTENT: self._content_rendered,
            }, **self._meta))
