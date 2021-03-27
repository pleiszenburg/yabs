# -*- coding: utf-8 -*-


import glob
import os
import random
from typing import Dict

from typeguard import typechecked

from ..const import (
    KEY_DOMAIN,
    KEY_OUT,
    KEY_PREFIX,
    KEY_ROOT,
)


HASH_DIGITS = 8


@typechecked
def run(context: Dict, options: Dict):

    disallow_prefix = options[f"disallow_{KEY_PREFIX:s}"] # list

    allow_files = []
    disallow_files = []

    for file_path in glob.glob(os.path.join(context[KEY_OUT][KEY_ROOT], "*.htm*")):

        fn = os.path.basename(file_path)

        if any(fn.startswith(prefix) for prefix in disallow_prefix):
            disallow_files.append(fn)
        else:
            allow_files.append(fn)

    cnt = """# revision {revision}

	User-agent: Mediapartners-Google
	Disallow: /

	User-agent: *
	{allow_list}
	{disallow_list}
	Sitemap: http://www.{domain}/sitemap.xml
	""".format(
        revision=(
            ("%0" + str(HASH_DIGITS) + "x") % random.randrange(16 ** HASH_DIGITS)
        ),
        allow_list="\n".join(["Allow: /%s" % item for item in allow_files]),
        disallow_list="\n".join(["Disallow: /%s" % item for item in disallow_files]),
        domain=context[KEY_DOMAIN],
    )

    cnt = "\n".join([line.strip() for line in cnt.split("\n")])

    with open(os.path.join(context[KEY_OUT][KEY_ROOT], "robots.txt"), "w") as f:
        f.write(cnt)
