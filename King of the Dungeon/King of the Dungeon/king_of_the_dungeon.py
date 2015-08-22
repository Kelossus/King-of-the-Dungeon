from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer

from pyglet.image import load_animation

from data import *

class HUDLayer(Layer):
    pass

class GUILayer(Layer):
    pass

class DynamicLayer(Layer):
    pass

class StaticLayer(Layer):
    def __init__(self):
        super().__init__()

        self.monster = Sprite(load_animation("resources/monster.gif"),
               position = monster_pos)

        self.add(self.monster)

class GroundLayer(Layer):
    def __init__(self):
        super().__init__()

        ws = director.get_window_size()

        self.cave_sprite = Sprite("resources/cave.png")
        self.cave_sprite.position = (ws[0]/2, ws[1]/2)

        self.background_sprite = Sprite("resources/background.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)

        self.add(self.background_sprite, z=0)
        self.add(self.cave_sprite, z=1)

class RootLayer(Layer):
    def __init__(self):
        super().__init__()
        
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]

        self.add(GroundLayer(), z=0)
        self.add(StaticLayer(), z=1)

def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    director.run(main_scene)

if __name__ == '__main__':
    main()
