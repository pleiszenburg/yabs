# -*- coding: utf-8 -*-


import os

from bs4 import BeautifulSoup
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from ...const import (
    AJAX_PREFIX,
    BLOG_PREFIX,
    KEY_ABSTRACT,
    KEY_AUTHORS,
    KEY_BASE,
    KEY_CONTENT,
    KEY_CTIME,
    KEY_EMAIL,
    KEY_FIRSTNAME,
    KEY_FN,
    KEY_ID,
    KEY_LANGUAGE,
    KEY_LANGUAGES,
    KEY_LASTNAME,
    KEY_MTIME,
    KEY_OUT,
    KEY_ROOT,
    KEY_TEMPLATE,
    KEY_TEMPLATES,
    KEY_TITLE,
)


class Entry:
    """
    One blog post / entry.

    Mutable.
    """

    def __init__(self, context, src_file_path, slug_func):

        def get_entry_segments():
            with open(src_file_path, "r") as f:
                raw = f.read()
            return raw.split("\n\n", 1)

        self.context = context
        self.slug_func = slug_func

        meta, content = get_entry_segments()
        self.meta_dict = self.__process_meta__(src_file_path, meta)
        self.meta_dict[KEY_CONTENT] = content

    def __process_meta__(self, src_file_path, meta):

        def process_author(in_data):

            if isinstance(in_data, str):
                lastname, firstname = in_data.split(",")
                email = ""
            elif isinstance(in_data, dict):
                lastname, firstname = list(in_data.keys())[0].split(",")
                email = list(in_data.values())[0].strip()
            else:
                raise TypeError('unhandled author datatype')

            return {
                KEY_LASTNAME: lastname.strip(),
                KEY_FIRSTNAME: firstname.strip(),
                KEY_EMAIL: email,
            }

        fn = os.path.basename(src_file_path)

        meta_dict = {
            KEY_LANGUAGE: fn.rsplit(".", 1)[0].rsplit("_", 1)[1],
            KEY_ID: fn.rsplit(".", 1)[0].rsplit("_", 1)[0],
            **load(meta, Loader=Loader),
        }

        meta_dict[KEY_AUTHORS] = [
            process_author(author) for author in meta_dict[KEY_AUTHORS]
        ]

        if KEY_MTIME not in meta_dict.keys():
            meta_dict[KEY_MTIME] = meta_dict[KEY_CTIME]
        for time_key in [KEY_CTIME, KEY_MTIME]:
            meta_dict["%s_datetime" % time_key] = meta_dict[time_key].replace(" ", "T")

        meta_dict[KEY_FN] = "%s%s.htm" % (
            BLOG_PREFIX,
            self.slug_func(meta_dict[KEY_TITLE]),
        )

        return meta_dict

    def render(self, renderer_dict, entry_language_list):
        def fix_headline_levels(html):
            soup = BeautifulSoup(html, "html.parser")
            for h_level in range(5, 0, -1):
                for h_tag in soup.find_all("h%d" % h_level):
                    if h_tag.has_attr("class"):
                        if "article_headline" in h_tag["class"]:
                            continue
                    h_tag.name = "h%d" % (h_level + 1)
            return str(soup)  # soup.prettify()

        renderer = renderer_dict[self.meta_dict[KEY_LANGUAGE]]

        self.meta_dict[KEY_ABSTRACT] = renderer(self.meta_dict[KEY_ABSTRACT])
        self.meta_dict[KEY_CONTENT] = renderer(self.meta_dict[KEY_CONTENT])

        for template_prefix, prefix in [
            (KEY_BASE, ""),
            ("%s%s" % (AJAX_PREFIX, KEY_BASE), AJAX_PREFIX),
        ]:

            with open(
                os.path.join(
                    self.context[KEY_OUT][KEY_ROOT], prefix + self.meta_dict[KEY_FN]
                ),
                "w+",
            ) as f:

                f.write(
                    fix_headline_levels(
                        self.context[KEY_TEMPLATES]["blog_article"].render(
                            **{
                                KEY_LANGUAGES: str(entry_language_list),
                                KEY_TEMPLATE: template_prefix,
                            },
                            **self.meta_dict
                        )
                    )
                )
