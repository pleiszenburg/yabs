# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/plugins/render_sequence/entry.py: A sequence entry

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

from typing import List, Set, Union

from typeguard import typechecked

from .translation import Translation

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Entry:
    """
    All translations of a post / entry.

    Mutable.
    """

    def __init__(self, id: str):

        self._id = id
        self._translations = {}


    def __getitem__(self, language: str) -> Union[Translation, None]:

        try:
            return self._translations[language]
        except KeyError:
            return None


    def add(self, translation: Translation):

        assert translation.id == self._id
        assert translation.language not in self._translations.keys()

        self._translations[translation.language] = translation


    @property
    def languages(self) -> Set[str]:

        return set(self._translations.keys())


    @property
    def translations(self) -> List[Translation]:

        return list(self._translations.values())
