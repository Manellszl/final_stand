import pygame
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, position: tuple):
        super().__init__("wolf", position, './assets/wolf.png')
        self.speed = 2
        self.health = 100

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.kill()
    def update(self):
        self.position.x -= self.speed
        if self.rect.right < 0:
            self.kill()
        self.rect.center = self.position