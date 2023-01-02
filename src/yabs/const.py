# -*- coding: utf-8 -*-

"""

YABS
Yet Another Build System
https://github.com/pleiszenburg/yabs

    src/yabs/const.py: Const values and defaults

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

from unidecode import unidecode

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# VALUES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CONFIG_FILE = "site.yaml"

LOGGER = "YABS"

IMAGE_SUFFIX_LIST = ["gif", "jpg", "jpeg", "png", "webp"]
FONT_SUFFIX_LIST = ["ttf", "woff", "woff2", "otf"]

META_DELIMITER = "<<DELIMITER>>" # sequences

PID_FN = ".pid"
YABS_FN = "yabs.yaml"

UMLAUT_DICT = {
    ch: f'{unidecode(ch):s}e'
    for ch in "äöüÄÖÜ"
}

KEY_ABSTRACT = "abstract"
KEY_AUTHORS = "authors"
KEY_BASE = "base"
KEY_BOKEH = "bokeh"
KEY_CODE = "code"
KEY_CONTENT = "content"
KEY_CONTEXT = "context"
KEY_COLORS = "colors"
KEY_CTIME = "ctime"
KEY_CWD = "cwd"
KEY_DATA = "data"
KEY_DEPLOY = "deploy"
KEY_DESCRIPTION = "description"
KEY_DOMAIN = "domain"
KEY_EMAIL = "email"
KEY_ENTRIES = "entries"
KEY_ENTRY = "entry"
KEY_EXTENDS = "extends"
KEY_FIGURE = "fig"
KEY_FIRSTNAME = "firstname"
KEY_FN = "fn"
KEY_FONTS = "fonts"
KEY_FOOTNOTES = "footnotes"
KEY_FORMULA = "formula"
KEY_GITHUB = "github"
KEY_HTML = "html"
KEY_HOSTNAME = "hostname"
KEY_ID = "id"
KEY_IGNORE = "ignore"
KEY_IMAGE = "image"
KEY_IMAGES = "images"
KEY_JINJA = "jinja"
KEY_LANGUAGE = "language"
KEY_LANGUAGES = "languages"
KEY_LASTNAME = "lastname"
KEY_LIBRARIES = "libraries"
KEY_LOG = "log"
KEY_MARKDOWN = "md"
KEY_MATH = "math"
KEY_MOUNTPOINT = "mountpoint"
KEY_MTIME = "mtime"
KEY_NAME = "name"
KEY_NAVIGATION = "navigation"
KEY_OUT = "out"
KEY_PATH = "path"
KEY_PASSWORD = "password"
KEY_PLACEHOLDER = "placeholder"
KEY_PLOT = "plot"
KEY_PLOTS = "plots"
KEY_PLOTLY = "plotly"
KEY_PORT = "port"
KEY_POST = "post"
KEY_PREFIX = "prefix"
KEY_PROJECT = "project"
KEY_RECIPE = "recipe"
KEY_RENDERER = "renderer"
KEY_RELEASE = "release"
KEY_ROOT = "root"
KEY_SCRIPT = "script"
KEY_SCRIPTS = "scripts"
KEY_SEQUENCES = "sequences"
KEY_SERVER = "server"
KEY_SIZE = "size"
KEY_SLUG = "slug"
KEY_SRC = "src"
KEY_STAGING = "staging"
KEY_STATIC = "static"
KEY_STYLE = "style"
KEY_STYLES = "styles"
KEY_SUBTITLE = "subtitle"
KEY_TAGS = "tags"
KEY_TARGET = "target"
KEY_TARGETS = "targets"
KEY_TEMPLATE = "template"
KEY_TEMPLATES = "templates"
KEY_THEME = "theme"
KEY_TIMER = "timer"
KEY_TITLE = "title"
KEY_TYPE = "type"
KEY_UPDATE = "update"
KEY_URL = "url"
KEY_USER = "user"
KEY_WARNING = "warning"
KEY_VARIANTS = "variants"
KEY_VERSION = "version"
KEY_VIDEO = "video"
