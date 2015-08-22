from cocos.sprite import Sprite

from pyglet.image import load
from pyglet.event import EventDispatcher

from data import gold_pos, gold_objective

class Gold():
    def __init__(self):
        super().__init__()

        self.images = [load("resources/gold_" + str(i + 1) + '.png') for i in range(4)]
        self.current_index = None
        self.parent = None
        self.update_turn = False

    def init(self, parent):
        logic.push_handlers(self)
        self.parent = parent

    def on_gold_gain(self, current_value):
        index = 5 * current_value / gold_objective
        if index != self.current_index and index < len(self.images):
            self.current_index = index

            self.parent.remove('gold' + str(int(self.update_turn) + 1))
            self.parent.add(Sprite(self.images[index], position = gold_pos[int(self.update_turn) + 1]))
            self.update_turn = not self.update_turn

class Logic(EventDispatcher):
    pass

Logic.register_event_type("on_gold_gain")

gold = Gold()
logic = Logic()