import pygame
from code.Entity import Entity
from code.Arrow import Arrow
from code.const import WIN_WIDTH, WIN_HEIGHT


def load_animation_frames(path_prefix, frame_count):
    frames = []
    for i in range(frame_count):
        path = f"{path_prefix}_{i}.png"
        try:
            frames.append(pygame.image.load(path).convert_alpha())
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {path}\n{e}")
    return frames

class Player(Entity):

    def __init__(self, position: tuple, groups: dict):
        super().__init__("player", position, './assets/player_idle_0.png')
        self.animations = {
            'idle': load_animation_frames('./assets/player_idle', 4),
            'walk': load_animation_frames('./assets/player_walk', 2),
            'shoot': load_animation_frames('./assets/player_shoot', 6)
        }
        self.groups = groups

        # --- ATRIBUTOS PARA O HUD ---
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

        self.is_shooting = False
        self.shoot_cooldown = 1000
        self.last_shot_time = 0
        self.arrow_damage = 100
        self.shoot_target_pos = None
        self.current_state = 'idle'
        self.current_direction = 'right'
        self.frame_index = 0
        self.animation_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.image = self.animations[self.current_state][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.is_moving = False

    def get_input(self):
        self.is_moving = False
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.position.x -= self.speed
            self.current_direction = 'left'
            self.is_moving = True
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.position.x += self.speed
            self.current_direction = 'right'
            self.is_moving = True
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.position.y -= self.speed
            self.is_moving = True
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT:
            self.position.y += self.speed
            self.is_moving = True

    def handle_events(self, events):
        now = pygame.time.get_ticks()

        self.get_input()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.is_shooting and (now - self.last_shot_time > self.shoot_cooldown):
                    self.is_shooting = True
                    self.frame_index = 0
                    self.last_shot_time = now
                    self.shoot_target_pos = event.pos

    def animate(self):
        now = pygame.time.get_ticks()

        if self.is_shooting:
            self.current_state = 'shoot'
            if self.shoot_target_pos:
                if self.shoot_target_pos[0] < self.rect.centerx:
                    self.current_direction = 'left'
                else:
                    self.current_direction = 'right'
        elif self.is_moving:
            self.current_state = 'walk'
        else:
            self.current_state = 'idle'

        animation_frames = self.animations[self.current_state]

        if now - self.last_update > self.animation_speed:
            self.last_update = now

            self.frame_index += 1

            if self.frame_index >= len(animation_frames):
                if self.current_state == 'shoot':
                    self.is_shooting = False
                    self.frame_index = 0
                    self.shoot()
                else:
                    self.frame_index = 0

            new_image = animation_frames[self.frame_index]
            if self.current_direction == 'left':
                self.image = pygame.transform.flip(new_image, True, False)
            else:
                self.image = new_image
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def shoot(self):
        if self.shoot_target_pos:
            new_arrow = Arrow(self.rect.center, self.shoot_target_pos, self.arrow_damage)
            self.groups['all'].add(new_arrow)
            self.groups['arrows'].add(new_arrow)
            self.shoot_target_pos = None  # Limpa o alvo

    def update(self):
        self.animate()
        self.rect.center = self.position