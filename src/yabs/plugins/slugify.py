# -*- coding: utf-8 -*-


from slugify import slugify
from unidecode import unidecode


UMLAUT_LIST = [i for i in 'äöü']
UMLAUT_LIST += [i.upper() for i in UMLAUT_LIST]
UMLAUT_DICT = {i: unidecode(i) for i in UMLAUT_LIST}


def slugify_costom(slug_str):

	for umlaut in UMLAUT_DICT.keys():
		slug_str = slug_str.replace(umlaut, UMLAUT_DICT[umlaut])

	return slugify(slug_str, lowercase = False)


def run(context, options = None):

	return slugify_costom
