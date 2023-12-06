from cmu_graphics import *

class Message():
    def __init__(self, x, y, width, height, messageText, size, fill='lightgrey', active = True, borderWidth = 3):
        self.width = width
        self.height = height
        self.top = y - self.height / 2
        self.left = x - self.width / 2
        self.bottom = y + self.height / 2
        self.right = x + self.width / 2
        self.x = x
        self.y = y
        self.clicked = False
        self.text = messageText
        self.size = size
        self.active = active
        self.fill = fill
        self.borderWidth = borderWidth
        self.centerX = x
        self.centerY = y

    def draw(self):
        opacity = 100 if self.active else 30
        border = 'red' if self.active else 'yellow'
        drawRect(self.left, self.top, self.width, self.height, fill=self.fill, border = border, borderWidth = self.borderWidth, opacity = opacity)
        drawLabel(self.text, self.x, self.y , size = self.size, opacity = opacity)

    def setActive(self, active):
        self.active = active

    def contains(self, mouseX, mouseY):
        if (mouseX > self.left and mouseX < self.right):
            if (mouseY > self.top and mouseY < self.bottom):
                print (f'button {self.text} is pressed')
                return True
        return None
