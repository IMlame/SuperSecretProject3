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
import os
import sys

import arcade
import arcade.gui

# To locate your assets
from pathlib import Path

import shared_vars
import enemysummoner
import externalsprites
import spritescaler
from externalsprites import Player

# Set the game window title
TITLE = "Jordan VS the World"

# Location of your assets
ASSETS_PATH = Path.cwd() / "assets"

BUTTON_STYLE = {"bg_color": (255, 192, 203), "border_color": None,
                                                         "font_size": 20, "font_name" : "Kongtext", "border_width" : 3}
BUTTON_WIDTH = 300

APPLICATION_PATH = "" if "venv/bin" in os.path.dirname(sys.executable) else os.path.dirname(sys.executable) + "/"
arcade.load_font(APPLICATION_PATH + "kongtext.ttf")
# Classes
class GameView(arcade.View):
    """The Arcade Game class"""
    def __init__(self):
        """Create the main game window

        Arguments:
            width {float} -- Width of the game window
            height {float} -- Height of the game window
            title {str} -- Title for the game window
        """

        # Call the super class init method
        super().__init__()
        # reset args
        shared_vars.game_timer = 0
        shared_vars.stage = 1
        shared_vars.score = 0
        shared_vars.won = False

        shared_vars.enemy_health_multiplier = 1
        shared_vars.enemy_health_add = 0
        shared_vars.enemy_velocity_increase = 1
        shared_vars.enemy_spawn_delay_percentage = 0

        # Set control list
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False

        # Player
        self.player = None
        # Player constant modifiers
        self.player_has_robe = False
        # will be increased to time + 0.15 every time bullet is fired
        self.player_arms_down = 0
        # will be increased to time + 15 when robe powerup collected
        self.player_robe_until = 0
        # red until
        self.player_colored_until = 0
        self.player_bullet_speed = 5
        self.player_move_speed = 10
        self.player_jump_velocity = 15
        self.player_gravity = 1
        self.initial_health = 8
        self.player_damage = 1
        self.player_dumbbell_size = 1
        self.player_fire_cooldown = 0.2
        self.player_max_bullets = 3
        self.robe_multiplier = 1
        self.player_combo = 0
        self.player_max_health = 8

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

        if shared_vars.difficulty == shared_vars.Difficulty.IMPOSSIBLE:
            shared_vars.enemy_rate_multiplier = 2
            shared_vars.enemy_health_add = 2
            shared_vars.enemy_velocity_increase = 2
            shared_vars.enemy_spawn_delay_percentage = 0.4
            self.player_max_health = 1

    def on_show(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(color=arcade.color.PINK)

        # Set up the player
        sprite_image = ASSETS_PATH / "images" / "jordan.png"
        self.player = Player(
            file=str(sprite_image), x=shared_vars.WIDTH // 2, y=shared_vars.FLOOR_HEIGHT,
            height=shared_vars.PLAYER_HEIGHT, width=shared_vars.PLAYER_WIDTH)
        self.player.append_texture(
            texture=spritescaler.scale("assets/images/jordan.png", shared_vars.PLAYER_WIDTH, shared_vars.PLAYER_HEIGHT))
        self.player.append_texture(
            texture=spritescaler.scale("assets/images/jordanup.png", shared_vars.PLAYER_WIDTH,
                                       shared_vars.PLAYER_HEIGHT))
        self.player.append_texture(
            texture=spritescaler.scale("assets/images/jordanrobe.png", shared_vars.PLAYER_WIDTH,
                                       shared_vars.PLAYER_HEIGHT))
        self.player.append_texture(
            texture=spritescaler.scale("assets/images/jordanrobeup.png", shared_vars.PLAYER_WIDTH,
                                       shared_vars.PLAYER_HEIGHT))
        self.player.set_texture(0)

        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.damage_indicator_list = []

        self.heart = externalsprites.Heart(x=750, y=shared_vars.HEIGHT - 50, initial_health=self.player_max_health,
                                           width=100, height=100)

        self.enemy_spawner = enemysummoner.EnemySummoner(enemy_list=self.enemy_list, width=shared_vars.WIDTH,
                                                         height=shared_vars.HEIGHT, player=self.player,
                                                         powerup_list=self.powerup_list,
                                                         damage_indicator_list=self.damage_indicator_list)

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
        # player animation state
        self.player_img_update()

        if shared_vars.DIFFICULTY_LENGTH[shared_vars.difficulty.value] - shared_vars.game_timer < 0:
            shared_vars.won = True
            self.end_game()

    def player_img_update(self):
        # robe
        cur_num = self.player.cur_texture_index
        if self.player_has_robe:
            if (shared_vars.game_timer < self.player_arms_down) and cur_num != 3:
                self.player.cur_texture_index = 3
                self.player.set_texture(3)
            elif shared_vars.game_timer >= self.player_arms_down and cur_num != 2:
                self.player.cur_texture_index = 2
                self.player.set_texture(2)
        else:
            if shared_vars.game_timer < self.player_arms_down and cur_num != 1:
                self.player.cur_texture_index = 1
                self.player.set_texture(1)
            elif shared_vars.game_timer >= self.player_arms_down and cur_num != 0:
                self.player.cur_texture_index = 0
                self.player.set_texture(0)

        if self.player_has_robe:
            time_left = self.player_robe_until - shared_vars.game_timer
            blink_color = (30, 255, 255)
            normal_color = (255, 255, 255)
            if time_left < 5:
                dec = time_left % 1
                if dec < 0.25:
                    self.player.color = normal_color
                elif 0.25 <= dec < 0.5:
                    self.player.color = blink_color
                elif 0.5 <= dec < 0.75:
                    self.player.color = normal_color
                else:
                    self.player.color = blink_color
            if time_left < 0:
                self.player.color = (255, 255, 255)
                self.player_has_robe = False
                self.robe_multiplier = 1
        # red animation
        if (shared_vars.game_timer >= self.player_robe_until) and self.player.color != (255, 255, 255):
            print("reset color")
            self.player.color = (255, 255, 255)


    def remove_old_projectiles(self):
        for bullet in self.bullet_list:
            if bullet.bottom > shared_vars.HEIGHT or bullet.top < 0 or bullet.right < 0 or bullet.left > shared_vars.WIDTH:
                bullet.remove_from_sprite_lists()
                # combo breaks if player doesn't have robe (with 3 second grace period)
                if not bullet.hit_something() and not self.player_has_robe and shared_vars.game_timer - self.player_robe_until > 3:
                    self.player_combo = 0

        for projectile in self.enemy_list:
            if projectile.is_projectile and projectile.bottom > shared_vars.HEIGHT or projectile.top < 0 or projectile.right < 0 or projectile.left > shared_vars.WIDTH:
                projectile.remove_from_sprite_lists()

    def update_movement(self):
        fast_fall_multiplier = 1
        # movement
        if self.left_pressed:
            if self.player.center_x + -self.player_move_speed < 0:
                self.player.center_x = 0
            else:
                self.player.center_x += -self.player_move_speed * self.robe_multiplier
        if self.right_pressed:
            if self.player.center_x + self.player_move_speed > shared_vars.WIDTH:
                self.player.center_x = shared_vars.WIDTH
            else:
                self.player.center_x += self.player_move_speed * self.robe_multiplier
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
            if not self.player_has_robe and self.heart.damage(enemy.damage):
                self.end_game()
            self.player_colored_until = shared_vars.game_timer + 0.2
            self.player.color = (255, 0, 255)
            self.player_combo = 0
            enemy.remove_from_sprite_lists()
        # destroy shot enemies
        dead_bullets = []
        for bullet in self.bullet_list:
            enemies_shot = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            dead_enemies = []
            for enemy in enemies_shot:
                if not self.player_has_robe:
                    self.player_combo += 1
                    if self.player_combo == 25:
                        # BOMB, CHICKEN, DRUMSTICK, DUMBBELL, ROBE
                        odds = [15, 15, 0, 15, 5]
                        externalsprites.random_powerup_drop(x=400, y=800, width=64, height=64,powerup_length=8,drop_odds=100, odds=odds, powerup_list=self.powerup_list)
                    elif self.player_combo % 100 == 0:
                        # BOMB, CHICKEN, DRUMSTICK, DUMBBELL, ROBE
                        odds = [20, 0, 0, 20, 60]
                        externalsprites.random_powerup_drop(x=400, y=800, width=64, height=64, powerup_length=8,
                                                            drop_odds=100, odds=odds, powerup_list=self.powerup_list)
                    elif self.player_combo % 50 == 0:
                        # BOMB, CHICKEN, DRUMSTICK, DUMBBELL, ROBE
                        odds = [30, 0, 0, 30, 20]
                        externalsprites.random_powerup_drop(x=400, y=800, width=64, height=64,powerup_length=8,drop_odds=100, odds=odds, powerup_list=self.powerup_list)


                enemy_health = enemy.health
                if enemy.sustain_damage(bullet.health):
                    shared_vars.score += enemy.value
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
            self.heart.heal(8)
            self.player_colored_until = shared_vars.game_timer + 0.2
            self.player.color = (0, 255, 0)
        elif type == shared_vars.PowerupTypes.BOMB:
            dead_enemies = []
            for enemy in self.enemy_list:
                if enemy.sustain_damage(2 * shared_vars.enemy_health_add * shared_vars.enemy_health_multiplier):
                    shared_vars.score += enemy.value
                    self.player_combo += 1
                    dead_enemies.append(enemy)
            for enemy in reversed(dead_enemies):
                enemy.remove_from_sprite_lists()
        elif type == shared_vars.PowerupTypes.DRUMSTICK:
            self.heart.heal(2)
            self.player_colored_until = shared_vars.game_timer + 0.2
            self.player.color = (0, 255, 0)
        elif type == shared_vars.PowerupTypes.DUMBBELL:
            self.player_damage += 1
            self.player_dumbbell_size += .5
        elif type == shared_vars.PowerupTypes.ROBE:
            self.heart.heal(8)
            self.player_has_robe = True
            self.player.color = (30, 255, 255)
            self.player_robe_until = max(self.player_robe_until, shared_vars.game_timer + 10)
            if self.robe_multiplier < 2:
                self.robe_multiplier += 1

    def update_player_projectile(self):
        if self.space_pressed and len(
                self.bullet_list) <= self.player_max_bullets * self.robe_multiplier and shared_vars.game_timer > self.player_next_fire:
            self.player_arms_down = shared_vars.game_timer + 0.15
            sprite_image = ASSETS_PATH / "images" / "dumbbell.png"
            capped_combo = min(50, self.player_combo)
            bullet = externalsprites.Bullet(file=str(sprite_image), x=self.player.center_x, y=self.player.center_y + 50,
                                            health=self.player_damage * self.robe_multiplier + int(capped_combo / 10), height=(32 + int(capped_combo / 10) * 10) * self.player_dumbbell_size * self.robe_multiplier,
                                            width=(32 + int(capped_combo / 10) * 10) * self.player_dumbbell_size * self.robe_multiplier)
            bullet.turn_left(math.pi / 2)
            bullet.change_x = math.cos(bullet.angle) * self.player_bullet_speed
            bullet.change_y = math.sin(bullet.angle) * self.player_bullet_speed
            self.bullet_list.append(bullet)
            self.player_next_fire = shared_vars.game_timer + self.player_fire_cooldown / self.robe_multiplier

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
        elif key == arcade.key.ESCAPE:
            home_view = HomeView()
            self.window.show_view(home_view)

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
                    arcade.draw_text(start_x=dmg_indi.x + 40, start_y=dmg_indi.y, text=dmg_indi.text, font_size=20,
                                     color=(255, 0, 255))
            else:
                self.damage_indicator_list.remove(dmg_indi)

        # score
        arcade.draw_text(start_x=50, start_y=40, text=str(shared_vars.score).zfill(6), font_name='Kongtext')
        # time left
        arcade.draw_text(start_x=670, start_y=40, text=str(max(round(shared_vars.DIFFICULTY_LENGTH[shared_vars.difficulty.value] - shared_vars.game_timer, 2), 0)), font_name='Kongtext')
        # combo
        arcade.draw_text(start_x=50, start_y=shared_vars.HEIGHT - 75, text= "Combo: " + str(self.player_combo), font_size=30, font_name='Kongtext')

    def end_game(self):
        end_game_view = GameOverView()
        self.window.show_view(end_game_view)


class GameOverView(arcade.View):
    def __init__(self):
        # Call the super class init method
        super().__init__()

        self.uimanager1 = arcade.gui.UIManager()
        self.uimanager1.enable()

        self.uimanager2 = arcade.gui.UIManager()
        self.uimanager2.enable()

        self.uimanager3 = arcade.gui.UIManager()
        self.uimanager3.enable()

        # Creating Button using UIFlatButton
        restart_button = arcade.gui.UIFlatButton(text="Restart", x=shared_vars.WIDTH / 2, y=shared_vars.HEIGHT / 2,
                                                 style=BUTTON_STYLE, width=BUTTON_WIDTH)
        restart_button.on_click = self.restart

        home_button = arcade.gui.UIFlatButton(text="Home", x=shared_vars.WIDTH / 2, y=shared_vars.HEIGHT / 2,
                                              style=BUTTON_STYLE, width=BUTTON_WIDTH)
        home_button.on_click = self.home

        exit_button = arcade.gui.UIFlatButton(text="Exit", x=shared_vars.WIDTH / 2, y=shared_vars.HEIGHT / 2,
                                              style=BUTTON_STYLE, width=BUTTON_WIDTH)
        exit_button.on_click = self.leave
        # Adding button in our uimanager
        self.uimanager1.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=restart_button,
                align_y=-25)
        )
        self.uimanager2.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=home_button,
                align_y=-75)
        )
        self.uimanager3.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=exit_button,
                align_y=-125)
        )

    def on_draw(self):
        # Start the rendering pass
        arcade.start_render()
        title_string = ""
        if shared_vars.won:
            title_string = "YOU WIN :)"
        else:
            title_string = "GAME OVER :("
        arcade.draw_lrtb_rectangle_outline(left=50,right=750,top=550,bottom=290,border_width=8,color=(255,255,255))
        arcade.draw_text(start_x=0, start_y=shared_vars.HEIGHT / 2 + 150, text=title_string, font_size=40,
                         align='center', width=800, font_name='Kongtext')
        arcade.draw_text(start_x=0, start_y=shared_vars.HEIGHT / 2 + 50, text=str("Score: " + str(shared_vars.score)),
                         font_size=30, align='center', width=800, font_name='Kongtext')
        self.uimanager1.draw()
        self.uimanager2.draw()
        self.uimanager3.draw()

    def on_show(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(color=arcade.color.PINK)

    def restart(self, event):
        game_view = GameView()
        self.window.show_view(game_view)


    def home(self, event):
        home_view = HomeView()
        self.window.show_view(home_view)

    def leave(self, event):
        arcade.close_window()


class HomeView(arcade.View):
    def __init__(self):
        # Call the super class init method
        super().__init__()

        self.uimanager_start = arcade.gui.UIManager()
        self.uimanager_start.enable()

        self.uimanager_difficulty = arcade.gui.UIManager()
        self.uimanager_difficulty.enable()

        self.uimanager_mode = arcade.gui.UIManager()
        self.uimanager_mode.enable()

        self.uimanager_exit = arcade.gui.UIManager()
        self.uimanager_exit.enable()

        # Creating Button using UIFlatButton
        self.start_game = arcade.gui.UIFlatButton(text="Start Game", x=shared_vars.WIDTH / 2, y=shared_vars.HEIGHT / 2,
                                                  style=BUTTON_STYLE, width=BUTTON_WIDTH, height=50)
        self.start_game.on_click = self.start
        self.difficulty_button = arcade.gui.UIFlatButton(
            text=shared_vars.DIFFICULTY_MAP.get(shared_vars.difficulty.value), x=shared_vars.WIDTH / 2,
            y=shared_vars.HEIGHT / 2,
            style=BUTTON_STYLE, width=BUTTON_WIDTH)
        self.difficulty_button.on_click = self.inc
        mode_text = "CLASSIC" if not shared_vars.WACKY else "SICK MODE"
        self.mode_button = arcade.gui.UIFlatButton(
            text=mode_text, x=shared_vars.WIDTH / 2,
            y=shared_vars.HEIGHT / 2,
            style=BUTTON_STYLE, width=BUTTON_WIDTH)
        self.mode_button.on_click = self.mode_switch
        self.exit_button = arcade.gui.UIFlatButton(text="Exit", x=shared_vars.WIDTH / 2, y=shared_vars.HEIGHT / 2,
                                                   style=BUTTON_STYLE, width=BUTTON_WIDTH)
        self.exit_button.on_click = self.leave
        # Adding button in our uimanager
        self.uimanager_start.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.start_game)
        )
        self.uimanager_difficulty.add((
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.difficulty_button,
                align_y=-50
            )
        ))
        self.uimanager_mode.add((
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.mode_button,
                align_y=-100
            )
        ))
        self.uimanager_exit.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.exit_button,
                align_y=-150)
        )

    def on_draw(self):
        # Start the rendering pass
        arcade.start_render()
        arcade.draw_lrtb_rectangle_outline(left=50,right=750,top=550,bottom=300,border_width=8,color=(255,255,255))
        arcade.draw_text(start_x=0, start_y=shared_vars.HEIGHT / 2 + 150, text=str(TITLE), font_size=50,
                         align='center', width=800, font_name='Kongtext')
        self.uimanager_start.draw()
        self.uimanager_difficulty.draw()
        self.uimanager_mode.draw()
        self.uimanager_exit.draw()

    def on_show(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(color=arcade.color.PINK)

    def start(self, event):
        game_view = GameView()
        self.window.show_view(game_view)


    def inc(self, event):
        val = shared_vars.difficulty.value
        if val == shared_vars.MAX_DIFFICULTY_NUM:
            shared_vars.difficulty = shared_vars.Difficulty(0)
        else:
            shared_vars.difficulty = shared_vars.Difficulty(val + 1)
        self.difficulty_button.text = shared_vars.DIFFICULTY_MAP.get(shared_vars.difficulty.value)
        self.uimanager_difficulty.remove(self.difficulty_button)
        self.uimanager_difficulty.add((
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.difficulty_button,
                align_y=-50
            )
        ))

    def mode_switch(self, event):
        shared_vars.WACKY = not shared_vars.WACKY
        self.mode_button.text = "CLASSIC" if not shared_vars.WACKY else "SICK MODE"

    def leave(self, event):
        arcade.close_window()


if __name__ == "__main__":
    window = arcade.Window(shared_vars.WIDTH, shared_vars.HEIGHT, TITLE)
    start_view = HomeView()
    window.show_view(start_view)
    arcade.run()

