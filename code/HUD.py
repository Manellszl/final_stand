import pygame
from pygame import Surface
from code.const import COLOR_WHITE, COLOR_YELLOW, WIN_WIDTH


class HUD:
    def __init__(self, player):
        self.player = player

        self.font = pygame.font.SysFont("dejavusansmono", 24, bold=True)

        # Configurações da barra de vida
        self.health_bar_pos = (20, 20)
        self.bar_width = 200
        self.bar_height = 20
        self.health_bar_color = (255, 0, 0)

        # Configurações da barra de XP
        self.xp_bar_pos = (20, 50)
        self.xp_bar_color = (0, 0, 255)


    def draw(self, screen: Surface, current_wave: int):

            # --- 1. Barra de Vida ---
            health_ratio = 1.0
            if self.player.max_health > 0:
                health_ratio = self.player.health / self.player.max_health

            pygame.draw.rect(screen, (100, 100, 100), (*self.health_bar_pos, self.bar_width, self.bar_height))
            pygame.draw.rect(screen, self.health_bar_color,
                             (*self.health_bar_pos, self.bar_width * health_ratio, self.bar_height))
            pygame.draw.rect(screen, COLOR_WHITE, (*self.health_bar_pos, self.bar_width, self.bar_height), 2)
            health_text_surf = self.font.render(f"{self.player.health}/{self.player.max_health}", True, COLOR_WHITE)
            health_text_rect = health_text_surf.get_rect(
                center=(self.health_bar_pos[0] + self.bar_width / 2, self.health_bar_pos[1] + self.bar_height / 2))
            screen.blit(health_text_surf, health_text_rect)

            # --- 2. Barra de XP ---
            xp_ratio = 1.0
            if self.player.xp_to_next_level > 0:
                xp_ratio = self.player.xp / self.player.xp_to_next_level

            pygame.draw.rect(screen, (100, 100, 100), (*self.xp_bar_pos, self.bar_width, self.bar_height))
            pygame.draw.rect(screen, self.xp_bar_color, (*self.xp_bar_pos, self.bar_width * xp_ratio, self.bar_height))
            pygame.draw.rect(screen, COLOR_WHITE, (*self.xp_bar_pos, self.bar_width, self.bar_height), 2)

            # --- 3. Texto do Nível ---
            level_text = f"Player Level: {self.player.level}"
            level_surf = self.font.render(level_text, True, COLOR_YELLOW)
            level_rect = level_surf.get_rect(left=self.health_bar_pos[0] + self.bar_width + 10,
                                             centery=self.health_bar_pos[1] + self.bar_height / 2)
            screen.blit(level_surf, level_rect)

            # --- 4. Texto da Horda ---
            wave_surf = self.font.render(f"Horda: {current_wave}", True, COLOR_WHITE)
            wave_rect = wave_surf.get_rect(topright=(WIN_WIDTH - 20, 20))
            screen.blit(wave_surf, wave_rect)

            # --- 5. Textos de Upgrade (Apenas se tiver pontos) ---
            if self.player.upgrade_points > 0:
                points_text = f"Upgrade Points: {self.player.upgrade_points}"
                points_surf = self.font.render(points_text, True, (0, 255, 0))
                points_rect = points_surf.get_rect(left=level_rect.right + 20, centery=level_rect.centery)
                screen.blit(points_surf, points_rect)

                instructions_font = pygame.font.SysFont("dejavusansmono", 18, bold=True)
                instructions_text = "[1] Vida | [2] Dano "
                instructions_surf = instructions_font.render(instructions_text, True, COLOR_WHITE)
                instructions_rect = instructions_surf.get_rect(left=self.xp_bar_pos[0],
                                                               top=self.xp_bar_pos[1] + self.bar_height + 5)
                screen.blit(instructions_surf, instructions_rect)