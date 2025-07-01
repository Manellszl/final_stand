#!/usr/bin/python
# -*- coding: utf-8 -*-

from Scene import Scene


class Game(Scene):
    def __init__(self):
        self.player = None
        self.all_sprites = None
        self.enemies = None
        self.projectiles = None
        self.wave_manager = None
        self.hud = None

    def handle_events(self, events):
        pass

    def update(self, ):
        pass

    def draw(self, screen):
        pass

    def check_collisions(self, ):
        pass

    def check_level_up(self, ):
        pass
