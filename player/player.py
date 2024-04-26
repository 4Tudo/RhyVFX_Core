#
import os.path
import time

from ursina import *
from functools import partial
import settings
from ui import *
from .textures import *
from .chart import *
from .attrs import *
from .entity import *


class HealthBars(Entity):

    def __init__(self,length):
        super().__init__(model='quad',
            # texture='assets/images/ui/healthBar.png',
            color=color.clear,
            parent=gameUi,
            position=(0,-.2,0),
            scale=(length,0.01,1))

        self.health_self = 50
        self.health_enemy = 50

        self.damage = 5
        self.length = length

        # self.healthBar_outLine = Entity(
        #
        # )

        self.healthBar_enemy = Entity(
            model='quad',
            color=color.clear,
            parent=self,
            scale=(0.5, 1, 1),
            origin_x=-0.5,
            position=(-0.5,
                      0,
                      0.00001
                      ),

        )
        self.healthBar_self = Entity(
            model='quad',
            color=color.white,
            parent=self,
            scale=(0.5, 1, 1),
            origin_x=0.5,
            position=(0.5,
                      0,
                      0.00001
                      )
        )

    def update(self):

        # self.healthBar_self.scale_x = 0.5 * self.health_self / 50
        # self.healthBar_enemy.scale_x = 0.5 * self.health_enemy / 50
        if self.health_self >= 100:
            self.health_self = 100
        if self.health_enemy >= 100:
            self.health_enemy = 100

    def input(self,event):
        if debugMode:
            if event == 's':
                self.damage_enemy()
            if event == 'd':
                self.damage_self()

    def damage_self(self):
        if self.health_enemy + self.damage >= 100:
            self.health_enemy = 100
            self.health_self = 0
        else:
            self.health_self -= self.damage
            self.health_enemy += self.damage

        self.healthBar_enemy.animate_scale((0.5 * self.health_enemy / 50, 1, 1), duration=0.8, curve=curve.out_cubic)
        self.healthBar_self.animate_scale((0.5 * self.health_self / 50,1,1),duration=0.8,curve=curve.out_cubic)


    def damage_enemy(self):
        if self.health_self + self.damage >= 100:
            self.health_self = 100
            self.health_enemy = 0
        else:
            self.health_self += self.damage
            self.health_enemy -= self.damage

        self.healthBar_self.animate_scale((0.5 * self.health_self / 50,1,1),duration=0.8,curve=curve.out_cubic)
        self.healthBar_enemy.animate_scale((0.5 * self.health_enemy / 50, 1, 1), duration=0.8, curve=curve.out_cubic)


healthBars = HealthBars(0.75)


class RectRound(Entity):
    def __init__(self,roundPosition,roundScale,gameSurParent,aniKey):
        super().__init__()
        self.model='quad'
        self.texture='./assets/images/rectRound.png'
        self.parent = gameSurParent
        self.scale = roundScale
        self.world_position = roundPosition
        self.aniKey = aniKey
        self.inital_scale = roundScale

        self.aniLast = time.time()
        self.autoPressState = False # False down   True up
        self.autoPressLast = time.time()

    def update(self):
        if time.time() >= self.aniLast + 1/200:
            self.rotation_z -= 0.1
            self.aniLast = time.time()


        if time.time() >= self.autoPressLast + .1 and self.autoPressState:
            self.animate_scale(
                self.inital_scale*1,
                duration=0.05,
                curve=curve.out_sine
            )
            self.autoPressState = False

    def input(self,event):
        if event == self.aniKey and not settings.autoPlay:
            self.animate_scale(
                self.inital_scale*1.4,
                duration=0.05,
                curve=curve.out_sine
            )
        if event == self.aniKey+' up' and not settings.autoPlay:
            self.animate_scale(
                self.inital_scale*1,
                duration=0.05,
                curve=curve.out_sine
            )

    def pressAni(self):
        self.animate_scale(
            self.inital_scale * 1.4,
            duration=0.05,
            curve=curve.out_sine
        )
        self.autoPressState = True
        self.autoPressLast = time.time()





class Round(Entity):
    def __init__(self,chartId,parent,timeList,trackLength,unitDis,autoPlay,startTime,**kwargs):
        super().__init__()

        self.model = 'quad'

        self.texture = './assets/images/rectRound.png'

        self.y = 0.15
        self.scale = 0.05
        self.originX = -0.1
        self.arrowId = chartId
        self.x = self.originX + (self.scale_x+0.02) * self.arrowId

        self.startTime = time.time()
        self.parent = parent
        self.round_inside = RectRound(roundPosition=self.world_position,
                  roundScale=self.scale*0.65,
                  gameSurParent=self.parent,
                  aniKey=settings.keys[chartId]
        )
        self.roundText = Text(
            text=str(chartId + 1),
            parent=self,
            position=self.position,
            x=self.x-0.2,
            scale=20,
            world_rotation=0,
            origin=0,

        )

        self.trackLine = Entity(
            model='quad',
            scale=(0.001,30),
            parent=self.parent,
            origin_y=0.5,
            position=self.position,
        )


        self.timeListForSelf = timeList[chartId]
        self.trackLength = trackLength
        self.unitDis = unitDis
        self.started = False
        self.gameLast = time.time()
        self.currentChart = 0
        self.autoPlay = autoPlay

        self.rot_aniLast = time.time()

    def update(self):
        self.roundText.world_rotation_z = 0

        if time.time() >= self.rot_aniLast + 1/200:
            self.rotation_z += 0.1
            self.rot_aniLast = time.time()

        if settings.debugMode:
            self.x += held_keys['d'] * 0.001
            self.x -= held_keys['a'] * 0.001
            self.y += held_keys['w'] * 0.001
            self.y -= held_keys['s'] * 0.001
        # print(time.time()-self.gameLast,self.timeListForSelf[self.currentChart])

        if self.currentChart < len(self.timeListForSelf):
            if time.time()-self.gameLast >= list(self.timeListForSelf.keys())[self.currentChart]:
                tailLength = self.timeListForSelf[list(self.timeListForSelf.keys())[self.currentChart]]
                Note(
                    bindArrow=self,
                    originY=self.unitDis*self.trackLength,
                    speed=self.unitDis,parent=self.parent,
                    tailLength=tailLength,
                    trackId=self.arrowId,
                    generateTime=list(self.timeListForSelf.keys())[self.currentChart],
                    startTime=self.startTime
                )
                self.currentChart += 1

    def input(self,event):

        if event == settings.keys[self.arrowId]:
            try:
                if not settings.autoPlay:
                    chart = find_nearest_specific_entity(self)
                    chart.chartPress()
            except Exception:
                pass


class GameSurface(Entity):
    def __init__(self,surfaceLength,unitDis,autoplay=False):
        super().__init__(z=1.2)

        self.surfaceLength = surfaceLength
        self.unitDis = unitDis
        self.autoplay = autoplay
        self.timeList = unit2time()
        self.started = False
        self.startLast = time.time()
        self.offset = self.surfaceLength/200
        self.startTime = time.time()

        self.arrow1 = Round(0, parent=self, timeList=self.timeList, trackLength=surfaceLength, unitDis=unitDis,
                            autoPlay=autoplay,startTime=self.startTime)
        self.arrow2 = Round(1, parent=self, timeList=self.timeList, trackLength=surfaceLength, unitDis=unitDis,
                            autoPlay=autoplay,startTime=self.startTime)
        self.arrow3 = Round(2, parent=self, timeList=self.timeList, trackLength=surfaceLength, unitDis=unitDis,
                            autoPlay=autoplay,startTime=self.startTime)
        self.arrow4 = Round(3, parent=self, timeList=self.timeList, trackLength=surfaceLength, unitDis=unitDis,
                            autoPlay=autoplay,startTime=self.startTime)

        # Entity(
        #     model='quad',
        #     scale=(30,0.001,1),
        #     parent=self,
        #     z=self.world_z,
        #     y=self.arrow1.y - (self.unitDis*windowRange/1000*200)
        #
        # )

    def update(self):
        # print_on_screen(abs(self.arrow1.y - (self.unitDis * windowRange / 1000 * 200)))
        # print_on_screen(300 - int(0))

        # print_on_screen()
        if settings.debugMode:
            print_on_screen(self.arrow1.x)

        if not self.started and time.time() >= self.startLast + self.offset:
            # print(True)
            self.sound = Audio('./assets/song/song.ogg')
            self.started = True







# class NoteShadow(Entity):
#     def __init__(self,bindChart):
#         super().__init__()
#         self.model = 'quad'
#         self.texture = './assets/images/note.png'
#         self.parent = bindChart.parent
#         self.scale = bindChart.scale
#         self.position = bindChart.position
#         self.aniLast = time.time()
#         self.alpha = 0.6
#
#     def update(self):
#         if time.time() >= self.aniLast + 1/200:
#             self.alpha -= 0.01
#             self.aniLast = time.time()
#
#         if self.alpha <= 0.02:
#             destroy(self)
#             return
# 卡成史

class Note(Entity):
    def __init__(self,bindArrow,originY,parent,speed,tailLength,trackId,generateTime,startTime):
        super().__init__()
        self.model = 'quad'
        self.parent = parent
        # self.x = 1
        self.scale = bindArrow.scale
        self.texture = './assets/images/note.png'
        self.y = bindArrow.y - originY
        self.bindArrow = bindArrow
        self.speed = speed
        self.originY = self.y
        self.x = bindArrow.x
        self.z = -0.000001
        self.speed = speed
        # self.unitId
        self.aniLast = time.time()
        self.missed = False
        self.trackId = trackId
        self.startTime = startTime
        self.aniLast = startTime + generateTime
        self.tail = Tail(bindObj=self, length_unit=tailLength, parent=self.parent, unitDis=self.speed)


        chartEntity.append(self)

        self.genShadowLast = time.time()


    def update(self):

        global currentMisses
        global currentScore
        global currentDestroy

        # if time.time() >= self.genShadowLast + 0.01:
        #     NoteShadow(self)
        #     self.genShadowLast = time.time()
        # 卡成史

        # print_on_screen(currentDestroy)
        self.y = self.originY + (time.time()-self.aniLast)*200 * self.speed

        if not settings.autoPlay:
            if self.y > self.bindArrow.y + (self.speed*windowRange/1000*200) and not self.missed:
                currentMisses += 1
                healthBars.damage_self()
                currentScore += -100
                self.missed = True
            try:
                if self.y > self.bindArrow.y + (self.speed * windowRange / 1000 * 200) + self.tail.scale_y:
                    destroy(self.tail)
                    destroy(self)
                    chartEntity.remove(self)
            except Exception:
                if self.y > self.bindArrow.y + (self.speed * windowRange / 1000 * 200):
                    destroy(self)
                    chartEntity.remove(self)
        else:
            if self.y >= self.bindArrow.y:
                self.chartPress()
                self.bindArrow.round_inside.pressAni()



        # print(self.y)

    def input(self,event):
        global currentPressChart
        global currentDestroy

    def chartPress(self):
        global currentScore
        if self.y >= self.bindArrow.y - (self.speed*windowRange/1000*200):
            self.tail.bindObj = self.bindArrow
            if not settings.autoPlay:
                self.tail.needHold = True
            healthBars.damage_enemy()
            if not settings.autoPlay:
                currentScore += int(300 - 300*(abs(self.bindArrow.y - self.y)/(self.speed * windowRange / 1000 * 200)))
            else:
                currentScore += 300
            destroy(self)
            chartEntity.remove(self)


class Tail(Entity):
    def __init__(self,bindObj,length_unit,parent,unitDis):
        super().__init__()



        self.model = 'quad'
        self.origin_y = 0.5
        self.parent = parent


        self.texture = './assets/images/holdRect.png'

        self.scale = (bindObj.scale_x * 0.3, length_unit * unitDis)
        self.bindObj = bindObj
        self.unitDis = unitDis
        self.needHold = False

        self.length_unit = length_unit
        self.needHoldLast = False
        self.missed = False

    def update(self):
        global currentScore
        global currentMisses

        # if self.scale_y <= 1 ^ 20:

        if self.scale_y <= 9.999999717180685e-7:
            destroy(self)
            return

        try:
            if not held_keys[settings.keys[self.bindObj.arrowId]]:
                self.needHold = False
        except Exception:
            pass

        if (self.needHold and not self.needHoldLast):
            self.aniLast = time.time()
            self.scale_y -= (self.y - self.bindObj.y)
            self.aniStart = self.scale_y
            self.needHoldLast = True
            self.damageLast = time.time()

        if self.needHold:
            self.scale_y = (self.aniStart-((time.time()-self.aniLast)*200*self.unitDis))
            if time.time() >= self.damageLast + 0.3:
                healthBars.damage_enemy()
                currentScore += 50
                self.damageLast = time.time()

        elif not self.needHold and isinstance(self.bindObj, Round):
            if not settings.autoPlay:
                if not self.missed:
                    currentMisses += 1
                    self.missed = True
                self.alpha -= 0.01
                if self.alpha <= 0.02:
                    destroy(self)
                    return
            else:
                self.bindObj.round_inside.pressAni()
                if not self.needHoldLast:
                    self.aniLast = time.time()
                    self.scale_y -= (self.y - self.bindObj.y)
                    self.aniStart = self.scale_y
                    self.needHoldLast = True
                    self.damageLast = time.time()
                self.scale_y = (self.aniStart - ((time.time() - self.aniLast) * 200 * self.unitDis))
                if time.time() >= self.damageLast + 0.3:
                    healthBars.damage_enemy()
                    currentScore += 50
                    self.damageLast = time.time()


        self.x = self.bindObj.x
        self.z = self.bindObj.z
        self.y = self.bindObj.y

    def input(self,event):
        pass
        # print(event)




# Note(gameSuface.arrow1,originY=5,speed=0.3)
# Note(gameSuface.arrow2,originY=5,speed=0.3)
# Note(gameSuface.arrow3,originY=5,speed=0.3)
# Note(gameSuface.arrow4,originY=5,speed=0.3)

def update():
    global currentScore
    currentScore = int(currentScore)
    # print(currentScore)
    gameUi.score.text = 'Score:'+str(currentScore)
    gameUi.misses.text = 'Misses:'+str(currentMisses)




if __name__ == '__main__':
    app = Ursina()
    EditorCamera()

    window.borderless = False
    app.run()


