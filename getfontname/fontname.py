#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack,calcsize
import sys
import platform,locale

# encoding id define

en_us=EN_US=1033
zh_cn=ZH_CN=2052
zh_tw=ZH_TW=1028

# name id define

FONT_COPYRIGHT=0
FONT_FAMILY=1
FONT_SUBFAMILY=2
FONT_ID=3
FONT_FULLNAME=4
FONT_VER=5
FONT_POSTSCRIPTNAME=6
FONT_TRADEMARK=7
FONT_MANUFACTURER=8
FONT_DESIGNER=9
FONT_DESCRIPTION=10
FONT_TYPOGRAPHICNAME=16
FONT_TYPOGRAPHICSUBNAME=17

#name id description map
FONTNAMEMAP={
    'CopyRight':0,
    'Family':1,
    'SubFamily':2,
    'Id':3,
    'FullName':4,
    'Version':5,
    'PostscriptNamge':6,
    'TradeMark':7,
    'Manufacture':8,
    'Designer':9,
    'TypographicName':16,
    'TypographicSubName':17
    }


LOCALMAP={
    'cp936':zh_cn
    }


'''
see The OpenType Font File detail in delow site
https://www.microsoft.com/typography/otspec/otff.htm

'''
_ttc_header_fmt='>4sHHL'
TTCHEADERSIZE=calcsize(_ttc_header_fmt)
        
class FontEntry():
    FormtStr='>HHHHHH'
    RawSize=calcsize(FormtStr)

    def __init__(self,rawstr):
        self.MajorVersion \
            ,self.MinorVersion \
            ,self.NumOfTables \
            ,self.SearchRange \
            ,self.EntrySelector \
            ,self.RangeShift \
        =unpack(self.FormtStr,rawstr)
        self.Tables={}
        self.Names={}
        self.LocalNames={}
        
class TableEntry():
    FormtStr='>4sLLL'
    RawSize=calcsize(FormtStr)
    
    def __init__(self,rawstr):
        '''
        offset: name tableentry
        '''
        tag \
                 ,self.CheckSum \
                 ,self.Offset \
                 ,self.Length \
        =unpack(self.FormtStr,rawstr)
        self.Tag=tag.decode('utf-8','replace')


class NameTableHeader():
    FormtStr='>HHH'
    RawSize=calcsize(FormtStr)
    
    def __init__(self,rawstr):
        '''
        Count: NameRecord numbers
        StringOffset: NameString area offset start of the table
        '''
        self.Selector \
                 ,self.Count \
                 ,self.StringOffset \
        =unpack(self.FormtStr,rawstr)
        
class NameRecord():
    FormtStr='>HHHHHH'
    RawSize=calcsize(FormtStr)

    def __init__(self,rawstr):
        '''
        Offset: offset from start of the NameString area
        '''
        self.PlatformId \
                 ,self.EncodingId \
                 ,self.LangId \
                 ,self.NameId \
                 ,self.Length \
                 ,self.Offset \
        =unpack(self.FormtStr,rawstr)

    def getNameInfo(self,NameID,PlatformID=3,LanguageID=EN_US):
        nth=self.TableDir['name']

        nid='%s-%s-%s' % (PlatformID,LanguageID,NameID)
        usnid='%s-1033-%s' % (PlatformID,NameID)
        eid,len,infoffset=self.NameRecords.get(nid,self.NameRecords.get(usnid,(None,None,None)))
        if eid is None:
            return None
        offset=nth['Offset']+self.NameTableHeader['StorageOffset']+infoffset
        namestr=self.RawFontStr[offset:offset+len]
        return namestr.decode('utf-16be','replace')
        
    

class OTFName():
    def __init__(self,ttffile,platformid=3,langid=en_us):
        self.PlatformId=platformid
        self.LangId=langid
        self.FontEntrys=[]
        self.RawFontStr=''
        self.FontFile=ttffile
        with open(ttffile,'rb') as f:
            self.RawFontStr=f.read()
        if self.RawFontStr[:4]==b'ttcf':
            self.FontType='TTC'
            self.loadTTC()
        else:
            self.FontType='TTF'
            self.loadTTF()

        self.RawFontStr=''

    def getFontInfo(self,name):
        '''
        name: string or int
        '''
        if isinstance(name,str):
            name=FONTNAMEMAP.get(name,None)
        if name is None:
            raise Exception("font name error")
        return [f.Names.get(name,'') for f in self.FontEntrys]

    def getFontLocalInfo(self,name):
        if isinstance(name,str):
            name=FONTNAMEMAP.get(name,None)
        if name is None:
            raise Exception("font name error")
        return [f.LocalNames.get(name,f.Names.get(name,'')) for f in self.FontEntrys]

        
    def loadFont(self,fontentry,offset_table_offset=0):
        offset = offset_table_offset + FontEntry.RawSize
        for i in range(0,fontentry.NumOfTables):
            tentry=TableEntry(self.RawFontStr[offset:offset+TableEntry.RawSize])
            fontentry.Tables[tentry.Tag]=tentry 
            offset += TableEntry.RawSize

            
    def loadFontName(self,fontentry): #,platformid=3,langid=en_us):
        fentry=fontentry
        nte=name_table_entry=fentry.Tables.get('name')
        if nte:
            s=self.RawFontStr[nte.Offset:NameTableHeader.RawSize+nte.Offset]
            nth=NameTableHeader(s)
            nroffset=nte.Offset+NameTableHeader.RawSize
            namestoreoffset=nte.Offset+nth.StringOffset
            for n in range(0,nth.Count):
                nrs=self.RawFontStr[nroffset:nroffset+NameRecord.RawSize]
                nr=NameRecord(nrs)
                nrid='%s-%s-%s' % (nr.PlatformId,nr.LangId,nr.NameId)
                stroffset=namestoreoffset+nr.Offset
                if self.PlatformId == nr.PlatformId and en_us == nr.LangId:
                    namestr=self.RawFontStr[stroffset:stroffset+nr.Length].decode('utf-16be','replace')
                    fentry.Names[nr.NameId]=namestr
                if self.PlatformId == nr.PlatformId and self.LangId == nr.LangId:
                    namestr=self.RawFontStr[stroffset:stroffset+nr.Length].decode('utf-16be','replace')
                    fentry.LocalNames[nr.NameId]=namestr
                nroffset+=NameRecord.RawSize
                
    def loadTTC(self):

        offset=TTCHEADERSIZE
        tag,mver,pver,numfonts=ttcheader=unpack(_ttc_header_fmt,self.RawFontStr[:offset])
        if mver==1: 
            pass

        for i in range(0,numfonts):
            taboffset=unpack('>L',self.RawFontStr[offset:offset+4])[0]
            fentry=FontEntry(self.RawFontStr[taboffset:taboffset+FontEntry.RawSize])
            self.loadFont(fentry,taboffset)
            self.FontEntrys.append(fentry)
            self.loadFontName(fentry)
            offset+=4

    def loadTTF(self):
        font=FontEntry(self.RawFontStr[:FontEntry.RawSize])
        self.loadFont(font) 
        self.FontEntrys.append(font)
        self.loadFontName(font)
        

def get_font_name(fontfile,langid=''):
        if platform.uname().system.upper() == 'WINDOWS':
            lang=LOCALMAP.get(locale.getdefaultlocale()[1],en_us)
        else:
            lang=en_us
        lang=langid if langid else lang
        otf=OTFName(fontfile,langid=lang)
        return (otf.getFontLocalInfo('Family'),otf.getFontInfo('SubFamily'))
    
    

if __name__=='__main__':

    print('zh_cn',zh_cn)
    ttf=OTFName('c:/windows/fonts/msyhbd.ttf',langid=zh_cn)    
    print('font file :',ttf.FontFile)
    print('font family Id',ttf.getFontInfo('Id'))
    print('font local family',ttf.getFontLocalInfo('Family'))
    print('font local subfamily',ttf.getFontLocalInfo('SubFamily'))            
    fn=r'C:\Windows/fonts/迷你简华隶.ttf'
    #fn=r'c:\windows/fonts/simsun.ttc'
    ttf=OTFName(fn,langid=zh_cn)    
    print('font file :',ttf.FontFile)
    print('font  family Id',ttf.getFontInfo('Id'))
    print('font local family',ttf.getFontLocalInfo('Family'))
    print('font local subfamily',ttf.getFontLocalInfo('SubFamily'))        
