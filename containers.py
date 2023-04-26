import shared_vars


class DamageIndicator():
    def __init__(self, text: str, display_length: int, x: float, y: float, is_score: bool):
        self.text = text
        self.display_until = display_length + shared_vars.game_timer
        self.x = x
        self.y = y
        self.is_score = is_score