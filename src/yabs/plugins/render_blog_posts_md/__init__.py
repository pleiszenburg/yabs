# -*- coding: utf-8 -*-

from typing import Any, Dict

from typeguard import typechecked

from .blog import Blog

@typechecked
def run(context: Dict, options: Any = None):

    blog = Blog(context, options)
    blog.render_entries()
    blog.build_data()
