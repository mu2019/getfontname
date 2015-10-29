#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getfontname
from getfontname import fontname,fontfile

ffilename=getfontname.get_font_file('宋体')
print('font file:', ffilename)

fname=getfontname.get_font_name(ffilename)
print('font name:',fname)
