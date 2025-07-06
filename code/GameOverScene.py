import pygame
import code.ScoreManager as sm
from pygame import Surface
from code.const import WIN_WIDTH, COLOR_RED, COLOR_WHITE, COLOR_YELLOW


class GameOverScene:
    def __init__(self, window: Surface):
        self.window = window
        self.font_large = pygame.font.SysFont("dejavusansmono", 100, bold=True)
        self.font_medium = pygame.font.SysFont("dejavusansmono", 50, bold=True)
        self.font_small = pygame.font.SysFont("dejavusansmono", 30, bold=True)
        self.menu_option = 0

        # Atributos para as estatísticas, que serão definidos depois
        self.final_level = 0
        self.waves_survived = 0
        self.enemies_killed = 0
        self.menu_options_list = ['RETRY', 'MENU']

    def set_stats(self, level: int, waves: int, kills: int):
        """Recebe as estatísticas finais da PlayScene."""
        self.final_level = level
        self.waves_survived = waves - 1  # Mostra a última wave completada
        self.enemies_killed = kills

        current_run_score = {
            "level": self.final_level,
            "waves": self.waves_survived,
            "kills": self.enemies_killed
        }
        # Adiciona e salva a pontuação assim que a tela de Game Over é criada
        sm.add_score(current_run_score)
        print("Pontuação salva!")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu_option = (self.menu_option + 1) % len(self.menu_options_list)
                elif event.key == pygame.K_UP:
                    self.menu_option = (self.menu_option - 1) % len(self.menu_options_list)
                elif event.key == pygame.K_RETURN:
                    if self.menu_option == 0:  # RETRY
                        return 'PLAYING'  # Retorna comando para jogar de novo
                    elif self.menu_option == 1:  # MENU
                        return 'MENU'
        return None

    def update(self):
        pass  # Nada para atualizar

    def draw(self, screen: Surface):
        screen.fill((10, 10, 30))  # Fundo escuro

        # Desenha "GAME OVER"
        game_over_surf = self.font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_surf.get_rect(center=(WIN_WIDTH / 2, 100))
        screen.blit(game_over_surf, game_over_rect)

        # Desenha as estatísticas
        stats_text = [
            f"Nivel Final: {self.final_level}",
            f"Hordas Sobrevividas: {self.waves_survived}",
            f"Inimigos Eliminados: {self.enemies_killed}"
        ]
        for i, text in enumerate(stats_text):
            stat_surf = self.font_small.render(text, True, COLOR_WHITE)
            stat_rect = stat_surf.get_rect(center=(WIN_WIDTH / 2, 250 + i * 40))
            screen.blit(stat_surf, stat_rect)

        # Desenha as opções
        for i, option_text in enumerate(self.menu_options_list):
            color = COLOR_WHITE
            if i == self.menu_option:
                color = COLOR_YELLOW

            option_surf = self.font_medium.render(option_text, True, color)
            option_rect = option_surf.get_rect(center=(WIN_WIDTH / 2, 450 + i * 60))
            screen.blit(option_surf, option_rect)