
import os
import uuid

import subprocess

cwd = os.getcwd()
if 'imagick' in os.path.basename(cwd):
    executable = os.path.join(cwd, 'convert')
else:
    executable = os.path.join(cwd, 'lib', 'imagick', 'convert')

def getTempFilename():
    fname = '{0}.png'.format(uuid.uuid4())
    fpath = os.path.join('tmp', fname)
    return fpath

def makeStrokedText(
    text, 
    pointSize=32, 
    font="Arial",
    stroke='#555', 
    strokeWidth=10, 
    fill='white', 
    fname=None):

    ''' Creates an image file with stroked text of the specified parameters; 
        Returns path of temporary file created or given path if specified. 
    '''

    fpath = fname if fname else getTempFilename()

    pad = strokeWidth
    offx = pad + 2
    offy = pointSize * 0.85 + pad

    # reference the executable to be called
    line = "{0}".format(executable)

    # create a transparent border as makeshift padding;
    # this prevents clipping as the size of the image depends on the label, NOT the stroke
    line += " -border {0}x{0} -bordercolor transparent -background none".format(pad)

    # font
    line += " -font {0} -pointsize {1}".format(font, pointSize)

    # create a transparent label so the image will be automatically sized
    line += " -fill transparent label:\"{0}\"".format(text)

    # inside stroke
    line += " -fill white -stroke {0} -strokewidth {1}".format(stroke, strokeWidth)
    line += " -annotate +{0}+{1} \"{2}\"".format(offx, offy, text)

    # outside stroke
    line += " -stroke none -annotate +{0}+{1} \"{2}\"".format(offx, offy, text)

    # file to save as
    line += " {0}".format(fpath)

    os.system(line)

    return fpath

def appendImage(a, b, gravity='north', hor=False, fname=None):
    ''' Appends image b to image a. '''

    ### TODO horizontal isn't implemented

    fpath = fname if fname else getTempFilename()

    # reference the executable to be called
    line = "{0}".format(executable)

    #line += " {0} -background Khaki label:'Faerie Dragon'".format(a)
    #line += " -gravity Center -append {0}".format(b)

    if hor:
        line += " {0} {1} +append".format(a, b)
    else:
        #line += " {0} {1} -append".format(a, b)
        ##line += " -size 500x700 plasma:fractal null: \( {0} -coalesce \)".format(a)
        ###line += " -size 500x700 {0} null: ( {1} -coalesce )".format(a, b)
        line += " -size 550x431 {0} null: ( {1} -coalesce )".format(a, b)
        line += " -gravity {0} -layers Composite".format(gravity)
        ####line += " -layers Optimize"

    # file to save as
    line += " {0}".format(fpath)

    #os.system(line)
    p = subprocess.Popen(line.split(' '))

    return p, fpath

### TODO XXX FIXME the size in makeCmdAppend is STATIC!!!!!

'''
def makeCmdAppend(a, b, gravity='north'):
    line = " -size 550x431 {0} null: ( {1} -coalesce )".format(a, b)
    line += " -gravity {0} -layers Composite".format(gravity)
    return line

def makeCmdOverlay(back, fore, off=(0, 0)):
    offx, offy = off
    line = " {0} -coalesce ".format(back)
    line += " -gravity none -geometry +{0}+{1} null: {2} -layers composite".format(offx, offy, fore)
    return line
'''

def composeXchange(back, gif, overlay, gravity='north', off=(0, 0), fname=None):

    fpath = fname if fname else getTempFilename()

    offx, offy = off

    line = "{0} ".format(executable)

    #line += makeCmdAppend(back, gif, gravity)
    line += " -size 550x431 {0} null: ( {1} -coalesce )".format(back, gif)
    line += " -gravity {0} -layers Composite".format(gravity)

    #line += makeCmdOverlay('', overlay)
    line += " -coalesce "
    line += " -gravity none -geometry +{0}+{1} null: {2} -layers composite".format(offx, offy, overlay)

    line += " {0}".format(fpath)

    p = subprocess.Popen(line.split(' '))

    return p, fpath

def mergeImages(a, b, fname=None):
    ### TODO only works with gifs!!!
    if fname:
        fpath = fname
    else:
        fname = '{0}.gif'.format(uuid.uuid4())
        fpath = os.path.join('tmp', fname)

    offx = 10
    #offy = 10
    offy = 300

    line = "{0} ".format(executable)
    #line += "{0} -coalesce -gravity South ".format(a)
    line += "{0} -coalesce ".format(a)
    line += " -geometry +{0}+{1} null: {2} -layers composite -layers optimize ".format(offx, offy, b)
    line += "{0}".format(fpath)

    os.system(line)

    return fpath

if __name__ == '__main__':
    #makeStrokedText('just a test', (400, 200), 12)
    mergeImages('tmp/gif.gif', 'tmp/mark.png')

