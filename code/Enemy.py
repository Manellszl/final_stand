import pygame
import random
from code.Entity import Entity
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


def tint_surface(surface, color):
    tinted_surface = surface.copy()
    tinted_surface.fill(color, special_flags=pygame.BLEND_RGB_MULT)
    return tinted_surface


class Enemy(Entity):
    def __init__(self, position: tuple, player, enemies_group, enemy_type: str, strength_multiplier: float = 1.0):
        super().__init__("wolf", position, './assets/wolf_walk_down_0.png')

        # --- ANIMAÇÕES ---
        self.animations = {
            'walk_down': load_animation_frames('./assets/wolf_walk_down', 6),
            'walk_up': load_animation_frames('./assets/wolf_walk_up', 6),
            'walk_side': load_animation_frames('./assets/wolf_walk_side', 6),
            'attack_down': load_animation_frames('./assets/wolf_attack_down', 4),
            'attack_side': load_animation_frames('./assets/wolf_attack_side', 4),
            'death': load_animation_frames('./assets/wolf_death', 5)
        }

        if enemy_type == 'fast':
            tint_color = (120, 170, 255)
            for key in self.animations:
                self.animations[key] = [tint_surface(frame, tint_color) for frame in self.animations[key]]
        elif enemy_type == 'tank':
            tint_color = (160, 110, 60)
            for key in self.animations:
                self.animations[key] = [tint_surface(frame, tint_color) for frame in self.animations[key]]

        # --- CONTROLE DE ANIMAÇÃO E ESTADO ---
        self.frame_index = 0
        self.animation_speed = 150
        self.last_animation_update = pygame.time.get_ticks()
        self.state = 'wandering'
        self.facing_direction = 'down'

        # --- REFERÊNCIAS ---
        self.player = player
        self.enemies_group = enemies_group

        # --- ATRIBUTOS BASEADOS NO TIPO ---
        base_health, base_speed, base_xp = 100, 2.0, 30
        if enemy_type == 'fast':
            base_health *= 0.7
            base_speed *= 1.6
            base_xp *= 1.2
        elif enemy_type == 'tank':
            base_health *= 2.0
            base_speed *= 0.7
            base_xp *= 1.5

        self.health = int(base_health * strength_multiplier)
        self.chase_speed = random.uniform(base_speed, base_speed + 0.5)
        self.xp_drop = int(base_xp * strength_multiplier)
        self.attack_damage = int(10 * strength_multiplier)

        # --- ATRIBUTOS DE IA E COMBATE ---
        self.velocity = pygame.math.Vector2()
        self.detection_radius = 800
        self.attack_range = 60
        self.attack_cooldown = 1800
        self.last_attack_time = 0
        self.wander_speed = 0.5
        self.wander_direction = self.get_random_wander_direction()
        self.last_wander_change = 0
        self.wander_interval = random.randint(2000, 4000)
        self.last_hit_time = -1000
        self.hit_flash_duration = 100
        self.separation_radius = 50
        self.separation_strength = 1.5

        self.image = self.animations['walk_down'][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.radius = self.rect.width / 2

    @staticmethod
    def get_random_wander_direction():
        return pygame.math.Vector2(1, 0).rotate(random.uniform(0, 360))

    def wander(self):
        if pygame.time.get_ticks() - self.last_wander_change > self.wander_interval:
            self.last_wander_change = pygame.time.get_ticks()
            self.wander_direction = self.get_random_wander_direction()
        return self.wander_direction * self.wander_speed

    def chase(self):
        if self.player.position.distance_to(self.position) > 0:
            return (self.player.position - self.position).normalize() * self.chase_speed
        return pygame.math.Vector2()

    def separation(self):
        steering = pygame.math.Vector2()
        for enemy in self.enemies_group:
            if enemy != self:
                distance = self.position.distance_to(enemy.position)
                if 0 < distance < self.separation_radius:
                    steering += (self.position - enemy.position) / (distance * distance)
        return steering

    def take_damage(self, amount: int):
        if self.state != 'death':
            self.last_hit_time = pygame.time.get_ticks()
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.state = 'death'
                self.frame_index = 0
                return True
        return False

    def set_state(self):
        if self.state == 'death': return

        distance_to_player = self.position.distance_to(self.player.position)
        now = pygame.time.get_ticks()

        if distance_to_player < self.attack_range and (now - self.last_attack_time > self.attack_cooldown):
            self.state = 'attack'
            self.frame_index = 0
            self.last_attack_time = now
        elif distance_to_player < self.detection_radius and self.state != 'attack':
            self.state = 'chasing'
        elif self.state != 'attack':
            self.state = 'wandering'

    def set_velocity(self):
        if self.state == 'chasing':
            self.velocity = self.chase() + self.separation() * self.separation_strength
        elif self.state == 'wandering':
            self.velocity = self.wander() + self.separation() * self.separation_strength
        else:
            self.velocity = pygame.math.Vector2()

    def animate(self):
        now = pygame.time.get_ticks()

        if self.state == 'death':
            animation_frames = self.animations['death']
        else:
            if self.velocity.magnitude() > 0.1:
                if abs(self.velocity.x) > abs(self.velocity.y):
                    self.facing_direction = 'right' if self.velocity.x > 0 else 'left'
                else:
                    self.facing_direction = 'down' if self.velocity.y > 0 else 'up'

            action = 'attack' if self.state == 'attack' else 'walk'
            direction_key = 'side' if self.facing_direction in ['left', 'right'] else self.facing_direction
            animation_key = f"{action}_{direction_key}"
            animation_frames = self.animations.get(animation_key, self.animations[f'{action}_down'])

        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.frame_index += 1

        if self.frame_index >= len(animation_frames):
            if self.state == 'attack':
                if self.position.distance_to(self.player.position) < self.attack_range + 10:
                    self.player.take_damage(self.attack_damage)
                self.state = 'wandering'
            elif self.state == 'death':
                self.kill()
                return
            self.frame_index = 0

        self.image = animation_frames[self.frame_index]
        if self.facing_direction == 'right':
            self.image = pygame.transform.flip(self.image, True, False)

        if now - self.last_hit_time < self.hit_flash_duration:
            red_image = self.image.copy()
            red_image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
            self.image = red_image

        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.set_state()
        self.set_velocity()
        self.animate()

        self.position += self.velocity
        self.rect.center = self.position

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIN_WIDTH: self.rect.right = WIN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT: self.rect.bottom = WIN_HEIGHT
        self.position.x, self.position.y = self.rect.centerx, self.rect.centery