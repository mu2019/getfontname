#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(name = 'getfontname',
      version = '0.0.1',
      description = 'get font name from the ttf/ttc font file.',
      author = 'Chen MuSheng',
      author_email = 'sheng.2179@gmail.com',
      url = 'https://github.com/mu2019/getfontname/',
      license='MIT',
      platforms = 'any',
      packages=['getfontname']
      #py_modules = find_packages(), # ['getfontname'],
      #scripts=['getfontname/fontname.py','getfontname/fontfile.py','getfontname/__init__.py'],
      )
      