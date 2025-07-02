import pygame
from code.Menu import Menu
from code.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.is_running = True

        # Cria a cena do menu apenas uma vez
        self.active_scene = Menu(self.window)

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer_music.load('./assets/craftpix-net-504452-free-village-pixel-tileset-for-top-down-defense/Menu.mp3')
        pygame.mixer_music.play(-1)

        # Este é o único loop principal do jogo
        while self.is_running:
            # 1. Lidando com Eventos
            events = pygame.event.get()
            command = self.active_scene.handle_events(events)

            if command == 'QUIT':
                self.is_running = False
            elif command == 'PLAYING':
                print("Iniciando o Jogo! (Ainda não implementado)")
            elif command == 'SCORE':
                print("seu score")
                # Futuramente, você mudaria a cena aqui:
                # self.active_scene = PlayScene(self.window)

            # 2. Atualizando a Lógica
            self.active_scene.update()

            # 3. Desenhando na Tela
            self.active_scene.draw(self.window)

            # 4. Atualizando o Display
            pygame.display.flip()
            clock.tick(60)

        # Encerra o jogo quando o loop termina
        pygame.quit()
        quit()