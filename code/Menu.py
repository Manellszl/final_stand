import pygame
from PIL import Image
from pygame import Surface
from pygame.font import Font

from code.const import WIN_HEIGHT, WIN_WIDTH, COLOR_YELLOW, MENU_OPTION, COLOR_WHITE, COLOR_RED, COLOR_DARK_YELLOW

def carregar_gif_para_frames(caminho_gif):
    frames = []
    with Image.open(caminho_gif) as gif:
        try:
            while True:
                frame_pil = gif.convert('RGBA')
                dados_frame = frame_pil.tobytes()
                tamanho_frame = frame_pil.size

                surface_pygame = pygame.image.fromstring(dados_frame, tamanho_frame, 'RGBA')
                surface_pygame = pygame.transform.scale(surface_pygame, (WIN_WIDTH, WIN_HEIGHT))
                frames.append(surface_pygame)

                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
    return frames


class Menu:
    def __init__(self, window):
        self.window = window
        self.title_font = pygame.font.SysFont(name="dejavusansmono", size=150, bold=True)
        self.option_font = pygame.font.SysFont(name="dejavusansmono", size=50, bold=True)
        self.frames = carregar_gif_para_frames(
            './assets/menu.gif')
        self.rect = self.frames[0].get_rect(left=0, top=0)
        self.menu_option = 0
        self.frame_index = 0
        self.animation_speed = 250
        self.last_update = pygame.time.get_ticks()

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu_option = (self.menu_option + 1) % len(MENU_OPTION)
                elif event.key == pygame.K_UP:
                    self.menu_option = (self.menu_option - 1) % len(MENU_OPTION)
                elif event.key == pygame.K_RETURN:
                    selected_text = MENU_OPTION[self.menu_option].strip()
                    if selected_text == 'START':
                        return 'PLAYING'
                    elif selected_text == 'EXIT':
                        return 'QUIT'
                    else:
                        return 'SCORE'
        return None

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen: Surface):
        screen.blit(self.frames[self.frame_index], self.rect)
        self.menu_text(self.title_font, 'FINAL', COLOR_DARK_YELLOW, (WIN_WIDTH / 2, 70))
        self.menu_text(self.title_font, 'STAND', COLOR_DARK_YELLOW, (WIN_WIDTH / 2, 170))

        for i, option_text in enumerate(MENU_OPTION):
            color = COLOR_WHITE
            if i == self.menu_option:
                color = COLOR_YELLOW
            elif option_text.strip() == 'EXIT':
                color = COLOR_RED

            self.menu_text(self.option_font, option_text, color, (WIN_WIDTH / 2, 300 + 60 * i))

    def menu_text(self, font: Font, text: str, text_color: tuple, text_center_pos: tuple):
        text_surf = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)