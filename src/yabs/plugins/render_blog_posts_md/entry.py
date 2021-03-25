# -*- coding: utf-8 -*-


import os
from typing import Callable, Dict, List, Union

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
    META_DELIMITER,
)


class Entry:
    """
    One blog post / entry.

    Mutable.
    """

    def __init__(self, context: Dict, src_file_path: str, slug_func: Callable):

        self._context = context
        self._slug_func = slug_func

        with open(src_file_path, "r") as f:
            raw = f.read()
        meta, content = raw.split(META_DELIMITER, 1)

        self._meta_dict = self._process_meta(src_file_path, meta.strip())
        self._meta_dict[KEY_CONTENT] = content.strip()

    @property
    def meta_dict(self) -> Dict:

        return self._meta_dict

    @staticmethod
    def _process_author(in_data: Union[Dict[str, str], str]) -> Dict[str, str]:

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

    def _process_meta(self, src_file_path: str, meta: str) -> Dict:

        fn = os.path.basename(src_file_path)

        meta_dict = {
            KEY_LANGUAGE: fn.rsplit(".", 1)[0].rsplit("_", 1)[1],
            KEY_ID: fn.rsplit(".", 1)[0].rsplit("_", 1)[0],
            **load(meta, Loader=Loader),
        }

        meta_dict[KEY_AUTHORS] = [
            self._process_author(author)
            for author in meta_dict[KEY_AUTHORS]
        ]

        if KEY_MTIME not in meta_dict.keys():
            meta_dict[KEY_MTIME] = meta_dict[KEY_CTIME]
        for time_key in [KEY_CTIME, KEY_MTIME]:
            meta_dict["%s_datetime" % time_key] = meta_dict[time_key].replace(" ", "T")

        meta_dict[KEY_FN] = "%s%s.htm" % (
            BLOG_PREFIX,
            self._slug_func(meta_dict[KEY_TITLE]),
        )

        return meta_dict

    @staticmethod
    def _fix_headline_levels(html: str) -> str:

        soup = BeautifulSoup(html, "html.parser")

        for h_level in range(5, 0, -1):
            for h_tag in soup.find_all("h%d" % h_level):
                if h_tag.has_attr("class"):
                    if "article_headline" in h_tag["class"]:
                        continue
                h_tag.name = "h%d" % (h_level + 1)

        return str(soup)  # soup.prettify()

    def render(self, renderer_dict: Dict, entry_language_list: List[str]):

        renderer = renderer_dict[self._meta_dict[KEY_LANGUAGE]]

        self._meta_dict[KEY_ABSTRACT] = renderer(self._meta_dict[KEY_ABSTRACT])
        self._meta_dict[KEY_CONTENT] = renderer(self._meta_dict[KEY_CONTENT])

        for template_prefix, prefix in (
            (KEY_BASE, ""),
            (f"{AJAX_PREFIX:s}{KEY_BASE:s}", AJAX_PREFIX),
        ):

            with open(
                os.path.join(
                    self._context[KEY_OUT][KEY_ROOT], prefix + self._meta_dict[KEY_FN]
                ),
                "w+",
            ) as f:

                f.write(
                    self._fix_headline_levels(
                        self._context[KEY_TEMPLATES]["blog_article"].render(
                            **{
                                KEY_LANGUAGES: str(entry_language_list),
                                KEY_TEMPLATE: template_prefix,
                            },
                            **self._meta_dict
                        )
                    )
                )
