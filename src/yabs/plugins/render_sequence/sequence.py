# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/render_sequence/sequence.py: A sequence

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
import glob
import os
from typing import Any, Dict, List

from typeguard import typechecked

from ...const import (
    KEY_ENTRIES,
    KEY_FN,
    KEY_LANGUAGES,
    KEY_MARKDOWN,
    KEY_MTIME,
    KEY_NAME,
    KEY_RENDERER,
    KEY_SEQUENCES,
    KEY_SRC,
    KEY_STAGING,
    KEY_TEMPLATE,
    KEY_TEMPLATES,
)
from .entry import Entry
from .translation import Translation

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Sequence:
    """
    A sequence with multiple entries.

    Mutable.
    """

    def __init__(self, context: Dict, options: Any):

        self._context = context
        self._name = options[KEY_NAME]
        self._template = context[KEY_TEMPLATES][options[KEY_TEMPLATE]]

        self._renderers = {
            language: context[KEY_MARKDOWN][options[KEY_RENDERER]][language]
            for language in context[KEY_LANGUAGES]
        }

        self._entries = sorted(self._match_translations([
            Translation(
                context = context,
                path = path,
                sequence = self._name,
            )
            for path in glob.glob(
                os.path.join(options[KEY_SRC], "**", f"*.{KEY_MARKDOWN:s}"),
                recursive = True,
            )
        ]), key = self._sort_entry_by)

        self._render_entries()
        self._build_data()


    @staticmethod
    def _match_translations(translations: List[Translation]) -> List[Entry]:

        entries = {
            translation.id: Entry(id = translation.id)
            for translation in translations
        }

        for translation in translations:
            entries[translation.id].add(translation)

        return list(entries.values())


    @staticmethod
    def _sort_entry_by(entry: Entry) -> datetime:

        return max([
            datetime.fromisoformat(translation[f"{KEY_MTIME:s}_datetime"])
            for translation in entry.translations
        ])


    def _build_data(self):

        if KEY_SEQUENCES not in self._context.keys():
            self._context[KEY_SEQUENCES] = {}

        assert self._name not in self._context[KEY_SEQUENCES].keys()
        self._context[KEY_SEQUENCES][self._name] = {
            KEY_ENTRIES: self._entries,
            **{
                language: [
                    entry[language]
                    for entry in self._entries
                    if entry[language] is not None
                ]
                for language in self._context[KEY_LANGUAGES]
            }
        }


    def _render_entries(self):

        for entry in self._entries:

            for translation in entry.translations:

                translation.render(
                    renderers = self._renderers,
                    languages = [
                        (language, entry[language][KEY_FN])
                        for language in entry.languages
                    ],
                    path = self._context[KEY_SRC][KEY_STAGING],
                    template = self._template.render,
                )
