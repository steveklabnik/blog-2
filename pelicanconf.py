#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Joshua R. Rodgers'
SITENAME = 'The Enginerd'
SITEURL = 'http://mr-byte.github.io/blog'

GITHUB_URL = 'http://github.com/mr-byte/blog'

PATH = 'Programming'

TIMEZONE = 'America/Denver'

DEFAULT_LANG = 'en'

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'atom.xml'
CATEGORY_FEED_ATOM = 'categories/%s/atom.xml'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

ARCHIVES_SAVE_AS = 'blog/archives/index.html'

CATEGORY_URL = 'categories/{slug}/'
CATEGORY_SAVE_AS = 'categories/{slug}/index.html'

DEFAULT_PAGINATION = 10
