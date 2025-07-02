import pygame
import random
from code.Entity import Entity
from code.const import WIN_WIDTH, WIN_HEIGHT


# Adicione esta função auxiliar no topo do seu arquivo Enemy.py
def load_animation_frames(path_prefix, frame_count):
    frames = []
    for i in range(frame_count):
        path = f"{path_prefix}_{i}.png"
        try:
            frames.append(pygame.image.load(path).convert_alpha())
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {path}\n{e}")
    return frames


class Enemy(Entity):
    def __init__(self, position: tuple, player, strength_multiplier: float = 1.0):
        # O super().__init__ agora usa o primeiro frame da animação como placeholder
        super().__init__("wolf", position, './assets/wolf_walk_0.png')

        # --- NOVOS ATRIBUTOS DE ANIMAÇÃO ---
        self.animations = {
            'walk': load_animation_frames('./assets/wolf_walk', 6),
            'attack': load_animation_frames('./assets/wolf_attack', 4)
        }

        self.attack_range = 40  # Raio de ataque em pixels (bem curto)
        self.attack_damage = int(10 * strength_multiplier)
        self.attack_cooldown = 2000  # 2 segundos para poder atacar de novo
        self.last_attack_time = 0

        self.radius = self.rect.width / 2
        self.frame_index = 0
        self.animation_speed = 150  # ms por frame
        self.last_animation_update = pygame.time.get_ticks()

        # Define a imagem inicial e o rect
        self.image = self.animations['walk'][self.frame_index]
        self.rect = self.image.get_rect(center=position)

        # O resto dos seus atributos continua o mesmo
        self.player = player
        self.state = 'wandering'
        # ... (detection_radius, speeds, health, etc.)
        self.detection_radius = 800
        self.chase_speed = random.uniform(1.5, 2.5)
        self.wander_speed = 0.5
        self.wander_direction = self.get_random_wander_direction()
        self.last_wander_change = pygame.time.get_ticks()
        self.wander_interval = random.randint(2000, 4000)
        base_health = 100
        self.health = int(base_health * strength_multiplier)
        self.xp_drop = int(10 * strength_multiplier)
        self.velocity = pygame.math.Vector2(0, 0)

    def get_random_wander_direction(self):
        angle = random.uniform(0, 360)
        return pygame.math.Vector2(1, 0).rotate(angle)

    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_wander_change > self.wander_interval:
            self.last_wander_change = now
            self.wander_interval = random.randint(2000, 4000)
            self.wander_direction = self.get_random_wander_direction()
        self.velocity = self.wander_direction * self.wander_speed

    def chase(self):
        direction = (self.player.position - self.position).normalize()
        self.velocity = direction * self.chase_speed

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.kill()

        # Dentro da classe Enemy

        # Dentro da classe Enemy

    def update(self):
            """O cérebro da IA: decide o que fazer a cada quadro."""
            now = pygame.time.get_ticks()

            if self.health > 0:
                distance_to_player = self.position.distance_to(self.player.position)

                # --- LÓGICA DE TRANSIÇÃO DE ESTADO (com prioridade de ataque) ---
                # 1. Pode atacar? (Está no alcance E o cooldown acabou)
                if distance_to_player < self.attack_range and (now - self.last_attack_time > self.attack_cooldown):
                    self.state = 'attacking'
                    self.frame_index = 0  # Reinicia a animação de ataque
                    self.last_attack_time = now
                # 2. Se não pode atacar, deve perseguir?
                elif distance_to_player < self.detection_radius and self.state != 'attacking':
                    self.state = 'chasing'
                # 3. Se não, apenas vagueia
                elif self.state != 'attacking':
                    self.state = 'wandering'

                # Define a velocidade com base no estado
                if self.state == 'chasing':
                    self.chase()
                elif self.state == 'wandering':
                    self.wander()
                elif self.state == 'attacking':
                    self.velocity = pygame.math.Vector2(0, 0)  # Fica parado para atacar

            else:  # Se está morto, não se move
                self.velocity = pygame.math.Vector2(0, 0)

            # Chama a animação e aplica o movimento
            self.animate()
            self.position += self.velocity
            self.rect.center = self.position

            # A lógica de contenção de tela continua a mesma
            # ...

    def animate(self):
            """Atualiza a imagem e aplica o dano no final da animação de ataque."""
            now = pygame.time.get_ticks()

            # Define qual animação usar com base no estado
            if self.state == 'attacking':
                animation_frames = self.animations['attack']
            else:  # Para 'wandering' e 'chasing', usa a mesma animação de andar
                animation_frames = self.animations['walk']

            # Atualiza a imagem para o frame atual
            self.image = animation_frames[self.frame_index]
            if self.velocity.x > 0:
                self.image = pygame.transform.flip(self.image, True, False)

            # Lógica para avançar o frame
            if now - self.last_animation_update > self.animation_speed:
                self.last_animation_update = now
                self.frame_index += 1

                # Se a animação terminou
                if self.frame_index >= len(animation_frames):
                    # Se era a animação de ATAQUE que acabou
                    if self.state == 'attacking':
                        # Verifica NOVAMENTE se o jogador ainda está no alcance para levar dano
                        if self.position.distance_to(self.player.position) < self.attack_range:
                            self.player.take_damage(self.attack_damage)
                        # Reseta o estado (na próxima volta do update, ele decidirá se persegue ou vagueia)
                        self.state = 'wandering'

                        # Para qualquer animação que termine, reseta o frame_index
                    self.frame_index = 0

            # Atualiza o retângulo
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)