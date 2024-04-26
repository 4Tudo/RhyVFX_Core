#
from ursina import *

import appdata
import settings
from settings import *

if __name__ == '__main__':
    app = Ursina()


class GameUi(Entity):

    def __init__(self):
        super().__init__()
        self.z = 1.2
        self.parent = camera.ui
        # self.scale=10
        self.texts = {
            'score':'Score:0',
            'misses':'Misses:0',
            'accuracy':'Accuracy:0',
            'rating':'None'
        }
        self.uiPos = {
            # 'score':(-.168,-.18,0),
            'score':(-.068,-.17,0),
            'misses':(.032,-.17,0),
            # 'rating':(.132,-.18,0),
            # 'rating':(.132,-.18,0),
            'rating': (114, 514, 0),
            'accuracy':(191,9810,0),
            'version':(-0.34,.19)
        }

        self.uiStyle = {
            'textScale':0.4,
        }

        self.scale = 2.5

        self.score = Text(text=self.texts['score'],
                          position=self.uiPos['score'],
                          parent=self,
                          scale=self.uiStyle['textScale']
                          )
        self.misses = Text(text=self.texts['misses'],
                          position=self.uiPos['misses'],
                          parent=self,
                           scale=self.uiStyle['textScale']
                           )
        self.accuracy = Text(text=self.texts['accuracy'],
                          position=self.uiPos['accuracy'],
                          parent=self,
                             scale=self.uiStyle['textScale']
                          )
        self.rating = Text(text=self.texts['rating'],
                          position=self.uiPos['rating'],
                          parent=self,
                           scale=self.uiStyle['textScale']
                          )
        self.version = Text(text=f'{appdata.name} {appdata.version}',
                            position=self.uiPos['version'],
                            parent=self,
                            scale=self.uiStyle['textScale'])
        # self.startButton = Button('Start!')

gameUi = GameUi()


if __name__ == '__main__':

    window.borderless = False
    EditorCamera()
    camera.z = 0
    # tester = Entity(model='cube')
    app.run()


