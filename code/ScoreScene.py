import pygame
from pygame import Surface
import code.ScoreManager as sm
from code.const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, COLOR_YELLOW


class ScoreScene:
    def __init__(self, window: Surface):
        self.window = window
        self.font_large = pygame.font.SysFont("dejavusansmono", 80, bold=True)
        self.font_medium = pygame.font.SysFont("dejavusansmono", 20, bold=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'MENU'
        return None

    def update(self):
        pass

    def draw(self, screen: Surface):
        self.scores = sm.load_scores()
        screen.fill((10, 10, 30))

        # Desenha o título
        title_surf = self.font_large.render("High Scores", True, COLOR_YELLOW)
        title_rect = title_surf.get_rect(center=(WIN_WIDTH / 2, 50))
        screen.blit(title_surf, title_rect)
        top_scores = self.scores[:10]
        start_y = 130

        if not top_scores:
            no_scores_surf = self.font_medium.render("Nenhuma pontuacao registrada", True, COLOR_WHITE)
            no_scores_rect = no_scores_surf.get_rect(center=(WIN_WIDTH / 2, 250))
            screen.blit(no_scores_surf, no_scores_rect)
        else:
            for i, score in enumerate(top_scores):
                score_text = f"#{i + 1:02d} | Nivel: {score['level']:<2} | Hordas: {score['waves']:<3} | Abates: {score['kills']}"
                score_surf = self.font_medium.render(score_text, True, COLOR_WHITE)
                score_rect = score_surf.get_rect(center=(WIN_WIDTH / 2, start_y + i * 35))
                screen.blit(score_surf, score_rect)

        back_surf = self.font_medium.render("Pressione ESC para voltar ao Menu", True, COLOR_YELLOW)
        back_rect = back_surf.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT - 50))
        screen.blit(back_surf, back_rect)