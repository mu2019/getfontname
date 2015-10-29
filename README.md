# getfontname
不需要其它库支持,使用python获取ttf及ttc字体文件的字体名称

get ttf/ttc font file name 

test.py

import getfontname
from getfontname import fontname,fontfile

ffilename=getfontname.get_font_file('宋体')
print('font file:', ffilename)

fname=getfontname.get_font_name(ffilename)
print('font name:',fname)



python test.py

out put >>>

font file: C:\Windows/fonts/simsun.ttc

font name: (['宋体', '新宋体'], ['Regular', 'Regular'])
