from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



import cocos

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.actions import *
from cocos.layer import *
from cocos.scenes import *
from cocos.sprite import *

import pyglet

from pyglet import image
from pyglet import font
from pyglet.gl import *

class MainMenu(Menu):
    def __init__( self ):
        super( MainMenu, self ).__init__("TITLE" )

        self.menu_valign = BOTTOM
        self.menu_halign = CENTER

        # then add the items
        items = [
            ( MenuItem('Item 1', self.on_quit ) ),
            ( MenuItem('Item 2', self.on_quit ) ),
            ( MenuItem('Item 3', self.on_quit ) ),
            ( MenuItem('Item 4', self.on_quit ) ),

        ]

        self.create_menu( items, activated_effect=shake())

    def on_quit( self ):
        pyglet.app.exit()




class DataBoard(Menu):
    def __init__(self):
        super(DataBoard, self).__init__()

        positions = []
        houses = []
        self.text = cocos.text.Label("dd", x=100, y=280 )

        ############   goblin house    ###################
        house_goblin = ImageMenuItem("grossini.png", None)

        house_goblin.on_selected

        houses.append(house_goblin)
        positions.append((100,60))

        ############  hobgoblin house  ###################

        house_hobgoblin = ImageMenuItem("grossini.png", None)
        houses.append(house_hobgoblin)
        positions.append((200,60))

        ############     orc  house    ###################

        house_orc = ImageMenuItem("grossini.png", None)
        houses.append(house_orc)
        positions.append((300,60))

        ############  madgnome house   ###################

        house_madgnome = ImageMenuItem("grossini.png", None)
        houses.append(house_madgnome)
        positions.append((400,60))

        ############ necromancer house ###################

        house_necromancer = ImageMenuItem("grossini.png", None)
        houses.append(house_necromancer)
        positions.append((500,60))

        ############    create menu    ###################
        self.create_menu(   houses,
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

    def on_quit( self ):
        pyglet.app.exit()

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')
        self.text = cocos.text.Label("dd", x=100, y=280 )
        self.add (self.text)

    def update_text(self, num):
        
        # Update self.text
        if   num == 0:
            self.text.element.text += " +"

        elif num == 1:
            self.text.element.text += " +"

        elif num == 2:
            self.text.element.text += " +"

        elif num == 3:
            self.text.element.text += " +"

        elif num == 4:
            self.text.element.text += " +"

        elif num == 5:
            self.text.element.text += " +"

    def draw( self ):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        glPopMatrix()

def main():

    pyglet.font.add_directory('.')

    director.init( resizable=True)

    # Scenes
    main_scene = cocos.scene.Scene()


    # Add layers
    main_scene.add( BackgroundLayer(), z=0 )
    main_scene.add(DataBoard())

    director.run( main_scene )

if __name__ == '__main__':
    main()
