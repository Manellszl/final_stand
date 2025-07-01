#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Menu import Menu


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(600, 480))
        self.clock = None
        self.is_running = None
        self.active_scene = None


    def run(self):
        while True:
            menu = Menu(self.window)
            menu.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def change_scene(self, new_scene_name):
        pass





