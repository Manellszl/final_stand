import pygame
from pygame import Surface
from code.const import COLOR_WHITE, COLOR_YELLOW


class HUD:
    def __init__(self, player):
        # Armazena uma referência ao jogador para acessar seus atributos
        self.player = player

        # Carrega a fonte que será usada
        self.font = pygame.font.SysFont("dejavusansmono", 24, bold=True)

        # Configurações da barra de vida
        self.health_bar_pos = (20, 20)
        self.bar_width = 200
        self.bar_height = 20
        self.health_bar_color = (255, 0, 0)  # Vermelho

        # Configurações da barra de XP
        self.xp_bar_pos = (20, 50)
        self.xp_bar_color = (0, 0, 255)  # Azul

    def draw(self, screen: Surface):
        """Desenha todos os elementos do HUD na tela."""

        # --- Barra de Vida ---
        # Calcula a proporção de vida atual
        health_ratio = self.player.health / self.player.max_health
        # Desenha o fundo cinza da barra
        pygame.draw.rect(screen, (100, 100, 100), (*self.health_bar_pos, self.bar_width, self.bar_height))
        # Desenha a parte preenchida da barra de vida
        pygame.draw.rect(screen, self.health_bar_color,
                         (*self.health_bar_pos, self.bar_width * health_ratio, self.bar_height))
        # Desenha uma borda
        pygame.draw.rect(screen, COLOR_WHITE, (*self.health_bar_pos, self.bar_width, self.bar_height), 2)

        # --- Barra de XP ---
        xp_ratio = self.player.xp / self.player.xp_to_next_level
        pygame.draw.rect(screen, (100, 100, 100), (*self.xp_bar_pos, self.bar_width, self.bar_height))
        pygame.draw.rect(screen, self.xp_bar_color, (*self.xp_bar_pos, self.bar_width * xp_ratio, self.bar_height))
        pygame.draw.rect(screen, COLOR_WHITE, (*self.xp_bar_pos, self.bar_width, self.bar_height), 2)

        # --- Texto do Nível ---
        level_text = f"Level: {self.player.level}"
        text_surf = self.font.render(level_text, True, COLOR_YELLOW)
        # Posiciona o texto ao lado das barras
        text_rect = text_surf.get_rect(left=self.health_bar_pos[0] + self.bar_width + 10,
                                       centery=self.health_bar_pos[1] + self.bar_height / 2)
        screen.blit(text_surf, text_rect)

        # --- Texto de Vida (Opcional) ---
        health_text = f"{self.player.health} / {self.player.max_health}"
        health_text_surf = self.font.render(health_text, True, COLOR_WHITE)
        health_text_rect = health_text_surf.get_rect(
            center=(self.health_bar_pos[0] + self.bar_width / 2, self.health_bar_pos[1] + self.bar_height / 2))
        screen.blit(health_text_surf, health_text_rect)