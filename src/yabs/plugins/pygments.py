# -*- coding: utf-8 -*-


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


def render_code(code, lang):

	tmp = highlight(
		code,
		get_lexer_by_name(lang, stripall = True),
		html.HtmlFormatter()
		)
	return tmp.replace('<div ', '<figure ').replace('</div>', '</figure>')


def run(context, options = None):

	return render_code
