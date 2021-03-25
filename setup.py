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

from setuptools import (
    find_packages,
    setup,
)
import ast
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_version(code: str) -> str:

    tree = ast.parse(code)

    for item in tree.body:
        if not isinstance(item, ast.Assign):
            continue
        if len(item.targets) != 1:
            continue
        if item.targets[0].id != "__version__":
            continue
        return item.value.s

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# List all versions of Python which are supported
python_minor_min = 8
python_minor_max = 9
confirmed_python_versions = [
    "Programming Language :: Python :: 3.{MINOR:d}".format(MINOR=minor)
    for minor in range(python_minor_min, python_minor_max + 1)
]

# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# Define source directory (path)
SRC_DIR = "src"

# Version
with open(os.path.join(SRC_DIR, "yabs", "__init__.py"), "r", encoding="utf-8") as f:
    __version__ = get_version(f.read())

# Requirements
with open("requirements_python.txt", "r", encoding="utf-8") as f:
    base_require = [line for line in f.read().split('\n') if len(line.strip()) > 0]
extras_require = {
    "base": base_require,
    "dev": [
        "black",
        "python-language-server[all]",
        "psutil",
        "setuptools",
        "Sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
        "twine",
        "wheel",
    ],
}
extras_require["all"] = list(
    {rq for target in extras_require.keys() for rq in extras_require[target]}
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

setup(
    author="Sebastian M. Ernst",
    author_email="ernst@pleiszenburg.de",
    classifiers=[
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha", "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
    + confirmed_python_versions
    + [
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    description="Yet Another Build System",
    entry_points={"console_scripts": ["yabs = yabs.cli:yabs_cli",],},
    extras_require=extras_require,
    include_package_data=True,
    install_requires=base_require,
    keywords=["static site generator", "build system"],
    license="LGPLv2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="yabs",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    python_requires=">=3.{MINOR:d}".format(MINOR=python_minor_min),
    url="https://github.com/pleiszenburg/yabs",
    download_url="https://github.com/pleiszenburg/yabs/archive/v%s.tar.gz" % __version__,
    version=__version__,
    zip_safe=False,
)
