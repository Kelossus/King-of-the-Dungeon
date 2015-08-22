﻿from time import clock
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

        self.soldiers = Queue()
        self.necromancers = 0
        self.hunters = Queue()

        self.dynamic_layer = dynamic_layer
        self.hud_layer = hud_layer

        self.current_wave = 0

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

                
                self.soldiers.put((minion, data.soldiers[minion][0]))
                if minion == 'madgnome':
                    self.soldiers.put((minion, data.soldiers[minion][0]))
                    self.soldiers.put((minion, data.soldiers[minion][0]))
                elif minion == 'necromancer':
                    self.necromancers += 1
                self.dynamic_layer.invoke(minion)
                return True
        else:
            corpses = self.corpses - data.farmers[minion][1]

            if corpses >= 0:
                self.corpses = corpses
                self.farmers[minion] += 1
                self.dynamic_layer.invoke(minion)
                return True
        return False

    def load_next_wave(self):
        self.current_wave += 1
        for i in range(data.waves):
            for j in range(data.waves[i]):
                self.hunters.put(data.hunters[i])

    def update(self):
        self.hud_layer.update(self.corpses, self.weapons, self.gold,
                              self.farmers['miner'], self.farmers['gatherer'])
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
        soldier = self.soldiers.get()
        hunter = self.hunters.get()

        if soldier[0] == 'orc' and not data.orc_berserk_chance < random():
            hunter[1][1] -= soldier[1][0]
            if not hunter[1][1] > 0:
                self.soldiers.put(soldier)
                return

        hunter[1][1] -= soldier[1][0]
        soldier[1][1] -= hunter[1][0]

        if soldier[1][1] > 0 or not self.necromancers * data.necromancer_revival_chance < random:
            self.soldiers.put(soldier)
        if hunter[1][1] > 0:
            self.hunters.put(hunter)


Logic.register_event_type("on_gold_gain")