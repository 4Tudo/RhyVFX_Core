#
import os.path
import xml.etree.ElementTree as etree
from PIL import Image
from ursina import *
# os.chdir('../')
import settings




def name2path_arrows(name):
    return {
        'arrowImg':f'assets/images/arrows/{name}/arrows.png',
        'arrowXML':f'assets/images/arrows/{name}/arrows.xml'
    }


def getArrowInfo(name,subTextureName):
    arrowXML = etree.parse(
        name2path_arrows(name)['arrowXML']
    )
    texturesXML = arrowXML.getroot()

    arrowTexture = None


    for texture in texturesXML:
        if texture.attrib['name'] == subTextureName:

                arrowTexture = {'startX':int(texture.attrib['x']),
                  'startY':int(texture.attrib['y']),
                  'endX':int(texture.attrib['x']) + int(texture.attrib['width']),
                  'endY':int(texture.attrib['y']) + int(texture.attrib['height']),
                  'name':texture.attrib['name']
                 }


    return arrowTexture


def cropArrowTexure(arrowName,subTextureName):
    textureInfo = getArrowInfo(arrowName,subTextureName)

    texture = Image.open(name2path_arrows(arrowName)['arrowImg'])


    cropTexture = texture.crop((int(textureInfo['startX']),
                                int(textureInfo['startY']),
                                int(textureInfo['endX']),
                                int(textureInfo['endY'])))
    return cropTexture


# class ArrowTextures:
#     def __init__(self,arrowName):
#         self.arrowName = arrowName
#         self.arrows = self.Arrows(self.arrowName)
#         self.note_alone = self.Note_alone(self.arrowName)
#         self.tails = self.Tails(self.arrowName)
#         self.holds = self.Holds(self.arrowName)
#         self.confirms = self.Confirms(self.arrowName)
#         self.press = self.Press(self.arrowName)
#
#
#     class Arrows:
#         def __init__(self,arrowName):
#             self.DOWN = Texture(cropArrowTexure(arrowName, 'arrowDOWN0000'))
#             self.LEFT = Texture(cropArrowTexure(arrowName, 'arrowLEFT0000'))
#             self.RIGHT = Texture(cropArrowTexure(arrowName, "arrowRIGHT0000"))
#             self.UP = Texture(cropArrowTexure(arrowName, 'arrowUP0000'))
#
#     class Note_alone:
#         def __init__(self,arrowName):
#             self.BLUE = Texture(cropArrowTexure(arrowName, 'blue alone0000'))
#             self.GREEN = Texture(cropArrowTexure(arrowName, 'green alone0000'))
#             self.PURPLE = Texture(cropArrowTexure(arrowName, 'purple alone0000'))
#             self.RED = Texture(cropArrowTexure(arrowName, 'red alone0000'))
#
#     class Tails:
#         def __init__(self,arrowName):
#             self.BLUE = Texture(cropArrowTexure(arrowName, 'blue tail0000'))
#             self.GREEN = Texture(cropArrowTexure(arrowName, 'green tail0000'))
#             self.PURPLE = Texture(cropArrowTexure(arrowName, 'purple tail0000'))
#             self.RED = Texture(cropArrowTexure(arrowName, 'red tail0000'))
#
#     class Holds:
#         def __init__(self,arrowName):
#             self.BLUE = Texture(cropArrowTexure(arrowName, 'blue hold0000'))
#             self.GREEN = Texture(cropArrowTexure(arrowName, 'green hold0000'))
#             self.PURPLE = Texture(cropArrowTexure(arrowName, 'purple hold0000'))
#             self.RED = Texture(cropArrowTexure(arrowName, 'red hold0000'))
#
#     class Confirms:
#         def __init__(self,arrowName):
#             self.DOWN = [
#                 Texture(cropArrowTexure(arrowName, 'down confirm0000')),
#                 Texture(cropArrowTexure(arrowName, 'down confirm0001')),
#                 Texture(cropArrowTexure(arrowName, 'down confirm0002')),
#                 Texture(cropArrowTexure(arrowName, 'down confirm0003'))
#             ]
#             self.LEFT = [
#                 Texture(cropArrowTexure(arrowName, 'left confirm0000')),
#                 Texture(cropArrowTexure(arrowName, 'left confirm0001')),
#                 Texture(cropArrowTexure(arrowName, 'left confirm0002')),
#                 Texture(cropArrowTexure(arrowName, 'left confirm0003'))
#             ]
#             self.RIGHT = [
#                 Texture(cropArrowTexure(arrowName, 'right confirm0000')),
#                 Texture(cropArrowTexure(arrowName, 'right confirm0001')),
#                 Texture(cropArrowTexure(arrowName, 'right confirm0002')),
#                 Texture(cropArrowTexure(arrowName, 'right confirm0003'))
#             ]
#             self.UP = [
#                 Texture(cropArrowTexure(arrowName, 'up confirm0000')),
#                 Texture(cropArrowTexure(arrowName, 'up confirm0001')),
#                 Texture(cropArrowTexure(arrowName, 'up confirm0002')),
#                 Texture(cropArrowTexure(arrowName, 'up confirm0003'))
#             ]
#
#     class Press:
#         def __init__(self,arrowName):
#             self.DOWN = [
#                 Texture(cropArrowTexure(arrowName, 'down press0000')),
#                 Texture(cropArrowTexure(arrowName, 'down press0001')),
#                 Texture(cropArrowTexure(arrowName, 'down press0002')),
#                 Texture(cropArrowTexure(arrowName, 'down press0003'))
#             ]
#             self.LEFT = [
#                 Texture(cropArrowTexure(arrowName, 'left press0000')),
#                 Texture(cropArrowTexure(arrowName, 'left press0001')),
#                 Texture(cropArrowTexure(arrowName, 'left press0002')),
#                 Texture(cropArrowTexure(arrowName, 'left press0003'))
#             ]
#             self.RIGHT = [
#                 Texture(cropArrowTexure(arrowName, 'right press0000')),
#                 Texture(cropArrowTexure(arrowName, 'right press0001')),
#                 Texture(cropArrowTexure(arrowName, 'right press0002')),
#                 Texture(cropArrowTexure(arrowName, 'right press0003'))
#             ]
#             self.UP = [
#                 Texture(cropArrowTexure(arrowName, 'up press0000')),
#                 Texture(cropArrowTexure(arrowName, 'up press0001')),
#                 Texture(cropArrowTexure(arrowName, 'up press0002')),
#                 Texture(cropArrowTexure(arrowName, 'up press0003'))
#             ]

    # class UP:
    #     def __init__(self,arrowName):
    #         self.



# arrowTextures = ArrowTextures(settings.arrowsStyle)
'''
I wanted make a Friday Night Funkin' engine lol
'''

class LoadTextureFromXML():
    def __init__(self,imgPath,xmlPath):
        self.imgPath = imgPath
        self.xmlPath = xmlPath
        self.textureXml = etree.parse(xmlPath)
        self.subTextures = self.textureXml.getroot()


    def getTexture(self,texName):
        textureData = {
            'startX':0,
            'startY':0,
            'endX':0,
            'endY':0
        }
        for texture in self.subTextures:
            if texture.attrib['name'] == texName:
                textureData = {
                    'startX':int(texture.attrib['x']),
                    'startY':int(texture.attrib['y']),
                    'endX':int(texture.attrib['x'])+int(texture.attrib['width']),
                    'endY':int(texture.attrib['y'])+int(texture.attrib['height'])
                }

        textureAtlas = Image.open(self.imgPath)
        cropedTexture = textureAtlas.crop((
            textureData['startX'],
            textureData['startY'],
            textureData['endX'],
            textureData['endY']
        ))

        return Texture(cropedTexture)


# class RankTextures:
#     def __init__(self,styleName):
#         self.styleName = styleName







if __name__ == '__main__':
    app = Ursina()
    window.borderless = False
    EditorCamera()

    arrowTextures = ArrowTextures('basic')

    textures = [
        arrowTextures.arrows.UP,
        arrowTextures.arrows.DOWN,
        arrowTextures.arrows.LEFT,
        arrowTextures.arrows.RIGHT,

        arrowTextures.note_alone.BLUE,
        arrowTextures.note_alone.GREEN,
        arrowTextures.note_alone.PURPLE,
        arrowTextures.note_alone.RED,

        arrowTextures.tails.BLUE,
        arrowTextures.tails.GREEN,
        arrowTextures.tails.PURPLE,
        arrowTextures.tails.RED,

        arrowTextures.holds.BLUE,
        arrowTextures.holds.GREEN,
        arrowTextures.holds.PURPLE,
        arrowTextures.holds.RED,

        arrowTextures.confirms.DOWN[0],
        arrowTextures.confirms.DOWN[1],
        arrowTextures.confirms.DOWN[2],
        arrowTextures.confirms.DOWN[3],
        arrowTextures.confirms.LEFT[0],
        arrowTextures.confirms.LEFT[1],
        arrowTextures.confirms.LEFT[2],
        arrowTextures.confirms.LEFT[3],
        arrowTextures.confirms.RIGHT[0],
        arrowTextures.confirms.RIGHT[1],
        arrowTextures.confirms.RIGHT[2],
        arrowTextures.confirms.RIGHT[3],
        arrowTextures.confirms.UP[0],
        arrowTextures.confirms.UP[1],
        arrowTextures.confirms.UP[2],
        arrowTextures.confirms.UP[3],

        arrowTextures.press.DOWN[0],
        arrowTextures.press.DOWN[1],
        arrowTextures.press.DOWN[2],
        arrowTextures.press.DOWN[3],
        arrowTextures.press.LEFT[0],
        arrowTextures.press.LEFT[1],
        arrowTextures.press.LEFT[2],
        arrowTextures.press.LEFT[3],
        arrowTextures.press.RIGHT[0],
        arrowTextures.press.RIGHT[1],
        arrowTextures.press.RIGHT[2],
        arrowTextures.press.RIGHT[3],
        arrowTextures.press.UP[0],
        arrowTextures.press.UP[1],
        arrowTextures.press.UP[2],
        arrowTextures.press.UP[3],
    ]

    for i in range(len(textures)):
        Entity(x=i,
               model='quad',
               texture=textures[i])

    testTex = LoadTextureFromXML('assets/images/arrows/basic/arrows.png','assets/images/arrows/basic/arrows.xml')
    Entity(model='quad',texture=testTex.getTexture(testTex.getTexture('arrowLEFT0000')))
    print(testTex.getTexture('arrowLEFT0000'))

    app.run()

