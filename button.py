from cmu_graphics import *

#The button class
class Button():
    def __init__(self, x, y, width, height, label, size, active = True):
        self.width = width
        self.height = height
        self.top = y - self.height / 2
        self.left = x - self.width / 2
        self.bottom = y + self.height / 2
        self.right = x + self.width / 2
        self.x = x
        self.y = y
        self.clicked = False
        self.text = label
        self.size = size
        self.active = active
        self.centerX = x #center x coord
        self.centerY = y #center y coord

    #Draws the buttons
    def draw(self):
        opacity = 100 if self.active else 30
        drawRect(self.left, self.top, self.width, self.height, fill='goldenrod', border = 'gray', opacity = opacity)
        drawLabel(self.text, self.x, self.y , size = self.size, opacity = opacity)

    #Sets button as pressed or not
    def setActive(self, active):
        self.active = active

    #checks if mouse press hits within box
    def contains(self, mouseX, mouseY):
        if not self.active:
            return None

        if (mouseX > self.left and mouseX < self.right):
            if (mouseY > self.top and mouseY < self.bottom):
                print (f'button {self.text} is pressed')
                return True
        return None
