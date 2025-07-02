import pygame
import random
from code.Entity import Entity
# 1. Importe as constantes de tamanho da tela
from code.const import WIN_WIDTH, WIN_HEIGHT


class Enemy(Entity):
    # O método __init__ e os outros métodos (get_random_wander_direction, wander, chase, take_damage)
    # continuam exatamente iguais. Não precisam de alteração.
    def __init__(self, position: tuple, player, strength_multiplier: float = 1.0):
        super().__init__("wolf", position, './assets/wolf.png')
        self.player = player
        self.state = 'wandering'
        self.detection_radius = 300
        self.chase_speed = random.uniform(1.5, 2.5)
        self.wander_speed = 0.5
        self.wander_direction = self.get_random_wander_direction()
        self.last_wander_change = pygame.time.get_ticks()
        self.wander_interval = random.randint(2000, 4000)
        base_health = 100
        self.health = int(base_health * strength_multiplier)
        self.xp_drop = int(10 * strength_multiplier)
        self.velocity = pygame.math.Vector2(0, 0)  # Inicializa a velocidade

    def get_random_wander_direction(self):
        angle = random.uniform(0, 360)
        return pygame.math.Vector2(1, 0).rotate(angle)

    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_wander_change > self.wander_interval:
            self.last_wander_change = now
            self.wander_interval = random.randint(2000, 4000)
            self.wander_direction = self.get_random_wander_direction()
        self.velocity = self.wander_direction * self.wander_speed

    def chase(self):
        direction = (self.player.position - self.position).normalize()
        self.velocity = direction * self.chase_speed

    def take_damage(self, amount: int):
        """Reduz a vida e remove o sprite se a vida chegar a zero."""
        self.health -= amount

        # --- MUDANÇA PRINCIPAL AQUI ---
        # Se a vida acabar, chama o self.kill() imediatamente.
        if self.health <= 0:
            self.kill()  # kill() remove o sprite de todos os grupos automaticamente.

        # Agora, vamos limpar o método update para remover a lógica de morte antiga

    def update(self):
        # A lógica de IA para definir o estado e a velocidade continua a mesma
        if self.health > 0:  # A IA só funciona se o inimigo estiver vivo
            distance_to_player = self.position.distance_to(self.player.position)
            if distance_to_player < self.detection_radius:
                self.state = 'chasing'
            else:
                self.state = 'wandering'

            if self.state == 'chasing':
                self.chase()
            elif self.state == 'wandering':
                self.wander()
        else:
            # Se não tiver vida, para de se mover
            self.velocity = pygame.math.Vector2(0, 0)

        # Aplica o movimento
        self.position += self.velocity
        self.rect.center = self.position

        # A lógica de contenção na tela continua a mesma
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

        self.position.x = self.rect.centerx
        self.position.y = self.rect.centery