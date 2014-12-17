
import uuid

import Image
import ImageDraw
import ImageFont
import cStringIO

import lib.imagick.basic as imagick

class Layer:

    def __init__(self):
        self.pos = (0, 0)

    def getPos(self):
        return self.pos[0], self.pos[1]

    def setPos(self, x, y):
        self.pos = (x, y)

class ImageLayer(Layer):

    def __init__(self, fname):
        Layer.__init__(self)
        self.image = Image.open(fname)

    def render(self):
        return self.image

    def getSize(self):
        return self.image.size

class StrokedTextLayer(Layer):

    def __init__(self, text=''):
        Layer.__init__(self)

        self.tmpFile = 'tmp/{0}.png'.format(uuid.uuid4())

        self.size = (1, 1)
        self.wrapWidth = None
        self.text = text
        self.fontSize = 32
        self.fontFamily = 'C:/Windows/Fonts/arial.ttf'
        self.font = ImageFont.truetype(self.fontFamily, self.fontSize)

        self.stroke = '#555'
        self.strokeWidth = 10

        # we only need to update if we were passed text initially
        self.dirty = bool(text)
        self.image = Image.new('RGBA', self.size, (0, 0, 0, 0))

    def getFont(self):
        ''' Returns ImageFont.FreeTypeFont object based on this layer's
            given font attributes 
        '''
        return ImageFont.truetype(self.fontFamily, self.fontSize)

    def getFontFamily(self):
        return self.fontFamily

    def getFontSize(self):
        return self.fontSize

    def getSize(self):
        return self.getImage().size

    def getStroke(self):
        return self.stroke

    def getStrokeWidth(self):
        return self.strokeWidth

    def getText(self):
        return self.text

    def getTextSize(self, text=None):
        ''' Returns the size of the given text, which is by default
            this layer's text. 
        '''

        image = Image.new('RGBA', self.size, (0, 0, 0, 0))

        text = text if text else self.getText()
        #draw = ImageDraw.Draw(self.getImage())
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(text, self.getFont())
        return w, h

    def getImage(self):
        return self.image

    def getWrapWidth(self):
        return self.wrapWidth

    def render(self):
        ''' Renders the image and returns the image object '''

        # if no changes have been made, there is no need to re-render
        if not self.dirty:
            return self.image

        text = self.getText()
        wrapWidth = self.getWrapWidth()
        if not wrapWidth is None:

            def wrapLine(text, width):
                # split text into lines based on image width
                lines = []
                buffer = ''
                for i in text.split(' '):
                    if self.getTextSize(buffer + i + ' ')[0] > wrapWidth:
                        lines.append(buffer + ' ')
                        buffer = i + ' '
                        continue
                    buffer += i + ' '
                lines.append(buffer)
                text = "\\n".join(lines)
                return text

            lines = text.splitlines()
            text = '\n'.join([wrapLine(l, wrapWidth) for l in lines])
            #text = wrapLine(text, wrapWidth)

        fname = imagick.makeStrokedText(
            text, 
            self.getFontSize(), 
            font=self.getFontFamily(),
            stroke=self.getStroke(),
            strokeWidth=self.getStrokeWidth(),
            fname=self.tmpFile
        )

        self.setImage(Image.open(fname))

        self.dirty = False

        return self.image

    def setFontFamily(self, family):
        if family == self.fontFamily:
            return
        self.fontFamily = family
        self.dirty = True

    def setFontSize(self, size):
        if size == self.fontSize:
            return
        self.fontSize = size
        self.dirty = True

    def setImage(self, image):
        self.image = image
        # we aren't dirty here because the image is being set directly

    def setStroke(self, stroke):
        if stroke == self.stroke:
            return
        self.stroke = stroke
        self.dirty = True

    def setStrokeWidth(self, width):
        if width == self.strokeWidth:
            return
        self.strokeWidth = width
        self.dirty = True

    def setText(self, text):
        # don't update if nothing has changed
        if text == self.text:
            return
        self.text = text
        self.dirty = True

    def setWrapWidth(self, width):
        if width == self.wrapWidth:
            return
        self.wrapWidth = width
        self.dirty = True


