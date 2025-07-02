import pygame
from pygame import Surface
from code.Player import Player
from code.Enemy import Enemy
from code.const import WIN_WIDTH, WIN_HEIGHT # Importe também a altura

class PlayScene:
    def __init__(self, window: Surface):
        self.window = window

        # --- MUDANÇA 1: Carrega e redimensiona o fundo ---
        # Carrega a imagem
        background_image = pygame.image.load('./assets/fundofase.jpg').convert() # Use .convert() para imagens sem transparência
        # Redimensiona para o tamanho exato da tela
        self.background = pygame.transform.scale(background_image, (WIN_WIDTH, WIN_HEIGHT))
        self.background_rect = self.background.get_rect(left=0, top=0)

        # Usando Grupos de Sprites do Pygame
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Cria o jogador e o adiciona ao grupo de todos os sprites
        self.player = Player(position=(WIN_WIDTH / 2, 500))
        self.all_sprites.add(self.player)

        # Cria um inimigo inicial para teste
        self.spawn_enemy()

    # ... (seus métodos spawn_enemy, handle_events, e update continuam iguais) ...
    def spawn_enemy(self):
        new_enemy = Enemy(position=(WIN_WIDTH, 480))
        self.all_sprites.add(new_enemy)
        self.enemies.add(new_enemy)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'MENU'
        return None

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            print("Colisão! O jogador perdeu.")
            return 'MENU'

    def draw(self, screen: Surface):
        """Desenha tudo na tela."""

        # --- MUDANÇA 2: Desenha o fundo primeiro ---
        screen.blit(self.background, self.background_rect)

        # Depois, desenha TODOS os sprites por cima do fundo
        self.all_sprites.draw(screen)