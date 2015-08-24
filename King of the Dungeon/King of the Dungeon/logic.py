from time import clock
from random import random, shuffle, randint, choice
from queue import Queue

from cocos.sprite import Sprite
from cocos.cocosnode import CocosNode
from cocos.actions import *
from cocos.scene import Scene

import pyglet
from pyglet.image import load
from pyglet.event import EventDispatcher
from pyglet.app import exit

import data
from data import gold_pos, gold_scale, gold_objective, necromancer_gold_cost

class Gold():
    def __init__(self, parent):
        super().__init__()

        self.images = [load("resources/gold_" + str(i + 1) + '.png') for i in range(4)]
        self.current_index = None
        self.parent = None
        self.update_turn = False
        self.parent = parent

    def on_gold_gain(self, current_value):
        index = int(2 * len(self.images) * current_value / gold_objective)
        
        if index != self.current_index and index < len(self.images)*2:
            self.current_index = index
            try:
                self.parent.remove('gold' + str(int(self.update_turn) + 1))
            except:
                pass
            self.parent.add(Sprite(self.images[index//2],
                            position = gold_pos[int(self.update_turn)],
                            scale = gold_scale))
            self.update_turn = not self.update_turn

class Logic(EventDispatcher):
    def __init__(self, dynamic_layer, hud_layer, wave_report, win, lose):
        super().__init__()

        self.corpses = data.start_corpses
        self.weapons = data.start_weapons
        self.gold = data.start_gold
        self.stage = False

        self.farmers = {
            'miner': 0,
            'gatherer': 0
        }

        self.soldier_each = {
            "goblin": 0,
            "hobgoblin": 0,
            "orc": 0,
            "madgnome": 0,
            "necromancer": 0
        }

        self.hunter_each = {
            "vagabound": 0,
            "militia": 0,
            "looter": 0,
            "agressor": 0,
            "defender": 0,
            "champion" : 0
        }

        self.battle_background_sounds = [pyglet.media.load("resources/audios/battle_background/" + str(i) + ".wav", streaming = False) for i in range(10)]

        self.death_sounds = { 
                "goblin": pyglet.media.load("resources/audios/death/goblin.wav", streaming = False),
                "hobgoblin": pyglet.media.load("resources/audios/death/hobgoblin.wav", streaming = False),
                "orc": pyglet.media.load("resources/audios/death/orc.wav", streaming = False),
                "madgnome": pyglet.media.load("resources/audios/death/madgnome.wav", streaming = False),
                "necromancer": pyglet.media.load("resources/audios/death/necro.wav", streaming = False),
                "vagabound": pyglet.media.load("resources/audios/death/vagabound.wav", streaming = False),
                "militia": pyglet.media.load("resources/audios/death/militia.wav", streaming = False),
                "looter": pyglet.media.load("resources/audios/death/looter.wav", streaming = False),
                "agressor": pyglet.media.load("resources/audios/death/agressor.wav", streaming = False),
                "defender": pyglet.media.load("resources/audios/death/defender.wav", streaming = False),
                "champion": pyglet.media.load("resources/audios/death/champion.wav", streaming = False)
        }


        self.soldiers = list()
        self.hunters = list()
        self.arena = list()

        self.arena_grid = {
           (577, 353): True,
           (612, 356): True,
           (716, 352): True,
           (581, 291): True,
           (622, 298): True,
           (667, 303): True,
           (719, 299): True
        }

        self.win = win
        self.lose = lose
        


        self.dynamic_layer = dynamic_layer
        self.hud_layer = hud_layer
        self.wave_report = wave_report

        self.current_wave = -1
        self.load_next_wave()
        
        self.wave_report.show(**self.hunter_each)
        

    def spawn(self, minion):
        if self.stage:
            if minion in data.soldiers:
                corpses = self.corpses - data.soldiers[minion][1]
                weapons = self.weapons - data.soldiers[minion][2]
                gold = self.gold
                if minion == 'necromancer':
                    gold -= necromancer_gold_cost

                if corpses >= 0 and weapons >= 0 and gold >= 0:
                    self.corpses = corpses
                    self.weapons = weapons
                    self.gold = gold
                    self.dispatch_event('on_gold_gain', self.gold)

                
                    self.soldiers.append([minion, data.soldiers[minion][0]])

                    if minion == 'madgnome':
                        self.soldiers.append([minion, data.soldiers[minion][0]])
                        self.soldiers.append([minion, data.soldiers[minion][0]])
                        self.soldier_each[minion] +=2
                    self.dynamic_layer.invoke(minion)
                    self.soldier_each[minion] +=1

                    self.hud_layer.update(self.corpses, self.weapons, self.gold, self.farmers["miner"],
                                  self.farmers["gatherer"], self.soldier_each["goblin"],
                                  self.soldier_each["hobgoblin"], self.soldier_each["orc"],
                                  self.soldier_each["madgnome"], self.soldier_each["necromancer"],
                                  self.hunter_each['vagabound'], self.hunter_each['militia'],
                                  self.hunter_each['looter'], self.hunter_each['agressor'],
                                  self.hunter_each['defender'], self.hunter_each['champion'])

                    return True
            else:
                corpses = self.corpses - data.farmers[minion][0]

                if corpses >= 0:
                    self.corpses = corpses
                    self.farmers[minion] += 1
                    self.dynamic_layer.invoke(minion)
                    self.hud_layer.update(self.corpses, self.weapons, self.gold, self.farmers["miner"],
                                  self.farmers["gatherer"], self.soldier_each["goblin"],
                                  self.soldier_each["hobgoblin"], self.soldier_each["orc"],
                                  self.soldier_each["madgnome"], self.soldier_each["necromancer"],
                                  self.hunter_each['vagabound'], self.hunter_each['militia'],
                                  self.hunter_each['looter'], self.hunter_each['agressor'],
                                  self.hunter_each['defender'], self.hunter_each['champion'])
                    return True
        return False

    def load_next_wave(self):
        if (self.current_wave >= len(list(data.waves.values())[0])-1):
            print("you win")
            self.win()
            self.stage = False
            return 

        self.current_wave += 1
        print(self.current_wave, "   ",  len(list(data.waves.values())[0]))
        k= 0
        for i,j in data.hunters.items():
            print(self.hunters)
            for z in range( data.waves[i][self.current_wave]):
                self.hunter_each[i] += 1
                self.hunters.append((i, list(j)));
        print(self.hunters)

        shuffle(self.hunters)

    def update(self):
        self.hud_layer.update(self.corpses, self.weapons, self.gold, self.farmers["miner"],
                              self.farmers["gatherer"], self.soldier_each["goblin"],
                              self.soldier_each["hobgoblin"], self.soldier_each["orc"],
                              self.soldier_each["madgnome"], self.soldier_each["necromancer"],
                              self.hunter_each['vagabound'], self.hunter_each['militia'],
                              self.hunter_each['looter'], self.hunter_each['agressor'],
                              self.hunter_each['defender'], self.hunter_each['champion'])
        if self.stage :
            print(self.hunters)
            if len(self.hunters) + len(self.arena) == 0 :
                self.stage = False
                self.load_next_wave()
                self.wave_report.show(**self.hunter_each)
                

            else:
                self.farm()

                if len(self.hunters) != 0:
                    self.fight()
                if len(self.arena) != 0:
                    sum = 0
                    for i in self.arena:
                        sum+= i[1][1][0]
                    self.gold -= sum
                    if self.gold < 0:
                        self.gold = 0
                        self.lose()

    def farm(self):
        for key in data.farmers:
            success_rate = data.farmers[key][1]
            i = 0
            while i < self.farmers[key]:
                if not success_rate  < random():
                    self.corpses += data.farmers[key][3]
                    self.weapons += data.farmers[key][4]
                    self.gold += data.farmers[key][2]
                    self.dispatch_event("on_gold_gain", self.gold)
                    self.dynamic_layer.bring(key)
                i+=1

    def fight(self):
        if len(self.soldiers) == 0:
            if True in self.arena_grid.values():
                pos = choice(list(self.arena_grid.keys()))
                while not self.arena_grid[pos]:
                    pos = choice(list(self.arena_grid.keys()))

                self.arena_grid[pos] = False
                hunter = self.hunters.pop(0)
                sprite = self.dynamic_layer.challenge(hunter[0],pos)
                self.arena.append([pos, hunter, sprite])
            return

        soldier = self.soldiers.pop(0)
        hunter = self.hunters.pop(0)

        # fight

        # orc special
        if soldier[0] == 'orc' and not data.orc_berserk_chance < random():
            hunter[1][1] -= soldier[1][0]
            if not hunter[1][1] > 0:
                self.soldiers.append(soldier)
                self.hunter_each[hunter[0]] -= 1
                self.death_sounds[hunter[0]].play()
                return

        # necromancer special
        no_luck = True
        i = 0
        while i < self.soldier_each["necromancer"] and no_luck:
                if not data.necromancer_revival_chance  < random():
                    no_luck = False
                i +=1

        if no_luck:
            soldier[1][1] -= hunter[1][0]
        hunter[1][1] -= soldier[1][0]

        # fight conclussion

        if soldier[1][1] > 0 :
            self.soldiers.append(soldier)
        else:
            self.soldier_each[soldier[0]] -=1

        if hunter[1][1] > 0:
            self.hunters.append(hunter)
        else:
            self.hunter_each[hunter[0]] -= 1

        # audio

        i = randint(0,2)
        if i == 0:
            i = randint(0, len(self.battle_background_sounds) - 1)
            self.battle_background_sounds[i].play()
        else:
            if soldier[1][1] > 0 and not (hunter[1][1] > 0):
                self.death_sounds[hunter[0]].play()
            elif not (soldier[1][1] > 0) and hunter[1][1] > 0:
                self.death_sounds[soldier[0]].play()
            if not (soldier[1][1] > 0) and not (hunter[1][1] > 0):
                i = randint(0,1)
                if i == 0:
                    self.death_sounds[hunter[0]].play()
                else:
                    self.death_sounds[soldier[0]].play()

Logic.register_event_type("on_gold_gain")