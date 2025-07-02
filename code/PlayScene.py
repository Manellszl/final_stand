import pygame
from pygame import Surface
from code.Player import Player
from code.Enemy import Enemy
from code.const import WIN_WIDTH, WIN_HEIGHT

class PlayScene:
    def __init__(self, window: Surface):
        self.window = window
        self.background = pygame.transform.scale(pygame.image.load('./assets/fundofase.jpg').convert(), (WIN_WIDTH, WIN_HEIGHT))
        self.background_rect = self.background.get_rect(left=0, top=0)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()

        groups = {
            'all': self.all_sprites,
            'arrows': self.arrows
        }
        self.player = Player(position=(WIN_WIDTH / 2, 500), groups=groups)
        self.all_sprites.add(self.player)

        self.spawn_enemy()
    # ... (resto da classe) ...
    def spawn_enemy(self):
        new_enemy = Enemy(position=(WIN_WIDTH, 480))
        self.all_sprites.add(new_enemy)
        self.enemies.add(new_enemy)

    def handle_events(self, events):

        self.player.handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'MENU'
        return None

    def update(self):
        self.all_sprites.update()

        hits = pygame.sprite.groupcollide(self.arrows, self.enemies, True, False)
        for arrow, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(arrow.damage)
                print(f"Inimigo atingido! Vida restante: {enemy.health}")

        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if player_hits:
            print("Colisão! O jogador perdeu.")
            return 'MENU'

    def draw(self, screen: Surface):
        screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(screen)