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

from singletons import gold, logic

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


class GUILayer(Menu):
    def __init__(self, hud):
        super().__init__()
        self.HUD_ref = hud

        positions = []
        houses = []
        
        ############   goblin house    ###################
        house_goblin = ImageMenuItem("resources/goblin_quarters.png", self.spawn_goblin)
        houses.append(house_goblin)
        positions.append((100,60))

        ############  hobgoblin house  ###################

        house_hobgoblin = ImageMenuItem("resources/hobgoblin_quarters.png", self.spawn_hobgoblin)
        houses.append(house_hobgoblin)
        positions.append((200,60))

        ############     orc  house    ###################

        house_orc = ImageMenuItem("resources/orc_quarters.png", self.spawn_orc)
        houses.append(house_orc)
        positions.append((300,60))

        ############  madgnome house   ##################

        house_madgnome = ImageMenuItem("resources/madgnome_quarters.png", self.spawn_madgnome)
        houses.append(house_madgnome)
        positions.append((400,60))

        ############ necromancer house ###################

        house_necromancer = ImageMenuItem("resources/necromancer_quarters.png", self.spawn_necromancer)
        houses.append(house_necromancer)
        positions.append((500,60))

        ############  gatherer  house  ###################

        house_gatherer = ImageMenuItem("resources/gatherer_quarters.png", self.spawn_gatherer)
        houses.append(house_gatherer)
        positions.append((600, 60))

        ############   miner   house   ###################

        house_miner = ImageMenuItem ("resources/miner_quarters.png", self.spawn_miner)
        houses.append(house_miner)
        positions.append((700,60))

        ############   attack button   ###################

        attack_button = MenuItem("ATTACK", None)
        houses.append(attack_button)
        positions.append((1000, 500))

        ############    create menu    ###################

        self.create_menu(houses,
                         activated_effect=self.shake(),
                         selected_effect=None,
                         unselected_effect=None,
                         layout_strategy=fixedPositionMenuLayout(positions))


        ############    animations     ###################

        house_goblin.selected_effect = self.selected_goblin()
        house_hobgoblin.selected_effect = self.selected_hobgoblin()
        house_orc.selected_effect = self.selected_orc()
        house_madgnome.selected_effect = self.selected_madgnome()
        house_necromancer.selected_effect = self.selected_necromancer()
        house_gatherer.selected_effect = self.selected_gatherer()
        house_miner.selected_effect = self.selected_miner()


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

    def selected_hobgoblin(self):
        self.HUD_ref.text.element.text = "this is a hobvery dangerous \n hack"

    def selected_orc(self):
        self.HUD_ref.text.element.text = "this is a orcstremely dangerous \n hack"

    def selected_madgnome(self):
        self.HUD_ref.text.element.text = "dude, it even says mad \n hack"

    def selected_necromancer(self):
        self.HUD_ref.text.element.text = "corpse and shit \n\n backstab"

    def selected_gatherer(self):
        self.HUD_ref.text.element.text = "looter \n\n backstab"

    def selected_miner(self):
        self.HUD_ref.text.element.text = "pickaxe \n poor worker"

    # Spawnning

    def spawn_goblin(self):
        pass

    def spawn_hobgoblin(self):
        pass

    def spawn_orc(self):
        pass

    def spawn_madgnome(self):
        pass

    def spawn_necromancer(self):
        pass

    def spawn_gatherer(self):
        pass

    def spawn_miner(self):
        pass

    def attack(self):

        minion_list = list()

        for i in range (0,int(self.HUD_ref.count_goblin.element.text)):
            minion_list.append(soldiers.get("goblin")[0])

        for i in range (0,int(self.HUD_ref.count_hobgoblin.element.text)):
            minion_list.append(soldiers.get("hobgoblin")[0])

        for i in range (0,int(self.HUD_ref.count_orc.element.text)):
            minion_list.append(soldiers.get("orc")[0])

        for i in range (0,int(self.HUD_ref.count_madgnome.element.text)):
            minion_list.append(soldiers.get("madgnome")[0])

        for i in range (0,int(self.HUD_ref.count_necro.element.text)):
            minion_list.append(soldiers.get("necromancer")[0])

        random.shuffle(minion_list)

        horde_count = 0

        hunter_list = list()

        for i in range (4):
            for j in range(waves[horde_count-1][i]):
                hunter_list.append(hunters[i])

        hunter_list = [[ hunters[i]
                             for j in range(0, waves[horde_count-1][i])]
                                    for i in range(0,4) ]

        random.shuffle(hunter_list)

        print (minion_list)
        print (hunter_list)

        # self.count_goblin = Label("5", x=200, y=300)
        # self.count_hobgoblin = Label("0", x=250, y=300)
        # self.count_orc = Label("0", x=300, y=300)
        # self.count_madgnome = Label("0", x=350, y=300)
        # self.count_necro = Label("0", x=400, y=300)
        # self.count_miner = Label("0", x=450, y=300)
        # self.count_gatherer = Label("0", x=500, y=300)
        # self.count_corpses = Label("0", x=550, y=300)


class DynamicLayer(Layer):
    pass

class StaticLayer(Layer):
    def __init__(self):
        super().__init__()

        self.monster =  Label("fuck you monstwr", x=700, y=500 )
        # self.monster = Sprite(load_animation("resources/monster.gif"),
        #        position = monster_pos)

        gold.init(self)


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
        hud = HUDLayer()
        self.add(hud,           z=2)
        self.add(GUILayer(hud), z=3)


def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    director.run(main_scene)

if __name__ == '__main__':
    main()
