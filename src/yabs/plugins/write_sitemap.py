# -*- coding: utf-8 -*-


import datetime
import glob
import os


from yabs.const import (
    AJAX_PREFIX,
    BLOG_PREFIX,
    KEY_BLOG,
    KEY_CTIME,
    KEY_DATA,
    KEY_DOMAIN,
    KEY_ENTRY,
    KEY_FN,
    KEY_MTIME,
    KEY_OUT,
    KEY_ROOT,
)


def run(context, options=None):
    def get_datestring_now():
        cur_date = datetime.datetime.now()
        return "%04d-%02d-%02d" % (cur_date.year, cur_date.month, cur_date.day)

    def get_lastmod(fn):
        if not fn.startswith(BLOG_PREFIX):
            return current_date_str
        blog_entry_meta_dict = None
        for entry in context[KEY_DATA][KEY_BLOG]["%s_list" % KEY_ENTRY]:
            if entry[KEY_FN] == fn:
                blog_entry_meta_dict = entry
                break
        if blog_entry_meta_dict is None:
            raise  # TODO
        if KEY_MTIME in blog_entry_meta_dict.keys():
            blog_date_str = blog_entry_meta_dict[KEY_MTIME]
        else:
            blog_date_str = blog_entry_meta_dict[KEY_CTIME]
        return blog_date_str.split(" ")[0]

    def get_priority(fn):
        if fn.startswith("index"):
            return 1.0
        elif fn.startswith(BLOG_PREFIX):
            return 0.5
        elif fn.startswith("plot_"):
            return 0.25
        else:
            return 0.75

    def generate_entry(fn):
        return """<url>
		<loc>http://www.{domain}/{filename}</loc>
		<lastmod>{lastmod}</lastmod>
		<changefreq>weekly</changefreq>
		<priority>{priority}</priority>
		</url>""".format(
            domain=context[KEY_DOMAIN],
            filename=fn,
            lastmod=get_lastmod(fn),
            priority="%0.2f" % get_priority(fn),
        )

    file_list = []

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], "*.htm*")):
        fn = os.path.basename(file_path)
        if not fn.startswith(AJAX_PREFIX):
            file_list.append(fn)

    current_date_str = get_datestring_now()

    cnt = """<?xml version="1.0" encoding="UTF-8"?>
	<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	{entries}
	</urlset>
	""".format(
        entries="\n".join([generate_entry(fn) for fn in file_list])
    )

    cnt = "\n".join([line.strip() for line in cnt.split("\n")])

    with open(os.path.join(context[KEY_OUT][KEY_ROOT], "sitemap.xml"), "w") as f:
        f.write(cnt)
