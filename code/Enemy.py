import pygame
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, position: tuple):
        super().__init__("wolf", position, './assets/wolf.png') # Crie uma imagem 'wolf.png'
        self.speed = 2

    def update(self):
        # Lógica de movimento simples: apenas para a esquerda
        self.position.x -= self.speed
        if self.rect.right < 0:
            self.kill() # Remove o sprite de todos os grupos quando ele sai da tela

        self.rect.center = self.position