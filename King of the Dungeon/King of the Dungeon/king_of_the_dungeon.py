import random
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.menu import Menu, ImageMenuItem, MenuItem, fixedPositionMenuLayout
from cocos.actions import *

from pyglet.image import load_animation

from data import *

from logic import Gold, Logic

def load_animation(path, *args, **kargs):
    return path

class WaveReportLayer(Menu):
    def __init__(self, logic):
        super().init()

        this.logic = logic

        self.create_menu([MenuItem("START WAVE", self.start_stage)],
                         activated_effect=None,
                         selected_effect=None,
                         unselected_effect=None,
                         layout_strategy=fixedPositionMenuLayout([(1100, 850)]))

        vaga_label = Label("Vagabonds: ")
        vaga_count = Label("")

        militiar_label = Label("Militiars: ")
        militiar_count = Label("")

        looter_label = Label("Looters: ")
        looter_count = Label("")

        defender_label = Label("Defendors: ")
        defender_count = Label("")

        agressor_label = Label("Agressors: ")
        agressor_count = Label("")

        champion_label = Label("Champion: ")
        champion_count = Label("")

        self.add(vaga_label)
        self.add(vaga_count)
        self.add(militiar_label)
        self.add(militiar_count)
        self.add(defender_label)
        self.add(defender_count)
        self.add(agressor_label)
        self.add(agressor_count)
        self.add(champion_label)
        self.add(champion_count)

    def start_page(self):
        self.logic.stage = True
        self.logic.load_next_wave()


class HUDLayer(Layer):
    def __init__(self):
        super().__init__()

        self.background_fill1 = ColorLayer(255, 255, 255, 255, width = 470, height = 100)
        self.background_fill1.position = (-280, 770)

        self.icon_corpses = Sprite("resources/corpses.png", position = (-250, 820))
        self.count_corpses = Label("", x=-210, y=810, font_size = 18, color = (0, 0, 0, 255))

        self.icon_weapons = Sprite("resources/weapons.png", position = (-100, 825), scale = 1.2)
        self.count_weapons = Label("", x=-55, y=810, font_size = 18, color = (0, 0, 0, 255))

        self.icon_gold = Sprite("resources/gold.png", position = (80, 830), scale = 1.4)
        self.count_gold = Label("0", x=150, y=810, font_size = 18, color = (0, 0, 0, 255))

        self.background_fill2 = ColorLayer(255, 255, 255, 255, width = 220, height = 100)
        self.background_fill2.position = (200, 770)

        self.icon_gatherers = Sprite("resources/gatherers.png", position = (240, 820), scale = 1.4)
        self.count_gatherers = Label("0", x=280, y=810, font_size = 18, color = (0, 0, 0, 255))

        self.icon_miners = Sprite("resources/miners.png", position = (340, 820))
        self.count_miners = Label("0", x=380, y=810, font_size = 18, color = (0, 0, 0, 255))

        self.add(self.background_fill1)

        self.add(self.icon_corpses)
        self.add(self.count_corpses)

        self.add(self.icon_weapons)
        self.add(self.count_weapons)

        self.add(self.icon_gold)
        self.add(self.count_gold)

        self.add(self.background_fill2)

        self.add(self.icon_gatherers)
        self.add(self.count_gatherers)

        self.add(self.icon_miners)
        self.add(self.count_miners)

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

    def start_stage(self):
        self.logic.stage = True
        self.logic.load_next_wave()


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

                mini = Sprite(load_animation("resources/gatherer_coming.gif"),
                              position = (spawn_place[minion][0] + minion_move_to[minion][0],
                                          spawn_place[minion][1] + minion_move_to[minion][1]))
                mini.scale = minion_scale
                self.add(mini)               
                mini.do(MoveTo(spawn_place[minion], minion_move_time) + CallFunc(mini.kill))
                self.gathval = False
            else:
                mini1 = Sprite(load_animation("resources/gatherer.gif"), position = spawn_place[minion])
                mini1.scale = minion_scale
                self.add(mini1)               
                mini1.do(MoveBy(minion_move_to[minion], minion_move_time) + CallFunc(mini1.kill))
                self.gathval = True
        elif minion == "miner":
            if self.minval:
                mini = Sprite(load_animation("resources/miner.gif"), 
                            position = (spawn_place[minion ][0] + minion_move_to[minion][0],
                            spawn_place[minion][1] + minion_move_to[minion][1]))
                mini.scale = minion_scale
                mini.scale_x = -minion_scale
                self.add(mini)               
                mini.do(MoveTo( (spawn_place[minion]), minion_move_time) + CallFunc(mini.kill) )
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

        wave_report = WaveReportLayer(self.logic)
        wave_report.do(Hide())

        self.add(GroundLayer(),               z=0)
        self.add(StaticLayer(self.logic),     z=1)
        self.add(dynamic_layer,               z=2)
        self.add(GUILayer(self.logic),        z=3)
        self.add(hud_layer,                   z=4)
        self.add(WaveReportLayer(self.logic), z=5)

class HuntersLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()

        self.background_sprite = Sprite("resources/HuntersMenu.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)
    def on_mouse_press (self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        if self.posx <  250  and self.posy > 930: 
            director.pop()

class SoldiersLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()

        self.background_sprite = Sprite("resources/SoldiersMenu.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)
    def on_mouse_press (self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        if self.posx <  250  and self.posy > 930: 
            director.pop()


def main():
    director.init(**window)
    main_scene = Scene(RootLayer())
    from pyglet.media import load
    director.run(main_scene)


if __name__ == '__main__':
    main()
