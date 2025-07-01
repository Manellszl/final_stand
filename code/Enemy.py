#!/usr/bin/python
# -*- coding: utf-8 -*-

from Entity import Entity


class Enemy(Entity):
    def __init__(self):
        self.vida = None
        self.dano = None
        self.xp_drop = None

    def take_damage(self, amount):
        pass

    def die(self, ):
        pass

    def chase_player(self, player_pos):
        pass
