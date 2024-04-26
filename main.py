#
import random
import sys

from ursina import *

game = Ursina()
import settings
from ui import *
from player import *
from ursina.shaders import camera_vertical_blur_shader
from ursina.shaders.screenspace_shaders.ssao import ssao_shader
from player.player import *


window.borderless = False
# EditorCamera()
from mod import *

mod = Mod()

camera.z = 0



game.run()