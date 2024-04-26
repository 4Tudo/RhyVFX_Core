import random

from ursina import *

debug = False
decorations = []
lightly = False

class Cities(Entity):
    def __init__(self,z,x,x_offset=0):
        global decorations
        super().__init__(
            model='quad',
            texture=f'./assets/images/cities{random.randint(1,5)}.png',
            scale=(20,5,1),
            z=z,
            y=-3,
            x=x,
            alpha=0.6
        )
        if debug:
            self.texture = f'../assets/images/cities{random.randint(1,5)}.png'
        self.x += random.uniform(0,x_offset)
        self.animate_position((self.x-60,self.y,self.z),duration=10,curve=curve.linear)
        self.startX = self.x

        decorations.append(self)

    def update(self):
        if lightly:

            self.color = color.hex('#ff426a')
        if self.x <= self.startX - 60:
            destroy(self)
            decorations.remove(self)
            return

class Flash(Entity):
    def __init__(self,colors,**kwargs):
        super().__init__(
            model='quad',
            parent=camera.ui,
            scale=2
        )
        self.flashLast = time.time()
        self.currentColor = 0
        self.colors = colors
    def update(self):

        if self.currentColor < len(self.colors):
            if time.time() - self.flashLast >= self.colors[self.currentColor][1]:
                self.animate_color(
                    self.colors[self.currentColor][0],
                    duration=self.colors[self.currentColor][1],
                    curve=curve.in_out_cubic
                )
                self.currentColor += 1

class SkyLight(Entity):
    def __init__(self):
        super().__init__(
            scale=(50,30,1),
            model='quad',
            z=30,
            y=-4,
            texture='./assets/images/light.png',
        )
        if debug:
            self.texture = '../assets/images/light.png'
        self.visible = False

    def update(self):
        if lightly:
            self.visible = True
            self.color = color.hex('#d8fffe')


class CinemaBorder(Entity):
    def __init__(self,type,size):
        super().__init__()
        self.model='quad'
        self.color=color.black
        if type == 'upper':
            self.y = size
        if type == 'under':
            self.y = -size
        self.scale = (18,4)
        self.state = 'up'
        self.loop = 2
        self.aniLast = time.time()
        self.parent = camera.ui
        self.z = 10
    def update(self):
        if time.time() >= self.aniLast + 1/60:
            if self.state == 'up' and self.loop == 0:
                self.y += 0.5
                self.y -= 0.5
            if self.state == 'down' and self.loop >= 0:
                self.y -= 0.04
                self.y += 0.04
            self.aniLast = time.time()


def changeLightingState(arg):
    global lightly
    lightly = arg


if __name__ == '__main__':
    app = Ursina()
    EditorCamera()
    window.borderless = False
    lightly = True
    debug = True
    cinema1 = CinemaBorder(type='under',size=4.5)
    cinema2 = CinemaBorder(type='upper',size=4.5)
    window.color = color.black
    SkyLight()
    for i in range(3, 23):
        Cities(z=i, x=0, x_offset=20)
        Cities(z=i, x=20, x_offset=20)
    Cities(0,0)
    app.run()
