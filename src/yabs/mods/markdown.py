
from pprint import pprint as pp
import re

import mistune

from bs4 import BeautifulSoup

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from yaml import load, dump # PyYAML
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

import jinja2

from katex import katex


# https://github.com/jupyter/nbconvert/blob/master/nbconvert/filters/markdown_mistune.py


class MathBlockGrammar(mistune.BlockGrammar):
	"""This defines a single regex comprised of the different patterns that
	identify math content spanning multiple lines. These are used by the
	MathBlockLexer.
	"""
	multi_math_str = "|".join([
		r"^\$\$.*?\$\$",
		r"^\\\\\[.*?\\\\\]",
		r"^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}"
		])
	multiline_math = re.compile(multi_math_str, re.DOTALL)


class MathBlockLexer(mistune.BlockLexer):
	""" This acts as a pass-through to the MathInlineLexer. It is needed in
	order to avoid other block level rules splitting math sections apart.
	"""

	default_rules = (['multiline_math'] + mistune.BlockLexer.default_rules)

	def __init__(self, rules=None, **kwargs):
		if rules is None:
			rules = MathBlockGrammar()
		super(MathBlockLexer, self).__init__(rules, **kwargs)

	def parse_multiline_math(self, m):
		"""Add token to pass through mutiline math."""
		self.tokens.append({
			"type": "multiline_math",
			"text": m.group(0)
			})


class MathInlineGrammar(mistune.InlineGrammar):
	"""This defines different ways of declaring math objects that should be
	passed through to mathjax unaffected. These are used by the MathInlineLexer.
	"""
	inline_math = re.compile(r"^\$(.+?)\$|^\\\\\((.+?)\\\\\)", re.DOTALL)
	block_math = re.compile(r"^\$\$(.*?)\$\$|^\\\\\[(.*?)\\\\\]", re.DOTALL)
	latex_environment = re.compile(r"^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}", re.DOTALL)
	text = re.compile(r'^[\s\S]+?(?=[\\<!\[_*`~$]|https?://| {2,}\n|$)')



class MathInlineLexer(mistune.InlineLexer):
	"""This interprets the content of LaTeX style math objects using the rules
	defined by the MathInlineGrammar.

	In particular this grabs ``$$...$$``, ``\\[...\\]``, ``\\(...\\)``, ``$...$``,
	and ``\begin{foo}...\end{foo}`` styles for declaring mathematics. It strips
	delimiters from all these varieties, and extracts the type of environment
	in the last case (``foo`` in this example).
	"""
	default_rules = (['block_math', 'inline_math', 'latex_environment'] + mistune.InlineLexer.default_rules)

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
		return self.inline(self.token["text"])



class RendererWithMath(mistune.Renderer):


	vocabulary_dict = {
		'de': {
			'fig': 'Abbildung',
			'vid': 'Video'
			},
		'en': {
			'fig': 'figure',
			'vid': 'video'
			}
		}
	counter_dict = {
		'fig': 0,
		'vid': 0,
		'formula': 0
		}


	def __init__(self, *args, **kwargs):

		super(RendererWithMath, self).__init__(*args, **kwargs)

		self.j_env = env = jinja2.Environment(
			loader = jinja2.FileSystemLoader('templates', encoding = 'utf-8', followlinks = False),
			autoescape = jinja2.select_autoescape(['html', 'xml'])
			)
		self.j_templates = {
			name: env.get_template('%s.htm' % name) for name in ['figure_image', 'figure_video', 'formula']
			}


	# Code >> pygments
	def block_code(self, code, lang):

		if not lang:
			raise
			# return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)

		lexer = get_lexer_by_name(lang, stripall = True)
		formatter = html.HtmlFormatter()
		return highlight(code, lexer, formatter)


	def block_math(self, text):
		self.counter_dict['formula'] += 1
		return self.j_templates['formula'].render(
			formula = katex(text),
			number = self.counter_dict['formula']
			)


	def latex_environment(self, name, text):
		return r'\begin{%s}%s\end{%s}' % (name, text, name)


	def inline_math(self, text):
		return '%s' % katex(text)


	# Images & Tables >> HTML5 Figure
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

		if any(src.endswith(item) for item in ['png', 'jpg', 'gif']):
			self.counter_dict['fig'] += 1
			return self.j_templates['figure_image'].render(
				alt_attr = text,
				alt_html = text,
				number = self.counter_dict['fig'],
				prefix = self.vocabulary_dict[self.options['lang']]['fig'],
				src = src,
				title = title
				)

		if src.startswith('youtube:'):
			self.counter_dict['vid'] += 1
			return self.j_templates['figure_video'].render(
				alt_html = text,
				number = self.counter_dict['vid'],
				prefix = self.vocabulary_dict[self.options['lang']]['vid'],
				video_id = src.split(':')[1]
				)

		raise # handle youtube, plots, etc HERE!


def render():

	with open('test_mistune_demo.md', 'r') as f:
		cnt_in = f.read()

	markdown_de = MarkdownWithMath(renderer = RendererWithMath(lang = 'de')) # inline = InlineLexer, block = BlockLexer

	meta_raw, cnt_raw = cnt_in.split('\n\n', 1)

	cnt_out = markdown_de(cnt_raw)

	pp(load(meta_raw, Loader = Loader))

	# HACK
	cnt_out = '<meta charset="utf-8"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css">\n' + cnt_out

	with open('test_mistune_demo.htm', 'w') as f:
		f.write(cnt_out)

if __name__ == '__main__':
	render()
