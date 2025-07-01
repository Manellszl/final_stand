import pygame
from PIL import Image
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_HEIGHT, WIN_WIDTH, COLOR_YELLOW, MENU_OPTION, COLOR_WHITE


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
        self.start_button_rect = None
        self.quit_button_rect = None

        self.frames = carregar_gif_para_frames('./assets/craftpix-net-504452-free-village-pixel-tileset-for-top-down-defense/menu.gif')
        self.rect = self.frames[0].get_rect(left=0, top=0)

        self.frame_index = 0
        self.animation_speed = 250
        self.last_update = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # ... (lógica de botões) ...

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

    def draw(self, screen: Surface):
        menu_option = 0
        current_frame = self.frames[self.frame_index]
        screen.blit(source=current_frame, dest=self.rect)

        self.menu_text(150, 'FINAL', COLOR_YELLOW, ((WIN_WIDTH / 2), 70))
        self.menu_text(150, 'STAND', COLOR_YELLOW, ((WIN_WIDTH / 2), 170))

        for i in range(len(MENU_OPTION)):
            if i ==menu_option:
                self.menu_text(50, MENU_OPTION [i], COLOR_WHITE, ((WIN_WIDTH / 2), 300 + 60 * i))
            else:
                self.menu_text(50, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 300 + 60 * i))
        pygame.display.flip()

    # 3. Desenhe outros elementos aqui (botões, etc.)
        # Ex: pygame.draw.rect(screen, 'red', self.start_button_rect)


    def run(self):
        pygame.mixer_music.load('./assets/craftpix-net-504452-free-village-pixel-tileset-for-top-down-defense/Menu.mp3')
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        menu_rodando = True
        while menu_rodando:
            events = pygame.event.get()
            self.handle_events(events)

            self.update()

            self.draw(self.window)

            pygame.display.flip()
            clock.tick(60)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="dejavusansmono", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text,  True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

