from enum import Enum

class PowerupTypes(Enum):
    BOMB = 0
    CHICKEN = 1
    DRUMSTICK = 2
    DUMBBELL = 3
    ROBE = 4

class Display(Enum):
    EXIT = -1
    HOME = 0
    GAME = 1
    END_GAME = 2

class Difficulty(Enum):
    EASY = 0
    IMPOSSIBLE = 1

MAX_DIFFICULTY_NUM = 1

DIFFICULTY_MAP = {0 : "Easy", 1 : "Impossible"}

WIDTH = 800
HEIGHT = 600
FLOOR_HEIGHT = 100
PLAYER_HEIGHT = 96
PLAYER_WIDTH = 96

DAMAGE_INDICATOR_CAP = 15

display = Display.HOME

difficulty = Difficulty.EASY
game_timer = 0
stage = 1
score = 0

enemy_health_multiplier = 1
enemy_health_add = 1
enemy_velocity_increase = 1
enemy_rate_multiplier = 1