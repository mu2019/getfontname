# getfontname
get ttf/ttc font file name 

from getfontname import OTFName

ttf=OTFName('c:/windows/fonts/msyh.ttf',langid=zh_cn)    
print('font file :',ttf.FontFile)
print('font en family',ttf.getFontInfo('Family'))
print('font local family',ttf.getFontLocalInfo('Family'))    


out put 

font file : c:/windows/fonts/msyh.ttf
font en family ['Microsoft YaHei']
font local family ['微软雅黑']
