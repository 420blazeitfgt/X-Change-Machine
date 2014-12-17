
import os

fname = 'tester.png'
text = "X-Change \\nBasic"

colStoke = (216, 36, 170)

'''
line = ""
line += "convert -size 320x100 xc:lightblue -font aardvark_cafe.ttf -pointsize 72"
line += " -fill black  -annotate +24+64 '{0}'".format(text)
line += "              -annotate +26+64 '{0}'".format(text)
line += "              -annotate +26+66 '{0}'".format(text)
line += "              -annotate +24+66 '{0}'".format(text)
line += " -fill white  -annotate +25+65 '{0}'".format(text)
line += " {0}".format(fname)
'''

line = "convert -size 400x500 xc:#00000000 -font aardvark_cafe.ttf -pointsize 72 -fill white"
line += " -stroke #d824aa -strokewidth 10 -annotate +25+65 \"{0}\"".format(text)
line += " -stroke none                    -annotate +25+65 \"{0}\"".format(text)
line += " {0}".format(fname)

os.system(line)

