# -*- coding: utf-8 -*-


import glob
import os


import jinja2


from yabs.const import (
    KEY_DATA,
    KEY_DOMAIN,
    KEY_JINJA,
    KEY_SRC,
    KEY_TEMPLATES,
    KEY_VOCABULARY,
)


def run(context, options=None):

    context[KEY_JINJA] = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            context[KEY_SRC][KEY_TEMPLATES], encoding="utf-8", followlinks=False
        ),
        autoescape=False,  # jinja2.select_autoescape(enabled_extensions = ('html', 'xml', 'svg', 'jinja'))
    )
    context[KEY_JINJA].globals.update({
        KEY_DOMAIN: context[KEY_DOMAIN],
        KEY_VOCABULARY: context[KEY_VOCABULARY],
    })
    if KEY_DATA in context.keys():
        context[KEY_JINJA].globals.update({
            KEY_DATA: context[KEY_DATA],
        })

    context[KEY_TEMPLATES] = {
        name.rsplit(".", 1)[0]: context[KEY_JINJA].get_template(name)
        for name in [
            os.path.basename(fn)
            for fn in glob.glob(os.path.join(context[KEY_SRC][KEY_TEMPLATES], "*"))
            if os.path.isfile(fn)
        ]
    }
