from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer

from pyglet.image import load_animation

from data import *

class HUDLayer(Layer):
    def __init__(self):
        super(HUDLayer, self).__init__()

        self.text = cocos.text.Label("aaaa", x=100, y=280 )
        self.add(self.text)


class GUILayer(Layer):
    def __init__(self, hud):
        super(DataBoard, self).__init__()
        self.HUD_ref = hud

        positions = []
        houses = []
        

        ############   goblin house    ###################
        house_goblin = ImageMenuItem("grossini.png", None)
        house_goblin.selected_effect = selected_goblin()
        houses.append(house_goblin)
        positions.append((100,60))

        ############  hobgoblin house  ###################

        house_hobgoblin = ImageMenuItem("grossini.png", None)
        houses.append(house_hobgoblin)
        positions.append((200,60))

        ############     orc  house    ###################

        house_orc = ImageMenuItem("grossini.png", None)
        houses.append(house_orc)
        positions.append((300,60))

        ############  madgnome house   ###################

        house_madgnome = ImageMenuItem("grossini.png", None)
        houses.append(house_madgnome)
        positions.append((400,60))

        ############ necromancer house ###################

        house_necromancer = ImageMenuItem("grossini.png", None)
        houses.append(house_necromancer)
        positions.append((500,60))

        ############    create menu    ###################
        self.create_menu(   houses,
                            activated_effect=self.shake(),
                            selected_effect=None,
                            unselected_effect=None,
                            layout_strategy=fixedPositionMenuLayout(positions))
    def shake(self):
        """Predefined action that performs a slight rotation and then goes back to the original rotation
        position.
        """
        angle = 30
        duration = 0.01

        rot = Accelerate(RotateBy(angle, duration), 2)
        rot2 = Accelerate(RotateBy(-angle * 2, duration), 2)
        return rot + (rot2 + Reverse(rot2)) * 2 + Reverse(rot)

    def selected_goblin(self):
        self.HUD_ref.text.element.text = "this is a very dangerous \n hack"

class DynamicLayer(Layer):
    pass

class StaticLayer(Layer):
    def __init__(self):
        super(StaticLayer, self).__init__()

        self.monster = Sprite(load_animation("resources/monster.gif"),
               position = monster_pos)

        self.add(self.monster)

class GroundLayer(Layer):
    def __init__(self):
        super(GroundLayer, self).__init__()

        ws = director.get_window_size()

        self.cave_sprite = Sprite("resources/cave.png")
        self.cave_sprite.position = (ws[0]/2, ws[1]/2)

        self.background_sprite = Sprite("resources/background.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)

        self.add(self.background_sprite, z=0)
        self.add(self.cave_sprite, z=1)

class RootLayer(Layer):
    def __init__(self):
        super(RootLayer, self).__init__()
        
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]

        self.add(GroundLayer(), z=0)
        self.add(StaticLayer(), z=1)
        hud = HUDLayer()
        self.add(hud,           z=2)
        self.add(GUILayer(hud), z=3)


def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    director.run(main_scene)

if __name__ == '__main__':
    main()
