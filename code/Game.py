import pygame
from code.Menu import Menu
from code.PlayScene import PlayScene
from code.GameOverScene import GameOverScene  # Importe a nova cena
from code.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.is_running = True

        # Armazena as instâncias das cenas
        self.scenes = {
            'MENU': Menu(self.window),
            'PLAYING': PlayScene(self.window),
            'GAME_OVER': GameOverScene(self.window)
        }
        self.active_scene_name = 'MENU'

    def run(self):
        clock = pygame.time.Clock()

        while self.is_running:
            active_scene = self.scenes[self.active_scene_name]

            events = pygame.event.get()
            command_from_events = active_scene.handle_events(events)
            command_from_update = active_scene.update()

            # Processa o comando de qualquer uma das fontes
            command = command_from_events or command_from_update

            if command == 'QUIT':
                self.is_running = False
            elif command == 'GAME_OVER':
                # Pega as estatísticas da PlayScene antes de mudar
                stats = {
                    "level": active_scene.player.level,
                    "waves": active_scene.wave_number,
                    "kills": active_scene.enemies_killed
                }
                # Passa as estatísticas para a cena de Game Over
                self.scenes['GAME_OVER'].set_stats(**stats)
                self.active_scene_name = 'GAME_OVER'
            elif command is not None:  # Se for 'MENU' ou 'PLAYING'
                # IMPORTANTE: Se o comando for para jogar, reseta a PlayScene
                if command == 'PLAYING':
                    self.scenes['PLAYING'] = PlayScene(self.window)

                # Reseta a cena do menu também, se estiver vindo do Game Over
                if self.active_scene_name == 'GAME_OVER' and command == 'MENU':
                    self.scenes['MENU'] = Menu(self.window)

                self.active_scene_name = command

            active_scene.draw(self.window)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        quit()