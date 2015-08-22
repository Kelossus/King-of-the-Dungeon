import cocos

from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer

class BackgroundLayer(Layer):
    def __init__(self):
        super().__init__()
        self.background_sprite = Sprite("resources/background.png")
        self.add(background_sprite)

def main():
    director.init(resizable=True)

    # Scenes
    main_scene = Scene()

    # Add layers
    main_scene.add(BackgroundLayer(), z=0 )
    # main_scene.add(DataBoard())

    director.run(main_scene)

if __name__ == '__main__':
    main()
