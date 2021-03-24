# -*- coding: utf-8 -*-


import glob
import os


from yabs.const import (
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


class Blog:

    def __init__(self, context, options):

        self.context = context
        self.slug = self.context[KEY_PROJECT].run_plugin(options[KEY_SLUG])

        src_file_list = glob.glob(
            os.path.join(self.context[KEY_SRC][KEY_BLOG], "**", "*.%s" % KEY_MARKDOWN),
            recursive=True,
        )

        self.entry_list = [
            Entry(context, file_path, self.slug)
            for file_path in src_file_list
        ]
        self.language_set = set(
            [entry.meta_dict[KEY_LANGUAGE] for entry in self.entry_list]
        )
        self.__match_language_versions__()

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
            for language in self.language_set
        }

    def __match_language_versions__(self):

        self.entry_dict = {}

        for entry in self.entry_list:
            if entry.meta_dict[KEY_ID] not in self.entry_dict.keys():
                self.entry_dict[entry.meta_dict[KEY_ID]] = []
            self.entry_dict[entry.meta_dict[KEY_ID]].append(
                (entry.meta_dict[KEY_LANGUAGE], entry.meta_dict[KEY_FN])
            )

        languages_set = set(self.context[KEY_LANGUAGES])
        for entry_key in self.entry_dict.keys():
            entry_languages = set([lang for lang, _ in self.entry_dict[entry_key]])
            missing_translations = languages_set - entry_languages
            for lang in missing_translations:
                self.entry_dict[entry_key].append((lang, str(None)))
            self.entry_dict[entry_key].sort()

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
