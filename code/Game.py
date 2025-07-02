import pygame
from code.Menu import Menu
from code.PlayScene import PlayScene  # Importe a nova cena
from code.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.is_running = True

        # Cria todas as cenas que o jogo terá
        self.scenes = {
            'MENU': Menu(self.window),
            'PLAYING': PlayScene(self.window)
        }
        # Define a cena inicial
        self.active_scene_name = 'MENU'

    def run(self):
        clock = pygame.time.Clock()

        while self.is_running:
            active_scene = self.scenes[self.active_scene_name]

            # 1. Lidando com Eventos
            events = pygame.event.get()
            command = active_scene.handle_events(events)

            if command == 'QUIT':
                self.is_running = False
            elif command is not None:  # Se a cena retornou um comando para trocar
                self.active_scene_name = command

            # 2. Atualizando a Lógica
            # Algumas cenas podem retornar comandos também no update (ex: colisão)
            command_from_update = active_scene.update()
            if command_from_update is not None:
                self.active_scene_name = command_from_update

            # 3. Desenhando na Tela
            active_scene.draw(self.window)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        quit()