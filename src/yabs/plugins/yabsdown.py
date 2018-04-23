# -*- coding: utf-8 -*-


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from pprint import pprint as pp
import re


from yabs.const import (
	IMAGE_SUFFIX_LIST,
	KEY_CODE,
	KEY_FORMULA,
	KEY_MATH,
	KEY_LANGUAGE,
	KEY_VOCABULARY
	)


import mistune

from bs4 import BeautifulSoup


# Inspired by
# https://github.com/jupyter/nbconvert/blob/master/nbconvert/filters/markdown_mistune.py


class MathBlockGrammar(mistune.BlockGrammar):
	"""This defines a single regex comprised of the different patterns that
	identify math content spanning multiple lines. These are used by the
	MathBlockLexer.
	"""


	multi_math_str = '|'.join([
		r'^\$\$.*?\$\$',
		r'^\\\\\[.*?\\\\\]',
		r'^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}'
		])

	multiline_math = re.compile(multi_math_str, re.DOTALL)


class MathBlockLexer(mistune.BlockLexer):
	""" This acts as a pass-through to the MathInlineLexer. It is needed in
	order to avoid other block level rules splitting math sections apart.
	"""


	default_rules = (['multiline_math'] + mistune.BlockLexer.default_rules)


	def __init__(self, rules = None, **kwargs):

		if rules is None:
			rules = MathBlockGrammar()
		super(MathBlockLexer, self).__init__(rules, **kwargs)


	def parse_multiline_math(self, m):
		"""Add token to pass through mutiline math."""

		self.tokens.append({
			'type': 'multiline_math',
			'text': m.group(0)
			})


class MathInlineGrammar(mistune.InlineGrammar):
	"""This defines different ways of declaring math objects that should be
	passed through to mathjax unaffected. These are used by the MathInlineLexer.
	"""


	inline_math = re.compile(r'^\$(.+?)\$|^\\\\\((.+?)\\\\\)', re.DOTALL)

	block_math = re.compile(r'^\$\$(.*?)\$\$|^\\\\\[(.*?)\\\\\]', re.DOTALL)

	latex_environment = re.compile(r'^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}', re.DOTALL)

	text = re.compile(r'^[\s\S]+?(?=[\\<!\[_*`~$]|https?://| {2,}\n|$)')


class MathInlineLexer(mistune.InlineLexer):
	"""This interprets the content of LaTeX style math objects using the rules
	defined by the MathInlineGrammar.

	In particular this grabs ``$$...$$``, ``\\[...\\]``, ``\\(...\\)``, ``$...$``,
	and ``\begin{foo}...\end{foo}`` styles for declaring mathematics. It strips
	delimiters from all these varieties, and extracts the type of environment
	in the last case (``foo`` in this example).
	"""


	default_rules = ([
		'block_math',
		'inline_math',
		'latex_environment'
		] + mistune.InlineLexer.default_rules)


	def __init__(self, renderer, rules=None, **kwargs):

		if rules is None:
			rules = MathInlineGrammar()
		super(MathInlineLexer, self).__init__(renderer, rules, **kwargs)


	def output_inline_math(self, m):

		return self.renderer.inline_math(m.group(1) or m.group(2))


	def output_block_math(self, m):

		return self.renderer.block_math(m.group(1) or m.group(2) or "")


	def output_latex_environment(self, m):

		return self.renderer.latex_environment(m.group(1), m.group(2))


class MarkdownWithMath(mistune.Markdown):


	def __init__(self, renderer, **kwargs):

		if 'inline' not in kwargs:
			kwargs['inline'] = MathInlineLexer
		if 'block' not in kwargs:
			kwargs['block'] = MathBlockLexer
		super(MarkdownWithMath, self).__init__(renderer, **kwargs)


	def output_multiline_math(self):

		return self.inline(self.token['text'])


class RendererWithMath(mistune.Renderer):


	def __init__(self, *args, **kwargs):

		super(RendererWithMath, self).__init__(*args, **kwargs)

		self.counter_dict = {'fig': 0, 'vid': 0, KEY_FORMULA: 0}


	def block_code(self, code, lang):

		if not lang:
			raise
			# return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)

		return self.options[KEY_CODE](code, lang)


	def block_math(self, text):

		self.counter_dict[KEY_FORMULA] += 1

		return self.options[KEY_TEMPLATES][KEY_FORMULA].render(
			formula = self.options[KEY_MATH](text),
			number = self.counter_dict[KEY_FORMULA]
			)


	def latex_environment(self, name, text):

		return r'\begin{%s}%s\end{%s}' % (name, text, name)


	def inline_math(self, text):

		return '%s' % self.options[KEY_MATH](text)


	def paragraph(self, text):

		text_strip = text.strip(' ')
		test_soup_list = list(BeautifulSoup(text_strip, 'html.parser'))

		if len(test_soup_list) == 1 and test_soup_list[0].name == 'img':
			return self._figure(
				test_soup_list[0].attrs['src'],
				test_soup_list[0].attrs['title'] if 'title' in test_soup_list[0].attrs.keys() else '',
				test_soup_list[0].attrs['alt']
				)

		return '<p>%s</p>\n' % text_strip


	def _figure(self, src, title, text):

		if any(src.endswith(item) for item in IMAGE_SUFFIX_LIST):
			self.counter_dict['fig'] += 1
			return self.options[KEY_TEMPLATES]['figure_image'].render(
				alt_attr = text,
				alt_html = text,
				number = self.counter_dict['fig'],
				prefix = self.options[KEY_VOCABULARY][self.options[KEY_LANGUAGE]]['fig'],
				src = src,
				title = title
				)

		if src.startswith('youtube:'):
			self.counter_dict['vid'] += 1
			return self.options[KEY_TEMPLATES]['figure_video'].render(
				alt_html = text,
				number = self.counter_dict['vid'],
				prefix = self.options[KEY_VOCABULARY][self.options[KEY_LANGUAGE]]['vid'],
				video_id = src.split(':')[1]
				)

		raise # handle youtube, plots, etc HERE!


def run(context, options = None):

	if options is None:
		options = {}

	return MarkdownWithMath(
		renderer = RendererWithMath(**options)
			# vocabulary = options[KEY_VOCABULARY]
			# language = options[KEY_LANGUAGE],
			# code = options[KEY_CODE],
			# math = options[KEY_MATH]
			# templates = options[KEY_TEMPLATES]
		)
