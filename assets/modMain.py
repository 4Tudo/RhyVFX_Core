from ursina import *
from player.player import *
from ursina.camera import *
from .decorations import *
from .shaders import *
from ursina.shaders.screenspace_shaders.camera_vertical_blur import camera_vertical_blur_shader
from ursina.shaders.screenspace_shaders.ssao import ssao_shader


# camera.shader = Shader(fragment=open('./assets/effects.fsh','r').read())
camera.shader = camera_vertical_blur_shader


window.color = color.black

gameSurface = GameSurface(surfaceLength=500, unitDis=0.006, autoplay=True)

jitterAllowed = True


genInterval = 10
last = time.time()

for i in range(3,23):
    Cities(z=i,x=0,x_offset=20)
    Cities(z=i,x=20,x_offset=20)


Flash(
    [
        (color.black,0),
        (color.clear,4)
    ]
)
skyLight = SkyLight()
camera.fov = 60


cameraShadow = Entity(
    model='quad',
    parent=camera.ui,
    texture='./assets/images/camera_shadow.png',
    scale=(2,1,1),
    color=(50,50,50)
)



def cameraJitter(strength,time):
    if jitterAllowed:
        camera.animate_position(
            (
                camera.x,
                camera.y,
                camera.z + strength
            ),
            duration=0
        )
        camera.animate_position(
            (
                camera.x,
                camera.y,
                camera.z - strength
            ),
            duration=time,
            curve=curve.out_cubic
        )


class CameraShake(Entity):

    def __init__(self,shake_obj):
        super().__init__()
        self.amplitude = 0.02
        # self.duration = 0.4
        self.duration = 60 / 155.01 * 4
        self.curve = curve.in_out_sine

        self.rotate_amplitude = 5

        self.last = time.time()

        # self.shake_obj = Entity(model='cube',
        #                   color=color.orange)
        self.shake_obj = shake_obj
        self.shake_allowed = True

    def update(self):

        if time.time() >= self.last + self.duration and self.shake_allowed:
            if time.time() >= self.last + self.duration and self.shake_allowed:
                self.shake_obj.animate_position((
                    random.uniform(self.amplitude, -self.amplitude),
                    random.uniform(self.amplitude, -self.amplitude),
                    random.uniform( + self.amplitude,  - self.amplitude)
                ),
                    duration=self.duration,
                    curve=self.curve)

            self.shake_obj.animate_rotation((
                # random.uniform(self.rotate_amplitude,-self.rotate_amplitude),
                # random.uniform(self.rotate_amplitude,-self.rotate_amplitude),
                0,
                0,
                random.uniform(self.rotate_amplitude,-self.rotate_amplitude)
            ),
            duration=self.duration,
            curve=self.curve)
            # print(camera.fov)


            self.last = time.time()



class GameLoop(Entity):
    def __init__(self):
        super().__init__()
        self.jitterLast = time.time()
        self.gameLast = time.time() + gameSurface.surfaceLength/200
        print(gameSurface.surfaceLength/200)

        self.changeStateFlashDone = False
        self.camChangeToCol = False
        self.part2 = False
        self.part3 = False
        self.part3_flash = True
        self.part4 = False
        self.part4_flash = True


    def update(self):
        global last
        global lightly
        global jitterAllowed

        if time.time() >= last+5:
            for i in range(3,23):
                Cities(z=i,x=20,x_offset=20)
            last = time.time()

        if not lightly:
            camera.set_shader_input('blur_size',random.uniform(0.15,0.01))

        if time.time() >= self.jitterLast+60/71 and time.time() >= self.gameLast + 23*60/71 and not self.part2:
            cameraJitter(0.1,0.3)
            self.jitterLast = time.time()

        if time.time() >= self.gameLast + 32*60/71 and not self.changeStateFlashDone:
            Flash([
                (color.clear,0),
                (color.black, 3 * 60 / 71),
                (color.clear, 6 * 60 / 71),
            ])
            camera.set_shader_input('blur_size', 0.15)
            self.changeStateFlashDone = True

        if time.time() >= self.gameLast + 32 * 60 / 71 + 6 * 60 / 71:
            changeLightingState(True)
            cameraShadow.visible = False
            lightly = True

        if time.time() >= self.gameLast + 69 * 60/71 and not self.camChangeToCol:
            camShake.shake_allowed = False
            jitterAllowed = False
            camera.animate_position(
                (1, camera.y, 4),
                duration=0.3,
                curve=curve.in_cubic
            )

            camera.animate_position(
                (-1, 0, -5),
                duration=0,
                curve=curve.in_out_cubic,
                delay=0.32
            )

            camera.animate_position(
                (0, 0, 0),
                duration=0.8,
                curve=curve.out_cubic,
                delay=0.33
            )
            gameSurface.animate_rotation((0,0,-90),
                                         duration=2,
                                         curve=curve.out_cubic,
                                         delay=0.34)
            gameSurface.animate_position((-0.95,0,2),
                                         duration=2,
                                         curve=curve.out_cubic,
                                         delay=0.34)
            self.part2 = True
            self.camChangeToCol = True
            camera.set_shader_input('blur_size', 0.15)


        if time.time() >= self.jitterLast+60/71*0.5 and time.time() >= self.gameLast + 71 * 60/71 and self.part2:
                print(True)
                cameraJitter(0.1,0.3)
                camShake.shake_allowed = True
                self.jitterLast = time.time()



        if time.time() >= self.gameLast + 101 * 60 / 71 and not self.part3:
            camShake.shake_allowed = False
            jitterAllowed = False
            cameraShadow.visible = True
            camera.animate_position(
                (1, camera.y, 4),
                duration=0.3,
                curve=curve.in_cubic
            )
            camera.animate_position(
                (-1, 0, -5),
                duration=0,
                curve=curve.in_out_cubic,
                delay=0.32
            )
            camera.animate_position(
                (0, 0, 0),
                duration=0.8,
                curve=curve.out_cubic,
                delay=0.35
            )
            gameSurface.animate_rotation((0,0,0),
                                         duration=2,
                                         curve=curve.out_cubic,
                                         delay=0.36)
            gameSurface.animate_position((0,0,2),
                                         duration=2.5,
                                         curve=curve.out_cubic,
                                         delay=0.36)
            self.part3 = True
            skyLight.color = color.hex('#cafffb')
            self.part3_blur = True
            self.camChangeToCol = True
            camera.set_shader_input('blur_size', 0.15)

        if time.time() >= self.gameLast + 126*60/71 and self.part3_flash:
            Flash([
                (color.clear,0),
                (color.black, 3 * 60 / 71),
                (color.clear, 6 * 60 / 71),
            ])
            self.part3_flash = False

        if time.time() >= self.gameLast + 132 * 60 / 71 and not self.part4:
            cameraShadow.visible = True


        if time.time() >= self.gameLast + 156*60/71 and not self.part4:
            print(True)
            cameraShadow.animate_color(
                color.clear,
                duration=6 * 60/71,
                curve=curve.in_out_cubic
            )
            gameSurface.animate_rotation((0, 0, 0),
                                         duration=6 * 60/71,
                                         curve=curve.out_cubic,
                                         )
            gameSurface.animate_position((0, 0, 2),
                                         duration=6 * 60/71,
                                         curve=curve.out_cubic,
                                         )
            self.part4 = True









camShake = CameraShake(camera)
cinema1 = CinemaBorder(type='under', size=4.5)
cinema2 = CinemaBorder(type='upper', size=4.5)
GameLoop()

