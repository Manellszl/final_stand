#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame


class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, name: str, position: tuple, path: str):
        super().__init__()

        self.name = name
        self.position = pygame.math.Vector2(position)

        self.image = pygame.image.load(path).convert_alpha()

        self.rect = self.image.get_rect(center=self.position)

        self.speed = 0

    @abstractmethod
    def update(self):
        # O método update é chamado automaticamente pelo grupo de sprites
        pass