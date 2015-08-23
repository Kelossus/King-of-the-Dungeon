from time import clock
from random import random
from random import shuffle
from queue import Queue

from cocos.sprite import Sprite
from cocos.cocosnode import CocosNode

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

class Logic(CocosNode, EventDispatcher):
    def __init__(self, dynamic_layer, hud_layer):
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

        self.soldiers = list()
        self.hunters = list()

        self.dynamic_layer = dynamic_layer
        self.hud_layer = hud_layer

        self.current_wave = -1
        

    def spawn(self, minion):
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

                
                self.soldiers.append((minion, data.soldiers[minion][0]))

                if minion == 'madgnome':
                    self.soldiers.append((minion, data.soldiers[minion][0]))
                    self.soldiers.append((minion, data.soldiers[minion][0]))
                self.dynamic_layer.invoke(minion)
                self.soldier_each[minion] +=1
                self.hud_layer.update(self.corpses, self.weapons, self.gold,
                self.farmers["miner"], self.farmers["gatherer"], self.soldier_each["goblin"], 
                self.soldier_each["hobgoblin"], self.soldier_each["orc"], self.soldier_each["madgnome"],
                self.soldier_each["necromancer"] )
                return True
        else:
            corpses = self.corpses - data.farmers[minion][0]

            if corpses >= 0:
                self.corpses = corpses
                self.farmers[minion] += 1
                self.dynamic_layer.invoke(minion)
                self.farmers[minion] +=1
                self.hud_layer.update(self.corpses, self.weapons, self.gold,
                self.farmers["miner"], self.farmers["gatherer"], self.soldier_each["goblin"], 
                self.soldier_each["hobgoblin"], self.soldier_each["orc"], self.soldier_each["madgnome"],
                self.soldier_each["necromancer"] )
                return True
        return False

    def load_next_wave(self):
        self.current_wave += 1
        print(self.current_wave, "   ", len(data.waves))
        if (self.current_wave >= len(data.waves)):
            print("you win")
            self.stage = False
            return 

        for i in range(5):
            for j in range(data.waves[self.current_wave][i]):
                self.hunters.append(list(data.hunters[i]))

    def update(self):
        self.hud_layer.update(self.corpses, self.weapons, self.gold,
                 self.farmers["miner"], self.farmers["gatherer"], self.soldier_each["goblin"], 
                 self.soldier_each["hobgoblin"], self.soldier_each["orc"], self.soldier_each["madgnome"],
                 self.soldier_each["necromancer"] )

        if self.stage :
            if len(self.hunters) == 0:
                stage = False
                
            elif len(self.soldiers) == 0:
                self.gold -= len(self.soldiers)
            else:
                self.fight()

                self.farm()

    def farm(self):
        for key in data.farmers:
            success_rate = data.farmers[key][1]
            if not success_rate * self.farmers[key] < random():
                self.corpses += data.farmers[key][2]
                self.weapons += data.farmers[key][3]
                self.gold += data.farmers[key][4]

                self.dispatch_event("on_gold_gain", self.gold)

                self.dynamic_layer.bring(key)

    def fight(self):
       
        soldier = self.soldiers.pop(0)
        hunter = self.hunters.pop(0)
        if soldier[0] == 'orc' and not data.orc_berserk_chance < random():
            hunter[1] -= soldier[1][0]
            if not hunter[1] > 0:
                self.soldiers.append(soldier)
                return
        if not (self.soldier_each["necromancer"] * data.necromancer_revival_chance < random()):
            soldier[1][1] -= hunter[0]

        hunter[1] -= soldier[1][0]


        if soldier[1][1] > 0 :
            self.soldiers.append(soldier)
        if hunter[1] > 0:
            self.hunters.append(hunter)



Logic.register_event_type("on_gold_gain")