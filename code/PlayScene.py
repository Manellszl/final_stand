import pygame
from pygame import Surface
import random  # 1. Importe o módulo random no início do arquivo

from code.Player import Player
from code.Enemy import Enemy
from code.HUD import HUD
from code.const import WIN_WIDTH, WIN_HEIGHT


class PlayScene:
    def __init__(self, window: Surface):
        # O seu método __init__ está correto, não precisa de alterações.
        self.window = window
        self.background = pygame.transform.scale(pygame.image.load('./assets/fundofase.jpg').convert(),
                                                 (WIN_WIDTH, WIN_HEIGHT))
        self.background_rect = self.background.get_rect(left=0, top=0)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()

        self.enemy_spawn_cooldown = 500
        self.last_enemy_spawn_time = 0
        self.player_spawn_safe_radius = 250

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
        # Este método está correto.
        self.player.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'MENU'
        return None

    def start_next_wave(self):
        # Este método está correto.
        self.wave_in_progress = True
        self.wave_number += 1
        print(f"Iniciando Horda número {self.wave_number}!")
        self.enemy_strength_multiplier *= 1.1
        self.enemies_to_spawn_this_wave = 3 + self.wave_number

    # 2. REMOVA A PRIMEIRA DEFINIÇÃO DE SPAWN_ENEMY E DEIXE APENAS ESTA VERSÃO CORRIGIDA
        # Dentro da classe PlayScene

        # Dentro da classe PlayScene

        # Substitua seu método spawn_enemy por este:
    def spawn_enemy(self):
            """Gera um único inimigo em uma posição aleatória e segura."""

            # Loop para garantir que a posição de spawn seja segura
            while True:
                # Escolhe um lado aleatoriamente (0: cima, 1: direita, 2: baixo, 3: esquerda)
                side = random.randint(0, 3)

                if side == 0:  # Cima
                    pos = (random.randint(0, WIN_WIDTH), -50)
                elif side == 1:  # Direita
                    pos = (WIN_WIDTH + 50, random.randint(0, WIN_HEIGHT))
                elif side == 2:  # Baixo
                    pos = (random.randint(0, WIN_WIDTH), WIN_HEIGHT + 50)
                else:  # Esquerda
                    pos = (-50, random.randint(0, WIN_HEIGHT))

                # Converte a posição para um vetor para facilitar o cálculo de distância
                spawn_pos_vec = pygame.math.Vector2(pos)
                player_pos_vec = self.player.position

                # Calcula a distância entre o ponto de spawn e o jogador
                distance = spawn_pos_vec.distance_to(player_pos_vec)

                # Se a distância for segura, sai do loop e usa essa posição
                if distance > self.player_spawn_safe_radius:
                    break

            # Quando o loop termina, 'pos' contém uma posição segura
            new_enemy = Enemy(position=pos,
                              player=self.player,
                              strength_multiplier=self.enemy_strength_multiplier)

            self.all_sprites.add(new_enemy)
            self.enemies.add(new_enemy)

    def update(self):
        # Este método está correto.
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
            print("Horda derrotada! Próxima horda em 5 segundos...")

        self.all_sprites.update()

        hits = pygame.sprite.groupcollide(self.arrows, self.enemies, True, False)
        for arrow, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(arrow.damage)
                if not enemy.alive():
                    self.player.xp += enemy.xp_drop
                    print(f"Inimigo derrotado! +{enemy.xp_drop} XP.")

        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if player_hits:
            print("Colisão! O jogador perdeu.")
            return 'MENU'

    def draw(self, screen: Surface):
        # Este método está correto.
        screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(screen)
        self.hud.draw(screen)