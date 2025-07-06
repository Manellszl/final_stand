import pygame
from code.Entity import Entity
from code.Arrow import Arrow
from code.const import WIN_WIDTH, WIN_HEIGHT


def load_animation_frames(path_prefix, frame_count):
    frames = []
    for i in range(frame_count):
        path = f"{path_prefix}_{i}.png"
        try:
            frames.append(pygame.image.load(path).convert_alpha())
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {path}\n{e}")
    return frames

class Player(Entity):

    # Dentro da classe Player

    # Dentro da classe Player

    def __init__(self, position: tuple, groups: dict):
        super().__init__("player", position, './assets/player_idle_0.png')
        self.animations = {
            'idle': load_animation_frames('./assets/player_idle', 4),
            'walk': load_animation_frames('./assets/player_walk', 2),
            'shoot': load_animation_frames('./assets/player_shoot', 6)
        }
        self.groups = groups
        self.max_health = 100
        self.health = self.max_health
        self.level = 0
        self.xp = 0
        self.xp_to_next_level = 100
        self.is_alive = True

        self.upgrade_points = 0

        # --- Bloco de atributos de tiro corrigido (sem duplicação) ---
        self.is_charging = False
        self.charge_complete = False
        self.shoot_cooldown = 10
        self.last_shot_time = -self.shoot_cooldown
        self.arrow_damage = 50
        self.shoot_target_pos = None

        self.current_direction = 'right'
        self.current_state = 'idle'
        self.previous_state = self.current_state

        self.frame_index = 0
        self.animation_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.image = self.animations[self.current_state][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.speed = 1.6
        self.is_moving = False

    def get_input(self):
        self.is_moving = False
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.position.x -= self.speed
            self.current_direction = 'left'
            self.is_moving = True
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.position.x += self.speed
            self.current_direction = 'right'
            self.is_moving = True
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.position.y -= self.speed
            self.is_moving = True
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT:
            self.position.y += self.speed
            self.is_moving = True

        # Dentro da classe Player

    def handle_events(self, events):
            now = pygame.time.get_ticks()

            # Input de movimento (teclado) sempre é verificado
            self.get_input()

            # Input de tiro (mouse)
            for event in events:
                # Pressionou o botão esquerdo para começar a carregar
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Só pode começar a carregar se o cooldown já passou
                    if now - self.last_shot_time > self.shoot_cooldown:
                        self.is_charging = True
                        self.charge_complete = False  # Reseta a flag de carga
                        self.frame_index = 0  # Reinicia a animação de tiro

                # Soltou o botão esquerdo
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Se estava carregando o tiro
                    if self.is_charging:
                        # E se a carga estava completa (animação no último frame)
                        if self.charge_complete:
                            # Atira!
                            self.shoot_target_pos = event.pos
                            self.shoot()
                            self.last_shot_time = now  # Inicia o cooldown
                        else:
                            # Se soltou antes, o tiro é cancelado
                            print("Tiro cancelado!")

                        # Para de carregar, independentemente de ter atirado ou não
                        self.is_charging = False
                        self.charge_complete = False
                if event.type == pygame.KEYDOWN:
                    if self.upgrade_points > 0:  # Só funciona se tiver pontos
                        if event.key == pygame.K_1:  # Tecla 1 para Vida
                            self.upgrade_health()
                            self.upgrade_points -= 1
                        elif event.key == pygame.K_2:  # Tecla 2 para Dano
                            self.upgrade_damage()
                            self.upgrade_points -= 1

    def level_up(self):
        """Processa o level up do jogador."""
        # Usa 'while' para o caso de o jogador ganhar XP para vários níveis de uma vez
        while self.xp >= self.xp_to_next_level:
            # Subtrai o XP necessário, mas mantém o excesso
            self.xp -= self.xp_to_next_level
            self.level += 1
            # Aumenta a quantidade de XP para o próximo nível (ex: 50% mais difícil)
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            self.upgrade_points += 1
            # Cura o jogador completamente como bônus de level up
            self.health = self.max_health
            print(f"LEVEL UP! Você chegou ao nível {self.level}!")

    # --- NOVOS MÉTODOS: UPGRADES ---
    def upgrade_health(self):
        self.max_health += 20
        self.health = self.max_health  # Cura total
        print(f"Vida máxima aumentada para {self.max_health}")

    def upgrade_damage(self):
        self.arrow_damage += 10
        print(f"Dano da flecha aumentado para {self.arrow_damage}")


    def take_damage(self, amount: int):
        """Reduz a vida do jogador e atualiza seu estado se morrer."""
        if self.health > 0:  # Só pode tomar dano se estiver vivo
            self.health -= amount
            print(f"Jogador atingido! Vida atual: {self.health}")
            if self.health <= 0:
                self.health = 0
                self.is_alive = False  # Sinaliza que o jogador morreu
                print("O jogador foi derrotado!")
                self.kill()  # Remove o sprite do jogador dos grupos

    def animate(self):
        now = pygame.time.get_ticks()

        # Define o estado da animação
        if self.is_charging:
            self.current_state = 'shoot'
            # Vira o personagem na direção do mouse
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x < self.rect.centerx:
                self.current_direction = 'left'
            else:
                self.current_direction = 'right'
        elif self.is_moving:
            self.current_state = 'walk'
        else:
            self.current_state = 'idle'

        # --- MUDANÇA PRINCIPAL AQUI ---
        # Se o estado mudou desde o último frame, reseta a animação
        if self.current_state != self.previous_state:
            self.frame_index = 0
        # Atualiza o estado anterior para o próximo ciclo
        self.previous_state = self.current_state

        animation_frames = self.animations[self.current_state]

        # Atualiza a imagem para o frame atual
        # O [self.frame_index] agora é seguro, pois foi resetado se necessário
        current_image = animation_frames[self.frame_index]
        if self.current_direction == 'left':
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image
        self.rect = self.image.get_rect(center=self.rect.center)

        # Lógica para avançar o frame (continua a mesma)
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            if self.is_charging:
                if not self.charge_complete:
                    self.frame_index += 1
                    if self.frame_index >= len(animation_frames) - 1:
                        self.frame_index = len(animation_frames) - 1
                        self.charge_complete = True
            else:
                self.frame_index = (self.frame_index + 1) % len(animation_frames)

    def shoot(self):
        if self.shoot_target_pos:
            new_arrow = Arrow(self.rect.center, self.shoot_target_pos, self.arrow_damage)
            self.groups['all'].add(new_arrow)
            self.groups['arrows'].add(new_arrow)
            self.shoot_target_pos = None  # Limpa o alvo

        # Dentro da classe Player

    def update(self):
            # A lógica de input foi movida para 'handle_events'
            # O update agora só precisa garantir que a animação rode e a posição seja atualizada
            self.animate()
            self.rect.center = self.position