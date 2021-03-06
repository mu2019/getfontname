#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .fontname import *
import platform
import os
import locale

LOCALMAP={
    'cp936':zh_cn
    }

class FontMapMate(type):
    _FontMap={}

    def __new__(mcl, name, bases, nmspc):
        FontMapMate._loadFontMap()
        return super(FontMapMate, mcl).__new__(mcl, name, bases, nmspc)

    @staticmethod
    def _loadFontMap(): #lang):
        '''
        lang: font name local language
        '''
        if platform.uname().system.upper() == 'WINDOWS':
            fontdir=[os.getenv('windir')+'/fonts']
            lang=LOCALMAP.get(locale.getdefaultlocale()[1],en_us)
        else:
            fontdir=['/usr/share/fonts','usr/share/fonts/truetype','~/.fonts']
            lang=en_us
            
        fonts=[]
        for fdir in fontdir:
            for f in os.listdir(fdir):
                if f[-4:].upper() in ('.OTF','.TTF','.TTC'):
                    fonts.append('%s/%s' % (fdir,f))
        for fn in fonts:
            otf=OTFName(fn,langid=lang)
            lfm=otf.getFontLocalInfo('Family')
            fm=otf.getFontInfo('Family')
            sfm=otf.getFontInfo('SubFamily')
            for i,f in enumerate(fm): #otf.getFontInfo('Id'):
                if f :
                    fid='%s-%s' % (f,sfm[i])
                    FontMapMate._FontMap[fid]=fn
                if lfm[i] :
                    fid='%s-%s' % (lfm[i],sfm[i])
                    FontMapMate._FontMap[fid]=fn
                
    @staticmethod
    def getFontFile(fontname,style='Regular'):
        '''
        style: Regular/常规,Bold/粗体
        '''
        fn='%s-%s' % (fontname,style)
        return FontMapMate._FontMap.get(fn)


class FontMap(metaclass=FontMapMate):
    def __init__(self):
        pass


get_font_file=FontMapMate.getFontFile

if __name__ == '__main__':
    ff=get_font_file('新宋体')
    
    print('font file',ff)
    
