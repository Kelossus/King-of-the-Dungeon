class Gold:
    def __init__(self):
        self.sprites = [Sprite("resource/gold_" + str(i + 1)) for i in range(4)]
        self.last_sprite = None