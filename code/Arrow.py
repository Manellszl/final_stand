import pygame
from code.Entity import Entity
from math import atan2, degrees


class Arrow(Entity):
    def __init__(self, start_pos: tuple, target_pos: tuple, damage: int):
        super().__init__("arrow", start_pos, './assets/arrow.png')

        self.damage = damage
        self.speed = 15

        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        self.velocity = direction.normalize() * self.speed

        angle = degrees(atan2(-self.velocity.y, self.velocity.x))

        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=start_pos)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()