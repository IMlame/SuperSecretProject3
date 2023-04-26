"""
Complete game in Arcade

This game demonstrates some of the more advanced features of
Arcade, including:
- Using sprites to render complex graphics
- Handling user input
- Sound output
"""

# Import arcade allows the program to run in Python IDLE
import math

import arcade

# To locate your assets
from pathlib import Path

from enum import Enum
import shared_vars
import enemysummoner
import externalsprites
from externalsprites import Player

# Set the game window title
TITLE = "Jordan VS the World"

# Location of your assets
ASSETS_PATH = Path.cwd() / "assets"

# Classes
class ArcadeGame(arcade.Window):
    """The Arcade Game class"""

    def __init__(self, width: float, height: float, title: str):
        """Create the main game window

        Arguments:
            width {float} -- Width of the game window
            height {float} -- Height of the game window
            title {str} -- Title for the game window
        """

        # Call the super class init method
        super().__init__(int(width), int(height), title)
        # Set control list
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False

        # Game state
        self.score = 0
        # Player
        self.player = None
        # Player constant modifiers
        self.player_bullet_speed = 5
        self.player_move_speed = 10
        self.player_jump_velocity = 20
        self.player_gravity = 1
        self.initial_health = 5
        self.player_damage = 1
        self.player_fire_cooldown = 0.2
        self.player_max_bullets = 3

        # Player state
        self.player_cur_upward_velocity = 0.0
        self.player_next_fire = 0

        # Projectile state
        self.bullet_list = None
        # Enemies/enemy projectiles
        self.enemy_list = None
        # Powerups
        self.powerup_list = None
        # Damage indicator
        self.damage_indicator_list = None
        # Player health
        self.heart = None

        # Enemy spawner
        self.enemy_spawner = None

    def setup(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(color=arcade.color.PINK)

        # Set up the player
        sprite_image = ASSETS_PATH / "images" / "dumbbell.png"
        self.player = Player(
            file=str(sprite_image), x=shared_vars.WIDTH // 2, y=shared_vars.FLOOR_HEIGHT, height=shared_vars.PLAYER_HEIGHT, width=shared_vars.PLAYER_WIDTH)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.damage_indicator_list = []

        self.heart = externalsprites.Heart(x=750, y=shared_vars.HEIGHT - 50, initial_health=self.initial_health, width=96, height=96)

        self.enemy_spawner = enemysummoner.EnemySummoner(enemy_list=self.enemy_list, width=shared_vars.WIDTH, height=shared_vars.HEIGHT, player=self.player, powerup_list=self.powerup_list, damage_indicator_list=self.damage_indicator_list)

    def on_update(self, delta_time: float):
        # movement
        shared_vars.game_timer += delta_time
        self.bullet_list.update()
        self.update_movement()
        # new sprites
        self.update_player_projectile()
        self.powerup_list.update()
        self.enemy_list.on_update(delta_time=delta_time)
        self.enemy_spawner.summon_enemies(delta_time=delta_time)
        # check collisions between objects
        self.collision_check()
        # remove out of bound projectiles
        self.remove_old_projectiles()

    def remove_old_projectiles(self):
        for bullet in self.bullet_list:
            if bullet.bottom > self.height or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

        for projectile in self.enemy_list:
            if projectile.is_projectile and projectile.bottom > self.height or projectile.top < 0 or projectile.right < 0 or projectile.left > self.width:
                projectile.remove_from_sprite_lists()

    def update_movement(self):
        fast_fall_multiplier = 1
        # movement
        if self.left_pressed:
            if self.player.center_x + -self.player_move_speed < 0:
                self.player.center_x = 0
            else:
                self.player.center_x += -self.player_move_speed
        if self.right_pressed:
            if self.player.center_x + self.player_move_speed > shared_vars.WIDTH:
                self.player.center_x = shared_vars.WIDTH
            else:
                self.player.center_x += self.player_move_speed
        if self.up_pressed and self.player.center_y == shared_vars.FLOOR_HEIGHT:
            self.player_cur_upward_velocity = self.player_jump_velocity
        if self.down_pressed and self.player.center_y != shared_vars.FLOOR_HEIGHT:
            fast_fall_multiplier = 4

        # player fall speed
        if (self.player.center_y + self.player_cur_upward_velocity) < shared_vars.FLOOR_HEIGHT:
            self.player.center_y = shared_vars.FLOOR_HEIGHT
            self.player_cur_upward_velocity = 0
        else:
            self.player.center_y += self.player_cur_upward_velocity
            self.player_cur_upward_velocity -= self.player_gravity * fast_fall_multiplier

    def collision_check(self):
        # check for player and enemy collisions
        enemy_collisions = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in enemy_collisions:
            if self.heart.damage(enemy.damage):
                self.end_game()
            self.score += enemy.value
            enemy.death_event()
            enemy.remove_from_sprite_lists()
        # destroy shot enemies
        dead_bullets = []
        for bullet in self.bullet_list:
            enemies_shot = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            dead_enemies = []
            for enemy in enemies_shot:
                enemy_health = enemy.health
                if enemy.sustain_damage(bullet.health):
                    self.score += enemy.value
                    dead_enemies.append(enemy)
                if bullet.sustain_damage(enemy_health):
                    dead_bullets.append(bullet)
            for enemy in reversed(dead_enemies):
                enemy.remove_from_sprite_lists()
        for bullet in reversed(dead_bullets):
            bullet.remove_from_sprite_lists()
        # check for player and powerup collisions
        powerup_collisions = arcade.check_for_collision_with_list(self.player, self.powerup_list)
        for powerup in powerup_collisions:
            self.trigger_powerup(powerup.type)
            powerup.remove_from_sprite_lists()

    def trigger_powerup(self, type: int):
        if type == shared_vars.PowerupTypes.CHICKEN:
            self.heart.heal(1)
        elif type == shared_vars.PowerupTypes.NUKE:
            dead_enemies = []
            for enemy in self.enemy_list:
                if enemy.sustain_damage(2):
                    self.score += enemy.value
                    dead_enemies.append(enemy)
            for enemy in reversed(dead_enemies):
                enemy.remove_from_sprite_lists()
        elif type == shared_vars.PowerupTypes.DRUMSTICK:
            self.heart.heal(5)

    def update_player_projectile(self):
        if self.space_pressed and len(self.bullet_list) <= self.player_max_bullets and shared_vars.game_timer > self.player_next_fire:
            sprite_image = ASSETS_PATH / "images" / "dumbbell.png"
            bullet = externalsprites.Bullet(file=str(sprite_image), x=self.player.center_x, y=self.player.center_y + 50, health=self.player_damage, height=32, width=32)
            bullet.turn_left(math.pi / 2)
            bullet.change_x = math.cos(bullet.angle) * self.player_bullet_speed
            bullet.change_y = math.sin(bullet.angle) * self.player_bullet_speed
            self.bullet_list.append(bullet)
            self.player_next_fire = shared_vars.game_timer + self.player_fire_cooldown

        for bullet in self.bullet_list:
            bullet.turn_left(2)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.SPACE or key == arcade.key.LSHIFT:
            self.space_pressed = True

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.SPACE or key == arcade.key.LSHIFT:
            self.space_pressed = False

    def on_draw(self):
        """Draw everything"""
        # Start the rendering pass
        arcade.start_render()
        # Draw the player
        self.player.draw()

        self.bullet_list.draw()

        self.enemy_list.draw()

        self.powerup_list.draw()

        self.heart.draw()

        for dmg_indi in reversed(self.damage_indicator_list):
            if shared_vars.game_timer < dmg_indi.display_until:
                if not dmg_indi.is_score:
                    arcade.draw_text(start_x=dmg_indi.x, start_y=dmg_indi.y, text=dmg_indi.text)
                else:
                    arcade.draw_text(start_x=dmg_indi.x + 40, start_y=dmg_indi.y, text=dmg_indi.text, font_size=20, color=(255, 0, 255))
            else:
                self.damage_indicator_list.remove(dmg_indi)

        arcade.draw_text(start_x=50, start_y=40, text=str(self.score).zfill(6))

    def end_game(self):
        exit()

if __name__ == "__main__":
    arcade_game = ArcadeGame(shared_vars.WIDTH, shared_vars.HEIGHT, TITLE)
    arcade_game.setup()
    arcade.run()

# evan final boss?
