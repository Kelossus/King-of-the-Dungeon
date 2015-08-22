import random
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer
from cocos.text import Label
from cocos.menu import Menu, ImageMenuItem, MenuItem, fixedPositionMenuLayout
from cocos.actions import *

from pyglet.image import load_animation

from data import *

from logic import Gold, Logic

class HUDLayer(Layer):
    def __init__(self):
        super().__init__()

        self.text = Label("aaaa", x=100, y=280 )
        self.count_goblin = Label("5", x=200, y=300)
        self.count_hobgoblin = Label("0", x=250, y=300)
        self.count_orc = Label("0", x=300, y=300)
        self.count_madgnome = Label("0", x=350, y=300)
        self.count_necro = Label("0", x=400, y=300)
        self.count_miner = Label("0", x=450, y=300)
        self.count_gatherer = Label("0", x=500, y=300)
        self.count_corpses = Label("0", x=550, y=300)

        self.add(self.text)
        self.add(self.count_goblin)
        self.add(self.count_hobgoblin)
        self.add(self.count_orc)
        self.add(self.count_madgnome)
        self.add(self.count_necro)
        self.add(self.count_miner)
        self.add(self.count_gatherer)
        self.add(self.count_corpses)

    def update(self, corpses, weapons, gold, miners, gatherers, orcs):
        pass


class GUILayer(Menu):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic

        positions = []
        houses = []
        
        ############   goblin house    ###################
        house_goblin = ImageMenuItem("resources/goblin_quarters.png",
                                     self.logic.spawn, "goblin")
        house_goblin.scale = house_scale
        houses.append(house_goblin)
        positions.append(spawn_place.get("goblin"))

        ############  hobgoblin house  ###################

        house_hobgoblin = ImageMenuItem("resources/hobgoblin_quarters.png",
                                        self.logic.spawn, "hobgoblin")
        house_hobgoblin.scale = house_scale
        houses.append(house_hobgoblin)
        positions.append(spawn_place.get("hobgoblin"))

        ############     orc  house    ###################

        house_orc = ImageMenuItem("resources/orc_quarters.png",
                                  self.logic.spawn, "orc")
        house_orc.scale = house_scale
        houses.append(house_orc)
        positions.append(spawn_place.get("orc"))

        ############  madgnome house   ##################

        house_madgnome = ImageMenuItem("resources/madgnome_quarters.png",
                                       self.logic.spawn, "madgnome")
        house_madgnome.scale = house_scale
        houses.append(house_madgnome)
        positions.append(spawn_place.get("madgnome"))

        ############ necromancer house ###################

        house_necromancer = ImageMenuItem("resources/necromancer_quarters.png",
                                          self.logic.spawn, "necromancer")
        house_necromancer.scale = house_scale
        houses.append(house_necromancer)
        positions.append(spawn_place.get("necromancer"))

        ############  gatherer  house  ###################

        house_gatherer = ImageMenuItem("resources/gatherer_quarters.png",
                                       self.logic.spawn, "gatherer")
        house_gatherer.scale = house_scale
        houses.append(house_gatherer)
        positions.append(spawn_place.get("gatherer"))

        ############   miner   house   ###################

        house_miner = ImageMenuItem ("resources/miner_quarters.png",
                                     self.logic.spawn, "miner")
        house_miner.scale = house_scale
        houses.append(house_miner)
        positions.append(spawn_place.get("miner"))

        ############    create menu    ###################

        self.create_menu(houses,
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

class DynamicLayer(Layer):
    def __init__(self):
        super().__init__()


    def invoke(self, minion):
        mini = Sprite("resources/"+minion+".gif", position = spawn_place[minion])
        self.add(mini)
        print("ok")
        if minion == "miner":    
            mini.do(MoveBy((200,0), minion_move_time) + CallFunc(mini.kill))
        else:
            mini.do(MoveBy((0,-200), minion_move_time) + CallFunc(mini.kill))
        print("amaihere")




    def bring(self, minion):
        pass

class StaticLayer(Layer):
    def __init__(self, logic):
        super().__init__()

        self.monster = Sprite("resources/monster.gif", position = monster_pos)
       # self.monster = Sprite(load_animation("resources/monster.gif"), position = monster_pos)
        self.gold = Gold(self)

        logic.push_handlers(self.gold)

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

        dynamic_layer = DynamicLayer()
        hud_layer = HUDLayer()
        self.logic = Logic(dynamic_layer, hud_layer)

        self.do(Repeat(CallFunc(self.logic.update) + Delay(1)))

        self.add(GroundLayer(),        z=0)
        self.add(StaticLayer(self.logic),        z=1)
        self.add(dynamic_layer,       z=2)
        self.add(GUILayer(self.logic), z=3)
        self.add(hud_layer,           z=4)



def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    director.run(main_scene)

if __name__ == '__main__':
    main()
