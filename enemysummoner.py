import math
import random

from arcade import SpriteList, Sprite

import shared_vars

import externalsprites

HEIGHT = shared_vars.HEIGHT
WIDTH = shared_vars.WIDTH

class EnemySummoner:
    def __init__(self, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, width: int, height: int):
        self.enemy_list = enemy_list
        self.powerup_list = powerup_list
        self.damage_indicator_list = damage_indicator_list
        self.player = player
        self.spawner_list = []
        self.width = width
        self.height = height
        self.elapsed_time = 0
        self.stage = 0

    def summon_enemies(self, delta_time: float):
        self.elapsed_time += delta_time
        if self.elapsed_time // 1 > self.stage:
            self.stage += 1
            self.stage_update()
        for spawner in self.spawner_list:
            spawner.attempt_spawn(delta_time=delta_time, enemy_list=self.enemy_list)

    def stage_update(self):
        # if self.stage == 1:
        #     self.create_broccoli_spawner(5, 8, despawn_time=15)
        #     self.create_peapod_spawner(10, 15, despawn_time=60)
        #     self.create_catgirl_spawner(4, 5, track_speed=0.005, despawn_time=15)
        #     self.create_shapiro_spawner(4, 5, despawn_time=60)
        if self.stage == 1:
            self.create_broccoli_spawner(5, 8, despawn_time=15)
        if self.stage == 10:
            self.create_broccoli_spawner(3, 5, despawn_time=15)
        if self.stage == 15:
            self.create_broccoli_spawner(1, 3, despawn_time=15)
        if self.stage == 30:
            self.create_peapod_spawner(10, 15, despawn_time=60)
        if self.stage == 60:
            self.create_broccoli_spawner(1, 3, despawn_time=15)
            self.create_broccoli_spawner(1, 3, despawn_time=15)
            self.create_broccoli_spawner(1, 3, despawn_time=15)
            self.create_peapod_spawner(15, 20, despawn_time=60)
            self.create_broccoli_spawner(1, 3, despawn_time=15)
            self.create_peapod_spawner(15, 20, despawn_time=60)
        if self.stage == 120:
            self.spawner_list.clear()
            self.create_catgirl_spawner(4, 5, track_speed=0.005, despawn_time=15)
        if self.stage == 125:
            self.spawner_list.clear()
        if self.stage == 130:
            shared_vars.enemy_health_add += 1
            for i in range(8):
                self.create_broccoli_spawner(1, 5, despawn_time=15)
        if self.stage == 145:
            shared_vars.enemy_spawn_delay_percentage += 0.3
        if self.stage == 155:
            shared_vars.enemy_spawn_delay_percentage += 0.3
        if self.stage == 170:
            shared_vars.enemy_spawn_delay_percentage -= 0.5
            self.create_catgirl_spawner(8, 10, track_speed=0.005, despawn_time=15)
            self.create_catgirl_spawner(8, 15, track_speed=0.005, despawn_time=15)
        if self.stage == 200:
            self.create_peapod_spawner(15, 20, despawn_time=60)
            self.create_peapod_spawner(15, 20, despawn_time=60)
        if self.stage == 240:
            self.spawner_list.clear()
        if self.stage == 250:
            self.create_shapiro_spawner(4, 5, despawn_time=60)
        if self.stage == 256:
            self.spawner_list.clear()
            shared_vars.enemy_velocity_increase += 3
        if self.stage == 275:
            for i in range(4):
                self.create_catgirl_spawner(8, 10, track_speed=0.005, despawn_time=15)
                self.create_catgirl_spawner(8, 15, track_speed=0.005, despawn_time=15)
            self.create_broccoli_spawner(1, 7, despawn_time=5)
        # if self.stage == 12:
        #         #
        #         #     self.create_broccoli_spawner(2, 4)
        #         # if self.stage == 24:
        #         #     self.create_broccoli_spawner(0, 2)
        #         #     self.create_broccoli_spawner(0, 2)
        #         # if self.stage == 36:
        #         #     self.create_peapod_spawner(7, 8)
        #         #     self.spawner_list.pop()

    def create_broccoli_spawner(self, spawn_min: int, spawn_max: int, despawn_time: int):
        self.spawner_list.append(
            BroccoliSpawner(file="assets/images/broccoli.png", base_health=1, damage=1, is_projectile=True, width=64,
                            height=64,
                            spawn_min=spawn_min, spawn_max=spawn_max, y_min=HEIGHT - 20, y_max=HEIGHT - 19,
                            enemy_list=self.enemy_list, value=1, player=self.player, powerup_list=self.powerup_list, despawn_time=despawn_time, damage_indicator_list=self.damage_indicator_list))

    def create_peapod_spawner(self, spawn_min: int, spawn_max: int, despawn_time: int):
        self.spawner_list.append(
            PeapodSpawner(file="assets/images/peapod.png", base_health=5, damage=3, is_projectile=False, width=100,
                          height=100,
                          spawn_min=spawn_min, spawn_max=spawn_max, y_min=HEIGHT + 50, y_max=HEIGHT + 51, x_min=100,
                          x_max=700, enemy_list=self.enemy_list, value=10, player=self.player, powerup_list=self.powerup_list, despawn_time=despawn_time, damage_indicator_list=self.damage_indicator_list))

    def create_catgirl_spawner(self, spawn_min: int, spawn_max: int, track_speed: float, despawn_time: int):
        self.spawner_list.append(
            CatgirlSpawner(file="assets/images/catgirl1.png", base_health=6, damage=2, is_projectile=False, width=100,
                           height=100,
                           spawn_min=spawn_min, spawn_max=spawn_max, y_min=HEIGHT, y_max=HEIGHT + 1, x_min=100,
                           x_max=700, enemy_list=self.enemy_list, value=10, player=self.player,
                           track_speed=track_speed, powerup_list=self.powerup_list, despawn_time=despawn_time, damage_indicator_list=self.damage_indicator_list))

    def create_shapiro_spawner(self, spawn_min: int, spawn_max: int, despawn_time: int):
        self.spawner_list.append(
            ShapiroSpawner(file="assets/images/shapiro.png", base_health=30, damage=1, is_projectile=False, width=256,
                           height=256,
                           spawn_min=spawn_min, spawn_max=spawn_max, y_min=HEIGHT + 80, y_max=HEIGHT + 81, x_min=100,
                           x_max=700, enemy_list=self.enemy_list, value=100, player=self.player, powerup_list=
                           self.powerup_list, despawn_time=despawn_time, damage_indicator_list=self.damage_indicator_list))


class EnemySpawner:
    def __init__(self, file: str, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, base_health: int, damage: int,
                 is_projectile: bool,
                 value: int,
                 width: int, height: int,
                 spawn_min: int, spawn_max: int, x_min=20, x_max=WIDTH - 20, y_min=HEIGHT - 300, y_max=HEIGHT - 20, despawn_time: int = -1):
        self.file = file
        self.player = player
        self.enemy_list = enemy_list
        self.powerup_list = powerup_list
        self.damage_indicator_list = damage_indicator_list
        self.despawn_time = despawn_time
        self.base_health = base_health
        self.damage = damage
        self.is_projectile = is_projectile
        self.value = value
        self.width = width
        self.height = height
        self.spawn_min = spawn_min
        self.spawn_max = spawn_max
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.spawn_time = random.uniform(self.spawn_min, self.spawn_max)
        self.time_elapsed = 0

    def attempt_spawn(self, delta_time: float, enemy_list: SpriteList):
        self.time_elapsed += delta_time
        if self.time_elapsed > self.spawn_time:
            self.time_elapsed = 0
            self.spawn_time = random.randint(self.spawn_min, self.spawn_max) * (1 - shared_vars.enemy_spawn_delay_percentage)
            self.spawn(enemy_list)

    # override
    def spawn(self, enemy_list: SpriteList):
        return

    # random xy
    def get_xy(self) -> (int, int):
        gen = random
        x = gen.randint(self.x_min, self.x_max)
        y = gen.randint(self.y_min, self.y_max)
        return x, y


class BroccoliSpawner(EnemySpawner):
    def __init__(self, file: str, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, base_health: int, damage: int,
                 is_projectile: bool,
                 value: int,
                 width: int, height: int,
                 spawn_min: int, spawn_max: int, x_min=20, x_max=WIDTH - 20, y_min=HEIGHT - 300, y_max=HEIGHT - 20, despawn_time: int = -1):
        super().__init__(file=file, enemy_list=enemy_list, damage_indicator_list=damage_indicator_list, base_health=base_health, damage=damage,
                         is_projectile=is_projectile, value=value, width=width, height=height, spawn_min=spawn_min,
                         spawn_max=spawn_max,
                         x_min=x_min, x_max=x_max,
                         y_min=y_min, y_max=y_max, player=player, powerup_list=powerup_list, despawn_time=despawn_time)

    def spawn(self, enemy_list: SpriteList):
        x, y = self.get_xy()
        angle_offset = random.uniform(-1 / 4 * math.pi, 1 / 4 * math.pi)
        velocity = random.randint(1, 5)
        enemy = externalsprites.BasicProjectile(x=x, y=y, damage=self.damage, velocity=velocity,
                                                base_health=self.base_health,
                                                angle=3 * math.pi / 2 + angle_offset, file=self.file, width=self.width,
                                                height=self.height, enemy_list=self.enemy_list, value=self.value,
                                                player=self.player, powerup_list=self.powerup_list, despawn_time=self.despawn_time, damage_indicator_list=self.damage_indicator_list)
        enemy_list.append(enemy)


class PeapodSpawner(EnemySpawner):
    def __init__(self, file: str, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, base_health: int, damage: int,
                 is_projectile: bool,
                 value: int,
                 width: int, height: int,
                 spawn_min: int, spawn_max: int, x_min=20, x_max=WIDTH - 20, y_min=HEIGHT - 300, y_max=HEIGHT - 20, despawn_time: int = -1):
        super().__init__(file=file, enemy_list=enemy_list, damage_indicator_list=damage_indicator_list, base_health=base_health, damage=damage,
                         is_projectile=is_projectile, value=value, width=width, height=height, spawn_min=spawn_min,
                         spawn_max=spawn_max,
                         x_min=x_min, x_max=x_max,
                         y_min=y_min, y_max=y_max, player=player, powerup_list=powerup_list, despawn_time=despawn_time)

    def spawn(self, enemy_list: SpriteList):
        x, y = self.get_xy()
        angle_offset = random.uniform(-1 / 10 * math.pi, 1 / 10 * math.pi)
        velocity = random.randint(5, 7)
        enemy = externalsprites.Peapod(x=x, y=y, damage=self.damage, velocity=velocity,
                                       base_health=self.base_health,
                                       angle=3 * math.pi / 2 + angle_offset, file=self.file, width=self.width,
                                       height=self.height, enemy_list=self.enemy_list, move_time=0.9, value=self.value,
                                       player=self.player, powerup_list=self.powerup_list, despawn_time=self.despawn_time, damage_indicator_list=self.damage_indicator_list)
        enemy_list.append(enemy)


class CatgirlSpawner(EnemySpawner):
    def __init__(self, file: str, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, base_health: int, damage: int,
                 is_projectile: bool,
                 value: int,
                 width: int, height: int,
                 spawn_min: int, spawn_max: int, track_speed: float, x_min=20, x_max=WIDTH - 20, y_min=HEIGHT - 300,
                 y_max=HEIGHT - 20, despawn_time: int = -1):
        super().__init__(file=file, enemy_list=enemy_list, damage_indicator_list=damage_indicator_list, base_health=base_health, damage=damage,
                         is_projectile=is_projectile, value=value, width=width, height=height, spawn_min=spawn_min,
                         spawn_max=spawn_max,
                         x_min=x_min, x_max=x_max,
                         y_min=y_min, y_max=y_max, player=player, powerup_list=powerup_list, despawn_time=despawn_time)
        self.track_speed = track_speed

    def spawn(self, enemy_list: SpriteList):
        x, y = self.get_xy()
        downwards_velocity = random.uniform(0.4, 0.9)
        enemy = externalsprites.Catgirl(x=x, y=y, damage=self.damage, downwards_velocity=downwards_velocity,
                                        base_health=self.base_health,
                                        file=self.file, width=self.width,
                                        height=self.height, enemy_list=self.enemy_list, value=self.value,
                                        player=self.player, track_speed=self.track_speed, powerup_list=self.powerup_list, despawn_time=self.despawn_time, damage_indicator_list=self.damage_indicator_list)
        enemy_list.append(enemy)


class ShapiroSpawner(EnemySpawner):
    def __init__(self, file: str, enemy_list: SpriteList, powerup_list: SpriteList, player: Sprite, damage_indicator_list: list, base_health: int, damage: int,
                 is_projectile: bool,
                 value: int,
                 width: int, height: int,
                 spawn_min: int, spawn_max: int, x_min=20, x_max=WIDTH - 20, y_min=HEIGHT - 300, y_max=HEIGHT - 20, despawn_time: int = -1):
        super().__init__(file=file, enemy_list=enemy_list, damage_indicator_list=damage_indicator_list, base_health=base_health, damage=damage,
                         is_projectile=is_projectile, value=value, width=width, height=height, spawn_min=spawn_min,
                         spawn_max=spawn_max,
                         x_min=x_min, x_max=x_max,
                         y_min=y_min, y_max=y_max, player=player, powerup_list=powerup_list, despawn_time=despawn_time)

    def spawn(self, enemy_list: SpriteList):
        x, y = self.get_xy()
        velocity = random.randint(1, 2)
        enemy = externalsprites.Shapiro(x=x, y=y, damage=self.damage, velocity=velocity,
                                        base_health=self.base_health,
                                        file=self.file, width=self.width,
                                        height=self.height, enemy_list=self.enemy_list, move_time=1.8, value=self.value,
                                        player=self.player, powerup_list=self.powerup_list, despawn_time=self.despawn_time, damage_indicator_list=self.damage_indicator_list)
        enemy_list.append(enemy)
