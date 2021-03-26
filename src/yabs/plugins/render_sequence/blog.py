# -*- coding: utf-8 -*-


import glob
import os
from typing import Any, Dict

from typeguard import typechecked

from ...const import (
    KEY_BLOG,
    KEY_DATA,
    KEY_ENTRY,
    KEY_FN,
    KEY_ID,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_MARKDOWN,
    KEY_RENDERER,
    KEY_SRC,
)
from .entry import Entry


@typechecked
class Blog:
    """
    An entire blog with multiple entries.

    Mutable.
    """

    def __init__(self, context: Dict, options: Any):

        self._context = context

        self._entry_list = [
            Entry(context, file_path)
            for file_path in glob.glob(
                os.path.join(self._context[KEY_SRC][KEY_BLOG], "**", "*.%s" % KEY_MARKDOWN),
                recursive=True,
            )
        ]
        self._entry_dict = self._match_language_versions()

        self._renderer_dict = {
            language: context[KEY_MARKDOWN][options[KEY_RENDERER]]
            for language in context[KEY_LANGUAGES]
        }

    def _match_language_versions(self):

        entry_dict = {}

        for entry in self._entry_list:

            if entry.meta_dict[KEY_ID] not in entry_dict.keys():
                entry_dict[entry.meta_dict[KEY_ID]] = []
            entry_dict[entry.meta_dict[KEY_ID]].append(
                (entry.meta_dict[KEY_LANGUAGE], entry.meta_dict[KEY_FN])
            )

        languages_set = set(self._context[KEY_LANGUAGES])

        for entry_key in entry_dict.keys():

            entry_languages = set([lang for lang, _ in entry_dict[entry_key]])
            missing_translations = languages_set - entry_languages
            for lang in missing_translations:
                entry_dict[entry_key].append((lang, str(None)))
            entry_dict[entry_key].sort()

        return entry_dict

    def build_data(self):

        if KEY_DATA not in self._context.keys():
            self._context[KEY_DATA] = {}

        self._context[KEY_DATA][KEY_BLOG] = {
            "%s_list" % KEY_ENTRY: [entry.meta_dict for entry in self._entry_list],
            "%s_dict" % KEY_ENTRY: self._entry_dict,
        }

    def render_entries(self):

        for entry in self._entry_list:
            entry.render(self._renderer_dict, self._entry_dict[entry.meta_dict[KEY_ID]])
