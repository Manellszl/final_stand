#!/usr/bin/python
# -*- coding: utf-8 -*-

from Scene import Scene


class Menu(Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.start_button_rect = None
        self.quit_button_rect = None
        self.title_font = None

    def handle_events(self, events):
        pass

    def update(self, ):
        pass

    def draw(self, screen):
        pass
