import pygame
from code.Entity import Entity
from code.const import WIN_WIDTH, WIN_HEIGHT


def load_animation_frames(path_prefix, frame_count):
    """Função auxiliar para carregar uma sequência de frames."""
    frames = []
    for i in range(frame_count):
        # Assumindo que os arquivos são nomeados como 'caminho_0.png', 'caminho_1.png', etc.
        path = f"{path_prefix}_{i}.png"
        try:
            frames.append(pygame.image.load(path).convert_alpha())
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {path}\n{e}")
    return frames


class Player(Entity):
    def __init__(self, position: tuple):
        # O init da classe Entity agora espera o caminho, então passamos um placeholder
        # já que vamos sobrescrever self.image imediatamente.
        super().__init__("player", position, './assets/player_idle_0.png')  # Use a primeira imagem como placeholder

        # --- LÓGICA DE ANIMAÇÃO ---
        self.animations = {
            'idle': load_animation_frames('./assets/player_idle', 4),  # Ex: 2 frames para a animação de parado
            'walk': load_animation_frames('./assets/player_walk', 2)  # Ex: 4 frames para a de andar
        }
        self.current_state = 'idle'
        self.current_direction = 'right'

        self.frame_index = 0
        self.animation_speed = 150  # ms por frame
        self.last_update = pygame.time.get_ticks()

        # Define a imagem inicial
        self.image = self.animations[self.current_state][self.frame_index]
        self.rect = self.image.get_rect(center=position)

        self.speed = 5
        self.is_moving = False

        # Dentro da classe Player

        # Dentro da sua classe Player, adicione este método:

    def get_input(self):
            """Processa o input do teclado para WASD e Setas."""
            self.is_moving = False
            keys = pygame.key.get_pressed()

            # Esquerda com 'A' OU Seta Esquerda
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
                self.position.x -= self.speed
                self.current_direction = 'left'
                self.is_moving = True

            # Direita com 'D' OU Seta Direita
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
                self.position.x += self.speed
                self.current_direction = 'right'
                self.is_moving = True

            # Cima com 'W' OU Seta Cima
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
                self.position.y -= self.speed
                self.is_moving = True

            # Baixo com 'S' OU Seta Baixo
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT:
                self.position.y += self.speed
                self.is_moving = True

            # Define o estado com base no movimento
            if self.is_moving:
                self.current_state = 'walk'
            else:
                self.current_state = 'idle'

    def animate(self):
        """Atualiza o frame da animação atual."""
        now = pygame.time.get_ticks()

        # Pega a lista de frames para o estado atual (idle ou walk)
        animation_frames = self.animations[self.current_state]

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            # Avança para o próximo frame, voltando ao início se chegar ao fim
            self.frame_index = (self.frame_index + 1) % len(animation_frames)

            # Atualiza a imagem para o novo frame
            new_image = animation_frames[self.frame_index]

            # Inverte a imagem se a direção for para a esquerda
            if self.current_direction == 'left':
                self.image = pygame.transform.flip(new_image, True, False)
            else:  # Direita
                self.image = new_image

            # IMPORTANTE: Atualiza o rect para o centro da posição antiga para não "pular"
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def update(self):
        """O método principal de atualização, chamado a cada quadro."""
        self.get_input()
        self.animate()

        # Atualiza a posição final do rect com base no vetor de posição
        self.rect.center = self.position