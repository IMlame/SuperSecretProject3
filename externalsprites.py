import math

import arcade
from arcade import SpriteList, Sprite

import constants
import powerups
import spritescaler

POWERUP_TYPES = constants.PowerupTypes

class Enemy(arcade.Sprite):
    def __init__(self, x: float, y: float, base_health: int, damage: int, is_projectile: bool, width: int, height: int,
                 value: int,
                 file: str, enemy_list: SpriteList, player: Sprite, powerup_list: SpriteList, despawn_time: float = -1):
        super().__init__(center_x=x, center_y=y)
        self.texture = spritescaler.scale(file, width, height)
        self.health = base_health
        self.damage = damage
        self.player = player
        self.enemy_list = enemy_list
        self.is_projectile = is_projectile
        self.value = value
        self.despawn_time = despawn_time
        self.powerup_list = powerup_list
        # damage animation
        self.time_passed = 0
        self.is_red = False
        self.stop_red = 0

    def sustain_damage(self, damage_amount: int) -> bool:
        self.health -= damage_amount
        # flash red
        self.color = (255, 0, 255)
        self.is_red = True
        self.stop_red = self.time_passed + 0.25
        if self.health <= 0:
            self.death_event()
            return True
        return False

    # for enemies that attack
    def attack(self, projectile_list: SpriteList, delta_time: float):
        return

    # for special enemies
    def death_event(self):
        return

    def on_update(self, delta_time: float = 1 / 60):
        self.time_passed += delta_time
        if self.is_red and self.time_passed > self.stop_red:
            self.is_red = False
            self.color = (255, 255, 255)

        if self.despawn_time != -1 and self.time_passed > self.despawn_time:
            self.death_event()
            self.remove_from_sprite_lists()


class BasicProjectile(Enemy):
    def __init__(self, x: float, y: float, base_health: int, damage: int, velocity: int, angle: float, width: int,
                 height: int, value: int, file: str, enemy_list: SpriteList, player: Sprite, powerup_list: SpriteList,
                 despawn_time: int = -1):
        super().__init__(file=file, x=x, y=y, base_health=base_health, damage=damage, is_projectile=True, width=width,
                         height=height, enemy_list=enemy_list, value=value, player=player, despawn_time=despawn_time,
                         powerup_list=powerup_list)
        self.health = base_health
        self.angle = angle
        self.change_x = math.cos(self.angle) * velocity
        self.change_y = math.sin(self.angle) * velocity

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 2


class Peapod(Enemy):
    def __init__(self, x: float, y: float, base_health: int, damage: int, velocity: int, angle: float, width: int,
                 height: int, move_time: float, value: int, file: str, enemy_list: SpriteList, player: Sprite,
                 powerup_list: SpriteList, despawn_time: int = -1):
        super().__init__(file=file, x=x, y=y, base_health=base_health, damage=damage, is_projectile=False, width=width,
                         height=height, enemy_list=enemy_list, value=value, player=player, despawn_time=despawn_time,
                         powerup_list=powerup_list)
        self.health = base_health
        self.angle = angle
        self.change_x = math.cos(self.angle) * velocity
        self.change_y = math.sin(self.angle) * velocity
        self.stop_moving = move_time

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)
        if self.time_passed < self.stop_moving:
            self.center_x += self.change_x
            self.center_y += self.change_y

    def death_event(self):
        for i in range(-1, 2):
            self.enemy_list.append(
                BasicProjectile(file="assets/images/pea.png", x=self.center_x - i * 5, y=self.center_y, base_health=1,
                                damage=1,
                                width=32,
                                height=32, angle=3 / 2 * math.pi - (0.3 * i), velocity=2, enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))


class Catgirl(Enemy):
    def __init__(self, x: float, y: float, base_health: int, damage: int, downwards_velocity: float, track_speed: float,
                 width: int,
                 height: int, value: int, file: str, enemy_list: SpriteList, player: Sprite, powerup_list: SpriteList,
                 despawn_time: int = -1):
        super().__init__(file=file, x=x, y=y, base_health=base_health, damage=damage, is_projectile=False, width=width,
                         height=height, enemy_list=enemy_list, value=value, player=player, despawn_time=despawn_time,
                         powerup_list=powerup_list)
        self.append_texture(spritescaler.scale("assets/images/catgirl1.png", width, height))
        self.append_texture(spritescaler.scale("assets/images/catgirl2.png", width, height))
        self.set_texture(0)
        self.texture_num = 0
        self.health = base_health
        self.change_y = downwards_velocity
        self.track_speed = track_speed

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)
        self.center_x += self.track_speed * (self.player.center_x - self.center_x)
        if (self.player.center_x - self.center_x) > 0 and self.texture_num != 1:
            self.set_texture(1)
            self.texture_num = 1
        elif (self.player.center_x - self.center_x) < 0 and self.texture_num != 0:
            self.set_texture(0)
            self.texture_num = 0
        self.center_y -= self.change_y

    def death_event(self):
        # self.powerup_list.append(powerups.Powerup(self.center_x, self.center_y, 64, 64,
        #                                           file="assets/images/nuke.png", powerup_length=10, type=POWERUP_TYPES.NUKE))
        return

class Shapiro(Enemy):
    def __init__(self, x: float, y: float, base_health: int, damage: int, velocity: int, width: int,
                 height: int, move_time: float, value: int, file: str, enemy_list: SpriteList, player: Sprite,
                 powerup_list: SpriteList, despawn_time: int = -1):
        super().__init__(file=file, x=x, y=y, base_health=base_health, damage=damage, is_projectile=False, width=width,
                         height=height, enemy_list=enemy_list, value=value, player=player, despawn_time=despawn_time,
                         powerup_list=powerup_list)
        self.health = base_health
        self.stop_moving = move_time
        self.change_y = velocity
        self.next_attack = 0
        self.attack_delay = 3

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)
        if self.time_passed < self.stop_moving:
            self.center_y -= self.change_y
        if self.time_passed > self.next_attack:
            self.enemy_list.append(
                BasicProjectile(file="assets/images/facts.png", x=self.center_x, y=self.center_y, base_health=1,
                                damage=1,
                                width=96,
                                height=96, angle=3 / 2 * math.pi - (0.15 * ((self.next_attack % 2) + 1)), velocity=2,
                                enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))
            self.enemy_list.append(
                BasicProjectile(file="assets/images/logic.png", x=self.center_x, y=self.center_y, base_health=1,
                                damage=1,
                                width=96,
                                height=96, angle=3 / 2 * math.pi + (0.15 * ((self.next_attack % 2) + 1)), velocity=2,
                                enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))
            self.enemy_list.append(
                BasicProjectile(file="assets/images/hypothetically.png", x=self.center_x, y=self.center_y,
                                base_health=1,
                                damage=1,
                                width=128,
                                height=128, angle=3 / 2 * math.pi, velocity=2, enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))
            self.next_attack = self.time_passed + self.attack_delay

    def death_event(self):
        for i in range(-4, 0):
            self.enemy_list.append(
                BasicProjectile(file="assets/images/facts.png", x=self.center_x - i * 5, y=self.center_y, base_health=1,
                                damage=1,
                                width=64,
                                height=64, angle=3 / 2 * math.pi - (0.3 * i), velocity=2, enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))
        for i in range(0, 4):
            self.enemy_list.append(
                BasicProjectile(file="assets/images/logic.png", x=self.center_x - i * 5, y=self.center_y, base_health=1,
                                damage=1,
                                width=64,
                                height=64, angle=3 / 2 * math.pi - (0.3 * i), velocity=2, enemy_list=self.enemy_list,
                                value=1, player=self.player, powerup_list=self.powerup_list))


class Player(arcade.Sprite):
    def __init__(self, x: float, y: float, file: str, width: int, height: int):
        super().__init__(center_x=x, center_y=y)
        self.texture = spritescaler.scale(file, width, height)

class Bullet(arcade.Sprite):
    def __init__(self, x: float, y: float, file: str, width: int, height: int, health: int):
        super().__init__(center_x=x, center_y=y)
        self.texture = spritescaler.scale(file, width, height)
        self.health = health

    def sustain_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

class Heart(arcade.Sprite):
    def __init__(self, x: float, y: float, initial_health: int, height: int, width: int):
        super().__init__(center_x=x, center_y=y)
        self.initial_health = initial_health
        self.health = initial_health
        for i in range(0, 6):
            texture_name = "assets/images/hearts/" + str(i) + "heart.png"
            self.append_texture(spritescaler.scale(texture_name, height=height, width=width))
        self.set_texture(5)

    def damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.set_texture(0)
        else:
            self.set_texture(int(5 * (self.health / self.initial_health)))

        return self.health <= 0

    def health(self, amount: int):
        self.health = min(self.health + amount, self.initial_health)
