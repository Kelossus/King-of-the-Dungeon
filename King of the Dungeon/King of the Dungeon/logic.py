from time import clock
from random import random
from queue import Queue

from cocos.sprite import Sprite

from pyglet.image import load
from pyglet.event import EventDispatcher

import data
from data import gold_pos, gold_objective, necromancer_gold_cost

class Gold():
    def __init__(self, parent):
        super().__init__()

        self.images = [load("resources/gold_" + str(i + 1) + '.png') for i in range(4)]
        self.current_index = None
        self.parent = None
        self.update_turn = False
        self.parent = parent

    def on_gold_gain(self, current_value):
        index = len(self.images) * current_value / gold_objective
        if index != self.current_index and index < len(self.images):
            self.current_index = index

            self.parent.remove('gold' + str(int(self.update_turn) + 1))
            self.parent.add(Sprite(self.images[index], position = gold_pos[int(self.update_turn) + 1]))
            self.update_turn = not self.update_turn

class Logic(EventDispatcher):
    def __init__(self, dynamic_layer, hud_layer):
        super().__init__()

        self.corpses = data.start_corpses
        self.weapons = data.start_weapons
        self.gold = data.start_gold

        self.farmers = {
            'miner': 0,
            'gatherer': 0
        }

        self.orcs = 0

        self.soldiers = Queue()

        self.dynamic_layer = dynamic_layer
        self.hud_layer = hud_layer

        

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

                if minion == 'orc':
                    self.orcs += 1
                else:
                    self.soldiers.put(data.soldiers[minion][0])
                    if minion == 'madgnome':
                        self.soldiers.put(data.soldiers[minion][0])
                        self.soldiers.put(data.soldiers[minion][0])
                    print("supersoldier")
                    self.dynamic_layer.invoke(minion)
                return True
        else:
            corpses = self.corpses - data.farmers[minion][1]

            if corpses >= 0:
                self.corpses = corpses
                self.farmers[minion] += 1
                print("chinofarmer")
                self.dynamic_layer.invoke(minion)
                return True
        return False


    def update(self):
        self.hud_layer.update(self.corpses, self.weapons, self.gold,
                              self.farmers['miner'], self.farmers['gatherer'],
                              self.orcs)
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
        pass

Logic.register_event_type("on_gold_gain")