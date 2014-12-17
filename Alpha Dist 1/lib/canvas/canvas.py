
import Image

class Canvas:

    def __init__(self, size=(1, 1)):
        self.layers = []

        self.size = size
        w, h = self.size
        self.bgCol = (0, 0, 0, 0)
        self.image = Image.new('RGBA', (w, h), self.bgCol)

    def addLayer(self, image):
        self.layers.append(image)

    def getBackgroundColor(self):
        return self.bgCol

    def getLayers(self):
        return self.layers

    def getSize(self):
        return self.size

    def render(self):
        canvas = self.image

        for layer in self.getLayers():
            rend = layer.render()
            x, y = layer.getPos()
            try:
                canvas.paste(rend, (x, y), rend)
            except ValueError:
                canvas.paste(rend, (x, y))

        return canvas

    def setBackgroundColor(self, col):
        self.bgCol = col
        self.image = Image.new('RGBA', self.getSize(), self.bgCol)

    def setSize(self, w, h):
        self.size = (w, h)
        self.image = Image.new('RGBA', (w, h), self.getBackgroundColor())
