import pygame
from pygame import Surface
import random

from code.Player import Player
from code.Enemy import Enemy
from code.HUD import HUD
from code.const import WIN_WIDTH, WIN_HEIGHT, COLOR_YELLOW


class PlayScene:
    def __init__(self, window: Surface):
        self.window = window
        self.background = pygame.transform.scale(pygame.image.load('./assets/fundofase.jpg').convert(),(WIN_WIDTH, WIN_HEIGHT))
        self.background_rect = self.background.get_rect(left=0, top=0)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()

        self.enemy_spawn_cooldown = 500
        self.last_enemy_spawn_time = 0
        self.player_spawn_safe_radius = 100

        self.enemies_killed = 0

        self.wave_message_font = pygame.font.SysFont("dejavusansmono", 70, bold=True)
        self.display_message = ""
        self.message_end_time = 0

        groups = {'all': self.all_sprites, 'arrows': self.arrows}
        self.player = Player(position=(WIN_WIDTH / 2, 500), groups=groups)
        self.all_sprites.add(self.player)
        self.hud = HUD(self.player)

        self.wave_number = 0
        self.wave_in_progress = False
        self.enemies_to_spawn_this_wave = 0
        self.enemy_strength_multiplier = 1.0

        self.next_wave_delay = 5000
        self.next_wave_start_time = pygame.time.get_ticks()

        self.enemy_spawn_cooldown = 500
        self.last_enemy_spawn_time = 0

    def handle_events(self, events):
        self.player.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'MENU'
        return None

    def start_next_wave(self):
        self.wave_in_progress = True
        self.wave_number += 1
        print(f"Iniciando Horda número {self.wave_number}!")
        self.enemy_strength_multiplier *= 1.1
        self.enemies_to_spawn_this_wave = 3 + self.wave_number

    def spawn_enemy(self):
            enemy_types = ['normal', 'fast', 'tank']
            enemy_weights = [0.60, 0.25, 0.15]

            chosen_type = random.choices(enemy_types, weights=enemy_weights, k=1)[0]

            while True:
                side = random.randint(0, 3)

                if side == 0:
                    pos = (random.randint(0, 900), -50)
                elif side == 1:
                    pos = (800 + 50, random.randint(0, 500))
                elif side == 2:
                    pos = (random.randint(0, 950), 450 + 50)
                else:
                    pos = (-50, random.randint(0, 400))

                spawn_pos_vec = pygame.math.Vector2(pos)
                player_pos_vec = self.player.position

                distance = spawn_pos_vec.distance_to(player_pos_vec)

                if distance > self.player_spawn_safe_radius:
                    break

            new_enemy = Enemy(position=pos,
                              player=self.player,
                              enemies_group=self.enemies,
                              enemy_type=chosen_type,
                              strength_multiplier=self.enemy_strength_multiplier)

            self.all_sprites.add(new_enemy)
            self.enemies.add(new_enemy)

    def update(self):
        now = pygame.time.get_ticks()

        if not self.wave_in_progress and len(self.enemies) == 0:
            if now >= self.next_wave_start_time:
                self.start_next_wave()

        if self.wave_in_progress and self.enemies_to_spawn_this_wave > 0:
            if now - self.last_enemy_spawn_time > self.enemy_spawn_cooldown:
                self.last_enemy_spawn_time = now
                self.spawn_enemy()
                self.enemies_to_spawn_this_wave -= 1

        elif self.wave_in_progress and len(self.enemies) == 0:
            self.wave_in_progress = False
            self.next_wave_start_time = now + self.next_wave_delay
            self.display_message = f"HORDE {self.wave_number} COMPLETED!"
            self.message_end_time = now + 3000
            print("Horda derrotada! Próxima horda em 5 segundos...")

        self.all_sprites.update()

        enemies_list = self.enemies.sprites()
        for i, enemy1 in enumerate(enemies_list):
            for j in range(i + 1, len(enemies_list)):
                enemy2 = enemies_list[j]

                distance_vec = enemy1.position - enemy2.position
                distance = distance_vec.length()

                total_radius = enemy1.radius + enemy2.radius
                if distance < total_radius:
                    overlap = total_radius - distance

                    if distance_vec.length() == 0:
                        distance_vec = pygame.math.Vector2(1, 0)

                    push_vec = distance_vec.normalize()

                    enemy1.position += push_vec * (overlap / 2)
                    enemy2.position -= push_vec * (overlap / 2)

                    enemy1.rect.center = enemy1.position
                    enemy2.rect.center = enemy2.position

        hits = pygame.sprite.groupcollide(self.arrows, self.enemies, True, False)
        for arrow, enemy_list in hits.items():
            for enemy in enemy_list:
                was_killed = enemy.take_damage(arrow.damage)
                if was_killed:
                    self.player.xp += enemy.xp_drop
                    print(f"Inimigo derrotado! +{enemy.xp_drop} XP.")

                    if self.player.xp >= self.player.xp_to_next_level:
                        self.player.level_up()

                    self.enemies_killed += 1

        if not self.player.alive():
            return 'GAME_OVER'

    def draw(self, screen: Surface):
            screen.blit(self.background, self.background_rect)
            self.all_sprites.draw(screen)

            self.hud.draw(screen, self.wave_number)
            if pygame.time.get_ticks() < self.message_end_time:
                text_surf = self.wave_message_font.render(self.display_message, True, COLOR_YELLOW)
                text_rect = text_surf.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
                screen.blit(text_surf, text_rect)

            self.hud.draw(screen, self.wave_number)