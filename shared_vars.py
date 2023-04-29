from enum import Enum

class PowerupTypes(Enum):
    BOMB = 0
    CHICKEN = 1
    DRUMSTICK = 2
    DUMBBELL = 3
    ROBE = 4

class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    IMPOSSIBLE = 3
    WHACKY = 4

MAX_DIFFICULTY_NUM = 3

DIFFICULTY_MAP = {0 : "Easy", 1 : "Medium", 2 : "Hard", 3 : "Impossible"}

DIFFICULTY_LENGTH = {0 : 60, 1 : 150, 2 : 240, 3 : 300}

WACKY = False

WIDTH = 800
HEIGHT = 600
FLOOR_HEIGHT = 100
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100

DAMAGE_INDICATOR_CAP = 15

difficulty = Difficulty.EASY
game_timer = 0
stage = 1
score = 0
won = False

enemy_health_multiplier = 1
enemy_health_add = 0
enemy_velocity_increase = 1
enemy_spawn_delay_percentage = 0