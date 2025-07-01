#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Menu import Menu
from code.const import WIN_WIDTH, WIN_HEIGHT


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.clock = None
        self.is_running = None
        self.active_scene = None


    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()


    def change_scene(self, new_scene_name):
        pass





