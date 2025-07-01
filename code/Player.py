#!/usr/bin/python
# -*- coding: utf-8 -*-

from Entity import Entity


class Player(Entity):
    def __init__(self):
        self.vida = None
        self.força = None
        self.velocidade = None
        self.cadencia = None
        self.level = None
        self.xp_atual = None
        self.xp_para_proximo_level = None
        self.pontos_de_atributo = None
        self.ultimo_tiro_timestamp = None

    def get_input(self, ):
        pass

    def move(self, ):
        pass

    def shoot(self, target_pos):
        pass

    def add_xp(self, amount):
        pass

    def level_up(self, ):
        pass

    def upgrade_attribute(self, attribute_name):
        pass
