# -*- coding: utf-8 -*-

from .blog import Blog

def run(context, options=None):

    blog = Blog(context, options)
    blog.render_entries()
    blog.build_data()
