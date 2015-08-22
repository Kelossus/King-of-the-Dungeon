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

        self.count_goblin = Label("5", x=200, y=800)
        self.count_hobgoblin = Label("0", x=250, y=800)
        self.count_orc = Label("0", x=301, y=800)
        self.count_madgnome = Label("0", x=350, y=800)
        self.count_necro = Label("0", x=400, y=800)
        self.count_miner = Label("0", x=450, y=800)
        self.count_gatherer = Label("0", x=500, y=800)
        self.count_corpses = Label("0", x=10, y=800)
        self.count_weapons = Label("0", x=50, y=820)
        self.count_gold = Label("0", x =100, y=840)

        # self.add(self.count_goblin)
        # self.add(self.count_hobgoblin)
        # self.add(self.count_orc)
        # self.add(self.count_madgnome)
        # self.add(self.count_necro)
        # self.add(self.count_miner)
        # self.add(self.count_gatherer)
        self.add(self.count_corpses)
        self.add(self.count_weapons)
        self.add(self.count_gold)



    def update(self, corpses, weapons, gold, miners, gatherers, goblins, hobgoblins, orcs,
               madgnomes, necromancers):
        self.count_corpses.element.text = str(corpses)
        self.count_weapons.element.text = str(weapons)
        self.count_gold.element.text = str(gold)


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
        self.gathval = True
        self.minval = True


    def invoke(self, minion):
        mini = Sprite(load_animation("resources/"+minion+".gif"), position = spawn_place[minion])
        mini.scale = minion_scale
        self.add(mini) 

        mini.do(MoveBy(minion_move_to[minion], minion_move_time) + CallFunc(mini.kill))
    

    def bring(self, minion):
        if minion == "gatherer":
            if self.gathval:
                mini = Sprite(load_animation("resources/gatherer_coming.gif"), position =(1200, -13))
                mini.scale = minion_scale
                self.add(mini)               
                mini.do(MoveBy((0, 273), minion_move_time) + CallFunc(mini.kill))
                self.gathval = False
            else:
                mini1 = Sprite(load_animation("resources/gatherer.gif"), position = spawn_place[minion])
                mini1.scale = minion_scale
                self.add(mini1)               
                mini1.do(MoveBy(minion_move_to[minion], minion_move_time) + CallFunc(mini1.kill))
                self.gathval = True
        elif minion == "miner":
            if self.minval:
                mini = Sprite(load_animation("resources/miner.gif"), position =(1270, 420))
                mini.scale = minion_scale
                mini.scale_x = -minion_scale
                self.add(mini)               
                mini.do(MoveBy( (-270, 0), minion_move_time) + CallFunc(mini.kill) )
                self.minval = False
            else:
                mini1 = Sprite(load_animation("resources/miner.gif"), position = spawn_place[minion])
                mini1.scale = minion_scale
                self.add(mini1)               
                mini1.do(MoveBy(minion_move_to[minion], minion_move_time) + CallFunc(mini1.kill))
                self.minval = True


class StaticLayer(Layer):
    def __init__(self, logic):
        super().__init__()

        self.monster = Sprite(load_animation("resources/monster.gif"), position = monster_pos)
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

        self.do(Repeat(CallFunc(self.logic.update) + Delay(update_delay)))

        self.add(GroundLayer(),           z=0)
        self.add(StaticLayer(self.logic), z=1)
        self.add(dynamic_layer,           z=2)
        self.add(GUILayer(self.logic),    z=3)
        self.add(hud_layer,               z=4)



def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    director.run(main_scene)

if __name__ == '__main__':
    main()
