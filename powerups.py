import arcade

import constants
import spritescaler


FLOOR_HEIGHT = constants.FLOOR_HEIGHT - (constants.PLAYER_HEIGHT / 2)
# invincibility (robe)
# health (chicken)
class Powerup(arcade.Sprite):
    def __init__(self, x: float, y: float, width: int, height: int, file: str,
                 powerup_length: int, type: constants.PowerupTypes, velocity: int = 2):
        super().__init__(center_x=x, center_y=y)
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
