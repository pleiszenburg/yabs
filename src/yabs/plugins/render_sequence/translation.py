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

from datetime import datetime
import os
from random import randint
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
    KEY_DESCRIPTION,
    KEY_EMAIL,
    KEY_FIRSTNAME,
    KEY_FN,
    KEY_ID,
    KEY_MARKDOWN,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_LASTNAME,
    KEY_SLUG,
    KEY_MTIME,
    KEY_TAGS,
    KEY_TITLE,
    META_DELIMITER,
)
from ...slugify import slugify
from ...times import get_isotime

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Translation:
    """
    The translation of a post / entry.

    Mutable.
    """

    def __init__(self, context: Dict, path: str, prefix: str):

        self._context = context
        self._prefix = prefix

        with open(path, "r", encoding = "utf-8") as f:
            raw = f.read()
        meta, abstract, content = raw.split(META_DELIMITER)

        self._meta = load(meta, Loader = Loader)

        self._meta[KEY_AUTHORS] = [self._process_author(author) for author in self._meta.get(KEY_AUTHORS, [])]

        ctime = self._meta.get(KEY_CTIME, None)
        if ctime is None:
            self._meta[KEY_CTIME] = get_isotime(
                fn = path,
                tf = KEY_CTIME,
                warn = True,
            )
        else:
            self._meta[KEY_CTIME] = datetime.fromisoformat(ctime.replace(' ', 'T') + ':00+00:00').isoformat()

        mtime = self._meta.get(KEY_MTIME, None)
        if mtime is None:
            self._meta[KEY_MTIME] = self._meta[KEY_CTIME]
        else:
            self._meta[KEY_MTIME] = datetime.fromisoformat(mtime.replace(' ', 'T') + ':00+00:00').isoformat()

        if self._meta[KEY_CTIME] > self._meta[KEY_MTIME]:
            raise ValueError('ctime > mtime', path)

        self._meta[KEY_TITLE] = self._meta.get(KEY_TITLE, f'{randint(2**0, (2**64)-1):016x}')

        self._meta[KEY_SLUG] = slugify(self._meta[KEY_TITLE])
        self._meta[KEY_FN] = f"{self._prefix:s}{self._meta[KEY_SLUG]:s}.htm"

        tags = self._meta.get(KEY_TAGS, [])
        self._meta[KEY_TAGS] = sorted({tag for tag in tags if not tag.startswith('_')})
        self._meta[f'special_{KEY_TAGS:s}'] = sorted({tag for tag in tags if tag.startswith('_')})

        self._abstract = abstract.strip()
        self._abstract_rendered = None
        self._content = content.strip()
        self._content_rendered = None

        fn = os.path.basename(path)
        self._id, self._language, ext = fn.rsplit(".")
        assert ext == KEY_MARKDOWN


    def __eq__(self, other: Any) -> bool:

        if other is None:
            return False

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
    ):

        renderer = renderers[self._language]
        renderer.reset_counters()

        self._abstract_rendered = renderer(self._abstract)
        self._content_rendered = self._fix_h_levels(renderer(self._content))


    def write(
        self,
        languages: List[Tuple[str, str]], # available translations and URLs
        path: str,
        template: Callable, # jinja
        prefix: str, # custom for template, ignoring the one in FN for JavaScript
    ):

        with open(os.path.join(path, prefix + self._meta[KEY_FN][len(self._prefix):]), "w+", encoding = "utf-8") as f:

            f.write(template(**{
                KEY_ID: self._id,
                KEY_LANGUAGE: self._language,
                KEY_LANGUAGES: str(languages),
                KEY_ABSTRACT: self._abstract_rendered,
                KEY_CONTENT: self._content_rendered,
                KEY_DESCRIPTION: BeautifulSoup(
                    self._abstract_rendered, "html.parser"
                ).get_text().replace('\n', ' ').replace('  ', ' ').replace('"', "'").strip(),
            }, **self._meta))
