# -*- coding: utf-8 -*-


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


def render_code(code, lang):

	return highlight(
		code,
		get_lexer_by_name(lang, stripall = True),
		html.HtmlFormatter()
		)


def run(context, options = None):

	return render_code
