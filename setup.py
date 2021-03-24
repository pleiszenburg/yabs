# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    setup.py: Used for package distribution

    Copyright (C) 2018-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/yabs/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from setuptools import find_packages, setup

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

setup(
    author="Sebastian M. Ernst",
    author_email="ernst@pleiszenburg.de",
    classifiers=["Development Status :: 3 - Alpha", "Topic :: Utilities"],
    description="Yet Another Build System",
    download_url="https://github.com/pleiszenburg/yabs",
    entry_points="""
		[console_scripts]
		yabs = yabs:yabs_cli
		""",
    extras_require={},
    include_package_data=True,
    install_requires=[],
    keywords=[],
    license="NONE",
    long_description="",
    name="yabs",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/pleiszenburg/yabs",
    version="0.0.0",
    zip_safe=False,
)
