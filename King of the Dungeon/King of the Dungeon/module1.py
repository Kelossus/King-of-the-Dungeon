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
