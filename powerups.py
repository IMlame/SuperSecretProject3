import arcade

import shared_vars
import spritescaler

FLOOR_HEIGHT = shared_vars.FLOOR_HEIGHT - (shared_vars.PLAYER_HEIGHT / 2)
class Powerup(arcade.Sprite):
    def __init__(self, x: float, y: float, width: int, height: int,
                 powerup_length: int, type: shared_vars.PowerupTypes, velocity: int = 2):
        super().__init__(center_x=x, center_y=y)
        file = "assets/images/test.png"
        if type == shared_vars.PowerupTypes.BOMB:
            file = "assets/images/bomb.png"
        elif type == shared_vars.PowerupTypes.CHICKEN:
            file = "assets/images/CHICKEN.png"
        elif type == shared_vars.PowerupTypes.DRUMSTICK:
            file = "assets/images/drumstick.png"
        elif type == shared_vars.PowerupTypes.DUMBBELL:
            file = "assets/images/dumbbell.png"
        elif type == shared_vars.PowerupTypes.ROBE:
            file = "assets/images/robe.png"
            width = 100
            height = 100
        self.texture = spritescaler.scale(file, width, height)
        self.velocity = velocity
        self.powerup_length = powerup_length
        self.type = type

    def update(self):
        if self.center_y != FLOOR_HEIGHT + self.height / 2:
            if self.center_y - self.velocity < FLOOR_HEIGHT + self.height / 2:
                self.center_y = FLOOR_HEIGHT + self.height / 2
            else:
                self.center_y -= self.velocity
