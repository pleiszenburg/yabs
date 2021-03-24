# -*- coding: utf-8 -*-


import glob
import os
from typing import Any, Dict

from typeguard import typechecked

from ...const import (
    KEY_BLOG,
    KEY_CODE,
    KEY_DATA,
    KEY_ENTRY,
    KEY_FN,
    KEY_ID,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_MARKDOWN,
    KEY_MATH,
    KEY_PROJECT,
    KEY_SLUG,
    KEY_SRC,
    KEY_TEMPLATES,
    KEY_VOCABULARY,
)
from .entry import Entry


@typechecked
class Blog:
    """
    An entire blog with multiple entries.

    Mutable.
    """

    def __init__(self, context: Dict, options: Any = None):

        self.context = context
        self.slug = self.context[KEY_PROJECT].run_plugin(options[KEY_SLUG])

        self.entry_list = [
            Entry(context, file_path, self.slug)
            for file_path in glob.glob(
                os.path.join(self.context[KEY_SRC][KEY_BLOG], "**", "*.%s" % KEY_MARKDOWN),
                recursive=True,
            )
        ]
        self.entry_dict = self._match_language_versions()

        self.renderer_dict = {
            language: self.context[KEY_PROJECT].run_plugin(
                options[KEY_MARKDOWN],
                {
                    KEY_CODE: self.context[KEY_PROJECT].run_plugin(options[KEY_CODE]),
                    KEY_MATH: self.context[KEY_PROJECT].run_plugin(options[KEY_MATH]),
                    KEY_VOCABULARY: self.context[KEY_VOCABULARY][language],
                    KEY_TEMPLATES: self.context[KEY_TEMPLATES],
                    KEY_LANGUAGE: language,
                },
            )
            for language in {entry.meta_dict[KEY_LANGUAGE] for entry in self.entry_list}
        }

    def _match_language_versions(self):

        entry_dict = {}

        for entry in self.entry_list:

            if entry.meta_dict[KEY_ID] not in entry_dict.keys():
                entry_dict[entry.meta_dict[KEY_ID]] = []
            entry_dict[entry.meta_dict[KEY_ID]].append(
                (entry.meta_dict[KEY_LANGUAGE], entry.meta_dict[KEY_FN])
            )

        languages_set = set(self.context[KEY_LANGUAGES])

        for entry_key in entry_dict.keys():

            entry_languages = set([lang for lang, _ in entry_dict[entry_key]])
            missing_translations = languages_set - entry_languages
            for lang in missing_translations:
                entry_dict[entry_key].append((lang, str(None)))
            entry_dict[entry_key].sort()

        return entry_dict

    def build_data(self):

        if KEY_DATA not in self.context.keys():
            self.context[KEY_DATA] = {}

        self.context[KEY_DATA][KEY_BLOG] = {
            "%s_list" % KEY_ENTRY: [entry.meta_dict for entry in self.entry_list],
            "%s_dict" % KEY_ENTRY: self.entry_dict,
        }

    def render_entries(self):

        for entry in self.entry_list:
            entry.render(self.renderer_dict, self.entry_dict[entry.meta_dict[KEY_ID]])
