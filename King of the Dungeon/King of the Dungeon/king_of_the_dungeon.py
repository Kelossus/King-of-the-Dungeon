import random
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.menu import Menu, ImageMenuItem, MenuItem, fixedPositionMenuLayout
from cocos.actions import *

from pyglet.image import load_animation
from pyglet.media import load, Player

from data import *

from logic import Gold, Logic
from math import floor

class HuntersLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]
        self.background_sprite = Sprite("resources/HuntersMenu.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)

    def on_mouse_press (self, x, y, buttons, modifiers):
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        if self.posx <  420  and self.posy > 620: 
            director.pop()

class SoldiersLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]
        self.background_sprite = Sprite("resources/SoldiersMenu.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)

    def on_mouse_press (self, x, y, buttons, modifiers):
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        if self.posx <  420  and self.posy > 620:
            director.pop()

class WaveReportMenu(Menu):
        def __init__(self, logic):
           super().__init__()

           self.logic = logic

           self.create_menu([MenuItem("START WAVE", self.start_stage)],
                         activated_effect=None,
                         selected_effect=ScaleBy(2, duration = 0.5),
                         unselected_effect=Reverse(ScaleBy(2, duration = 0.5)),
                         layout_strategy=fixedPositionMenuLayout([(800, 110)]))

        def start_stage(self):
            self.logic.stage = True
            self.parent.do(Hide())

class WaveReportLayer(Layer):

    def __init__(self):
        super().__init__()

        ws = director.get_window_size()

        color_fill = ColorLayer(0, 191, 255, 255, height = 800, width = 800)
        color_fill.position = (250, 0)
        self.add(color_fill)

        self.add(Label("REPORT OF THE NEXT WAVE", font_size = 34, x = 320, y = 700))
        self.add(Label("Vagabonds: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 600))
        self.add(Label("Militiars: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 550))
        self.add(Label("Looters: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 500))
        self.add(Label("Defendors: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 450))
        self.add(Label("Agressors: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 400))
        self.add(Label("Champions: ", color = (255, 255, 255, 255), font_size = 32, x = 400, y = 350))

        self.vaga_count = Label("0",  font_size = 32, x = 750, y = 600)
        self.mili_count = Label("0",  font_size = 32, x = 750, y = 550)
        self.loot_count = Label("0",  font_size = 32, x = 750, y = 500)
        self.defe_count = Label("0",  font_size = 32, x = 750, y = 450)
        self.agre_count = Label("0",  font_size = 32, x = 750, y = 400)
        self.cham_count = Label("0",  font_size = 32, x = 750, y = 350)

        self.add(self.vaga_count)
        self.add(self.mili_count)
        self.add(self.loot_count)
        self.add(self.defe_count)
        self.add(self.agre_count)
        self.add(self.cham_count)

    def show(self, vagabound, militia, looter, defender, agressor, champion):
        

        self.vaga_count.element.text = str(vagabound)
        self.mili_count.element.text = str(militia)
        self.loot_count.element.text = str(looter)
        self.defe_count.element.text = str(defender)
        self.agre_count.element.text = str(agressor)
        self.cham_count.element.text = str(champion)
        self.do(Show())

class HUDLayer(Layer):
    def __init__(self):
        super().__init__()

        # Resources

        self.count_corpses = Label("", x=-210, y=795, font_size = 18, color = (0, 0, 0, 255))
        self.count_weapons = Label("", x=-55, y=795, font_size = 18, color = (0, 0, 0, 255))
        self.count_gold = Label("0", x=120, y=795, font_size = 18, color = (0, 0, 0, 255))

        self.add(self.count_corpses)
        self.add(self.count_weapons)
        self.add(self.count_gold)

        # Farmers count

        self.count_gatherers = Label("0", x=280, y=795, font_size = 18, color = (0, 0, 0, 255))
        self.count_miners = Label("0", x=380, y=795, font_size = 18, color = (0, 0, 0, 255))

        self.add(self.count_gatherers)
        self.add(self.count_miners)

        # Farmers stats

        self.cost_gatherers = Label(str(farmers['gatherer'][0]) + "C", x=980, y=795, font_size = 18, color = (0, 0, 0, 255))
        self.cost_miners = Label(str(farmers['miner'][0]) + "C", x=1080, y=795, font_size = 18, color = (0, 0, 0, 255))

        self.add(self.cost_gatherers)
        self.add(self.cost_miners)

        # Soldiers

        self.count_goblins = Label("0", x=-180, y=630, font_size = 18, color = (0, 0, 0, 255))
        self.spec_goblins = Label(str(soldiers['goblin'][0][0]) + '/' +
                                  str(soldiers['goblin'][0][1]) + " | " +
                                  str(soldiers['goblin'][1]) + 'C ' +
                                  str(soldiers['goblin'][2]) + 'W',
                                  x=-270, y=590, font_size = 14, color = (0, 0, 0, 255))

        self.count_hobgoblins = Label("0", x=-180, y=520, font_size = 18, color = (0, 0, 0, 255))
        self.spec_hobgoblins = Label(str(soldiers['hobgoblin'][0][0]) + '/' +
                                     str(soldiers['hobgoblin'][0][1]) + " | " +
                                     str(soldiers['hobgoblin'][1]) + 'C ' +
                                     str(soldiers['hobgoblin'][2]) + 'W',
                                     x=-270, y=480, font_size = 14, color = (0, 0, 0, 255))

        self.count_orcs = Label("0", x=-180, y=410, font_size = 18, color = (0, 0, 0, 255))
        self.spec_orcs = Label(str(soldiers['orc'][0][0]) + '/' +
                               str(soldiers['orc'][0][1]) + " | " +
                               str(soldiers['orc'][1]) + 'C ' +
                               str(soldiers['orc'][2]) + 'W',
                               x=-275, y=360, font_size = 14, color = (0, 0, 0, 255))

        self.count_madgnomes = Label("0", x=-180, y=290, font_size = 18, color = (0, 0, 0, 255))
        self.spec_madgnomes = Label(str(soldiers['madgnome'][0][0]) + '/' +
                                        str(soldiers['madgnome'][0][1]) + " | " +
                                        str(soldiers['madgnome'][1]) + 'C ' +
                                        str(soldiers['madgnome'][2]) + 'W',
                                        x=-275, y=240, font_size = 14, color = (0, 0, 0, 255))

        self.count_necromancers = Label("0", x=-180, y=160, font_size = 18, color = (0, 0, 0, 255))
        self.spec_necromancers = Label(str(soldiers['necromancer'][0][0]) + '/' +
                                           str(soldiers['necromancer'][0][1]) + " | " +
                                           str(soldiers['necromancer'][1]) + 'C ' +
                                           str(soldiers['necromancer'][2]) + 'W',
                                           x=-280, y=110, font_size = 14, color = (0, 0, 0, 255))
        self.add(self.count_goblins)
        self.add(self.spec_goblins)

        self.add(self.count_hobgoblins)
        self.add(self.spec_hobgoblins)

        self.add(self.count_orcs)
        self.add(self.spec_orcs)

        self.add(self.count_madgnomes)
        self.add(self.spec_madgnomes)

        self.add(self.count_necromancers)
        self.add(self.spec_necromancers)

        # Hunters
        
        self.count_vagabound = Label("0", x=1440, y=635, font_size = 18, color = (0, 0, 0, 255))
        self.spec_vagabound = Label(str(hunters['vagabound'][0])+ '/' +
                                    str(hunters['vagabound'][1]),
                                    x=1440, y=595, font_size = 16, color = (0, 0, 0, 255))

        self.count_militia = Label("0", x=1440, y=540, font_size = 18, color = (0, 0, 0, 255))
        self.spec_militia = Label(str(hunters['militia'][0]) + '/' +
                                  str(hunters['militia'][1]),
                                  x=1440, y=500, font_size = 16, color = (0, 0, 0, 255))

        self.count_looter = Label("0", x=1440, y=435, font_size = 18, color = (0, 0, 0, 255))
        self.spec_looter = Label(str(hunters['looter'][0]) + '/' +
                                 str(hunters['looter'][1]),
                                 x=1440, y=390, font_size = 16, color = (0, 0, 0, 255))

        self.count_agressor = Label("0", x=1440, y=325, font_size = 18, color = (0, 0, 0, 255))
        self.spec_agressor = Label(str(hunters['agressor'][0]) + '/' +
                                   str(hunters['agressor'][1]),
                                   x=1440, y=285, font_size = 16, color = (0, 0, 0, 255))

        self.count_defender = Label("0", x=1440, y=205, font_size = 18, color = (0, 0, 0, 255))
        self.spec_defender = Label(str(hunters['defender'][0]) + '/' +
                                   str(hunters['defender'][1]),
                                   x=1440, y=165, font_size = 16, color = (0, 0, 0, 255))

        self.count_champion = Label("0", x=1440, y=100, font_size = 18, color = (0, 0, 0, 255))
        self.spec_champion = Label(str(hunters['champion'][0]) + '/' +
                                   str(hunters['champion'][1]),
                                   x=1440, y=55, font_size = 16, color = (0, 0, 0, 255))
        
        self.add(self.count_vagabound)
        self.add(self.spec_vagabound)

        self.add(self.count_militia)
        self.add(self.spec_militia)

        self.add(self.count_looter)
        self.add(self.spec_looter)

        self.add(self.count_agressor)
        self.add(self.spec_agressor)

        self.add(self.count_defender)
        self.add(self.spec_defender)

        self.add(self.count_champion)
        self.add(self.spec_champion)

    def update(self, corpses, weapons, gold, miners, gatherers, goblins, hobgoblins, orcs,
               madgnomes, necromancers, vagabounds, militians, looters, agressors, defenders, champions):
        self.count_corpses.element.text = str(corpses)
        self.count_weapons.element.text = str(weapons)
        self.count_gold.element.text = str(gold)
        self.count_gatherers.element.text = str(gatherers)
        self.count_miners.element.text = str(miners)
        self.count_goblins.element.text = str(goblins)
        self.count_hobgoblins.element.text = str(hobgoblins)
        self.count_orcs.element.text = str(orcs)
        self.count_madgnomes.element.text = str((madgnomes)//3)
        self.count_necromancers.element.text = str(necromancers)
        self.count_vagabound.element.text = str(vagabounds)
        self.count_militia.element.text = str(militians)
        self.count_looter.element.text = str(looters)
        self.count_agressor.element.text = str(agressors)
        self.count_defender.element.text = str(defenders)
        self.count_champion.element.text = str(champions)

class GUILayer(Menu):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        positions = []
        houses = []
        self.cds = []
        
        ############   goblin house    ###################
        house_goblin = ImageMenuItem("resources/goblin_quarters.png",
                                     self.spawn, "goblin", 0)
        house_goblin.scale = house_scale
        houses.append(house_goblin)
        positions.append(spawn_place.get("goblin"))
        self.cds.append(False)

        ############  hobgoblin house  ###################

        house_hobgoblin = ImageMenuItem("resources/hobgoblin_quarters.png",
                                        self.spawn, "hobgoblin", 1)
        house_hobgoblin.scale = house_scale
        houses.append(house_hobgoblin)
        positions.append(spawn_place.get("hobgoblin"))
        cd_hobgoblin = False
        self.cds.append(False)

        ############     orc  house    ###################

        house_orc = ImageMenuItem("resources/orc_quarters.png",
                                  self.spawn, "orc", 2)
        house_orc.scale = house_scale
        houses.append(house_orc)
        positions.append(spawn_place.get("orc"))
        cd_orc = False
        self.cds.append(False)

        ############  madgnome house   ##################

        house_madgnome = ImageMenuItem("resources/madgnome_quarters.png",
                                       self.spawn, "madgnome", 3)
        house_madgnome.scale = house_scale
        houses.append(house_madgnome)
        positions.append(spawn_place.get("madgnome"))
        cd_madgnome = False
        self.cds.append(False)

        ############ necromancer house ###################

        house_necromancer = ImageMenuItem("resources/necromancer_quarters.png",
                                          self.spawn, "necromancer", 4)
        house_necromancer.scale = house_scale
        houses.append(house_necromancer)
        positions.append(spawn_place.get("necromancer"))
        cd_necromancer = False
        self.cds.append(False)

        ############  gatherer  house  ###################

        house_gatherer = ImageMenuItem("resources/gatherer_quarters.png",
                                       self.spawn, "gatherer", 5)
        house_gatherer.scale = house_scale
        houses.append(house_gatherer)
        positions.append(spawn_place.get("gatherer"))
        cd_gatherer = False
        self.cds.append(False)

        ############   miner   house   ###################

        house_miner = ImageMenuItem("resources/miner_quarters.png",
                                     self.spawn, "miner", 6)
        house_miner.scale = house_scale
        houses.append(house_miner)
        positions.append(spawn_place.get("miner"))
        cd_miner = False
        self.cds.append(False)

        ###########   minion    help   ###################
        minion_help = ImageMenuItem("resources/minion_help.png",
                                    director.push, Scene(SoldiersLayer()))
        minion_help.scale = 4
        houses.append(minion_help)
        positions.append((1500, 810))

        ###########   hero    help     ###################
        hero_help = ImageMenuItem("resources/hero_help.png",
                                    director.push, Scene(HuntersLayer()))
        hero_help.scale = 3.5
        houses.append(hero_help)
        positions.append((1350, 820))

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

    def spawn(self, minion, house_id):
        if not self.cds[house_id]:
            self.logic.spawn(minion)
            self.cds[house_id] = True
            cds = self.cds
            self.do(Delay(building_cool_down) + CallFunc(self.stop_cd, house_id))

    def stop_cd(self, house_id):
        self.cds[house_id] = False

class CollisionLayer(Layer):

    is_event_handler = True

    def __init__(self, logic):
        super().__init__()

        self.logic = logic

    def on_mouse_press (self, x, y, buttons, modifiers):
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        
        for x in self.logic.arena:
            pos, hunter, sprite = x
            if abs(sprite.x - self.posx) < col_radious or abs(sprite.y - self.posy) < col_radious:
                hunter[1][1] -= 1
                if hunter[1][1] <= 0:
                    self.logic.arena.remove(x)
                    self.logic.hunter_each[hunter[0]] -= 1
                    self.logic.arena_grid[pos] = True
                    self.logic.death_sounds[hunter[0]].play()
                    sprite.kill()
                    self.logic.corpses += 1
            
class DynamicLayer(Layer):
    def __init__(self):
        super().__init__()
        self.gathval = True
        self.minval = True
        
    def invoke(self, minion):
        mini = Sprite(load_animation("resources/" + minion + ".gif"), position = spawn_place[minion])
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

    def challenge(self, type, pos):
         hunter = Sprite(load_animation("resources/" + type + ".gif"), position = (random.randint(483, 826), 105))
         hunter.scale = minion_scale
         self.add(hunter)               
         hunter.do(MoveTo(pos, minion_move_time)) 

         return hunter

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


        self.background_sprite = Sprite("resources/background.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)

        self.add(self.background_sprite, z=0)

class RootLayer(Layer):

     is_event_handler = True

     def __init__(self):
        super().__init__()

        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]

        dynamic_layer = DynamicLayer()
        hud_layer = HUDLayer()
        wave_report = WaveReportLayer()
        wave_report.do(Hide())
        self.logic = Logic(dynamic_layer, hud_layer, wave_report,self.win, self.lose)



        self.do(Repeat(CallFunc(self.logic.update) + Delay(update_delay)))

        wave_report.add(WaveReportMenu(self.logic))

        self.add(GroundLayer(),               z=0)
        self.add(StaticLayer(self.logic),     z=1)
        self.add(dynamic_layer,               z=2)
        self.add(CollisionLayer(self.logic),  z=3)
        self.add(GUILayer(self.logic),        z=4)
        self.add(hud_layer,                   z=6)
        self.add(wave_report,                 z=7)

     def on_mouse_press (self, x, y, buttons, modifiers):
        print( director.get_virtual_coordinates (x, y))

     def win(self):
         director.replace(Scene(WinLayer()))
     def lose(self):
         director.replace(Scene(LoseLayer()))
     



class StartLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]
        self.background_sprite = Sprite("resources/StartScreen.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)

    def on_mouse_press (self, x, y, buttons, modifiers):
        director.replace(Scene(RootLayer()))


class WinLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]
        self.background_sprite = Sprite("resources/WinScreen.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)

    def on_mouse_press (self, x, y, buttons, modifiers):
        director.replace(Scene(StartLayer()))


class LoseLayer(Layer):

    is_event_handler = True   

    def __init__(self):
        super().__init__()
        ws = director.get_window_size()
        self.scale_x = ws[0]/window_original[0]
        self.scale_y = ws[1]/window_original[1]
        self.background_sprite = Sprite("resources/LoseScreen.png")
        self.background_sprite.position = (ws[0]/2, ws[1]/2)
        self.add(self.background_sprite, z=0)

    def on_mouse_press (self, x, y, buttons, modifiers):
        director.replace(Scene(StartLayer()))

def main():
    director.init(**window)
    main_scene = Scene(StartLayer())

    player = Player()
    player.queue(load("resources/audios/cave.wav"))
    player.eos_action = player.EOS_LOOP
    player.play()

    director.run(main_scene)


if __name__ == '__main__':
    main()
