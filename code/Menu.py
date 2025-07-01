import pygame
from PIL import Image
from pygame import Surface, Rect
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
        self.start_button_rect = None
        self.quit_button_rect = None
        self.title_font = pygame.font.SysFont(name="dejavusansmono", size=150, bold=True)
        self.option_font = pygame.font.SysFont(name="dejavusansmono", size=50, bold=True)
        self.frames = carregar_gif_para_frames('./assets/craftpix-net-504452-free-village-pixel-tileset-for-top-down-defense/menu.gif')
        self.rect = self.frames[0].get_rect(left=0, top=0)
        self.menu_option = 0
        self.frame_index = 0
        self.animation_speed = 250
        self.last_update = pygame.time.get_ticks()

    def handle_events(self, events):
        # Check for all events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # Todas as referências a 'menu_option' agora usam 'self.menu_option'
                if event.key == pygame.K_DOWN:
                    if self.menu_option < len(MENU_OPTION) - 1:
                        self.menu_option += 1
                    else:
                        self.menu_option = 0
                if event.key == pygame.K_UP:
                    if self.menu_option > 0:
                        self.menu_option -= 1
                    else:
                        self.menu_option = len(MENU_OPTION) - 1
                if event.key == pygame.K_RETURN:
                    return MENU_OPTION[self.menu_option]
        return None

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

    def draw(self, screen: Surface):
        current_frame = self.frames[self.frame_index]
        screen.blit(source=current_frame, dest=self.rect)

        self.menu_text(self.title_font, 'FINAL', COLOR_DARK_YELLOW, ((WIN_WIDTH / 2), 70))
        self.menu_text(self.title_font, 'STAND', COLOR_DARK_YELLOW, ((WIN_WIDTH / 2), 170))

        for i in range(len(MENU_OPTION)):
            option_text = MENU_OPTION[i]

            if i == self.menu_option:
                color = COLOR_YELLOW
            elif option_text.strip() == 'EXIT':
                color = COLOR_RED
            else:
                color = COLOR_WHITE

            self.menu_text(self.option_font, option_text, color, ((WIN_WIDTH / 2), 300 + 60 * i))



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

    def menu_text(self, font: Font, text: str, text_color: tuple, text_center_pos: tuple):
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
