# YABS

The surprised and appalled sound ones makes learning that there is "Yet Another Build System".

## Synopsis

YABS is a highly customizable system for creating build pipelines for static websites. Although it is inspired by systems like [Pelican](https://blog.getpelican.com/), [Sphinx](http://www.sphinx-doc.org) and [Lektor](https://www.getlektor.com/), it works at a somewhat lower level, providing a maximum of flexibility to end users while eliminating elements like a stiff, complex content management engine. YABS is intended to provide a thin layer - a Python wrapper - around a number of popular tools for building static websites, allowing to rapidly build just about anything ranging from small single page sites to large and complex blogs.

## Design

YABS is based on a minimal plugin system core: Every piece of build functionality is isolated into individual plugins, which can be chained up into custom pipelines and configured in project-specific configuration files. If a certain functionality is not provided by an existing YABS plugin, it is trivial to write your own and add it to the system. Every plugin is a stand-alone Python module exposing one single method which must accept two things - a project context object and an options parameter. If a certain plugin happens to be too slow for a certain use case, it can easily be optimized without interfering with other functionality.

## Features

YABS currently offers plugins for the following common [static] website build steps:

* a cleanup routine, plowing the ground for new builds
* a templating engine (thin wrapper around [Jinja2](jinja.pocoo.org))
* a markdown processor (extended [mistune](https://github.com/lepture/mistune))
* a data loader for [YAML](https://pyyaml.org/) & JSON data (exposing data to the templating engine)
* a [slugifier](https://github.com/un33k/python-slugify) (turning headlines into valid IDs and filenames)
* building & embedding interactive plots with [plotly](https://plot.ly/) and [bokeh](https://bokeh.pydata.org/)
* [syntax highlighting](http://pygments.org/) (rendered at build time)
* [math & formulas](https://khan.github.io/KaTeX/) (rendered at build time)
* code compression ([HTML](https://github.com/mankyd/htmlmin), [CSS](https://github.com/sprymix/csscompressor))
* code obfuscation / minimization ([JavaScript](http://lisperator.net/uglifyjs/))
* code transpilers ([between different versions of JavaScript](https://babeljs.io/); from [SASS/SCSS to CSS](https://sass.github.io/libsass-python/))
* code validation ([HTML](https://validator.github.io/validator/))
* inclusion of third party libraries ([JavaScript](http://browserify.org/), CSS)
* processing of font files
* processing of image files
* static file repository
* a favicon generator
* a robots.txt generator
* a sitemap.xml generator
* a htaccess generator
* a HTTP server for testing
* a symlink creator
* content deployment based on [sshfs](https://github.com/libfuse/sshfs)/sftp

If it is required to repeatedly run a small subset of a build pipeline e.g. for debugging, it is perfectly possible to do so.

## Installation

1. Check out the latest source code of YABS from its git repository: `git checkout [...]`
1. Change into the source folder of YABS: `cd yabs`
1. Create a new empty virtual environment named `env` with Python 3.8 or better: `python3 -m venv env`
1. Install YABS: `make install`
1. Activate the virtual environment: `source env/bin/activate`

## Basic usage

At a project root, first create a `site.yaml` configuration file. Once this has been done, you can use the following commands:

```bash
# Run the entire pipeline
yabs build
# Run a list of space-separated plugins
yabs run [plugins]
# Start the HTTP server
yabs server start
# Stop the HTTP server
yabs server stop
# Deploy the latest build to a pre-configured target
yabs deploy [target]
```
