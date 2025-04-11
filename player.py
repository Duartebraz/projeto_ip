from configuracoes import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, colisao_sprites, limites_mapa):
        super().__init__(grupos)
        
        # Configurações de animação
        self.animations = self.load_animations()
        self.status = 'down'  # Direção inicial
        self.frame_index = 0
        self.animation_speed = 0.15
        self.last_update = pygame.time.get_ticks()
        
        # Configurações de imagem
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)

        # Movimento
        self.direcao = pygame.Vector2()
        self.velocidade = 5
        self.colisao_sprites = colisao_sprites
        self.limites_mapa = limites_mapa

    def load_animations(self):
        """Carrega todas as animações do jogador"""
        animations = {}
        directions = ['up', 'down', 'left', 'right']
        
        for direction in directions:
            animations[direction] = []
            path = join('images', 'player', direction)
            
            # Verifica quantos frames existem (0.png, 1.png, etc.)
            frame_count = 0
            while os.path.exists(join(path, f'{frame_count}.png')):
                img = pygame.image.load(join(path, f'{frame_count}.png')).convert_alpha()
                animations[direction].append(img)
                frame_count += 1
                
            # Se não encontrou frames, cria um placeholder
            if frame_count == 0:
                surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                color = {
                    'right': (255, 0, 0),
                    'left': (0, 255, 0),
                    'up': (0, 0, 255),
                    'down': (255, 255, 0)
                }[direction]
                pygame.draw.rect(surf, color, (0, 0, 32, 32))
                animations[direction].append(surf)
                
        return animations

    def entradas(self):
        teclas = pygame.key.get_pressed()
        
        # Reset da direção
        old_direction = self.direcao.copy()
        self.direcao.x = int(teclas[pygame.K_d]) - int(teclas[pygame.K_a])
        self.direcao.y = int(teclas[pygame.K_s]) - int(teclas[pygame.K_w])
        
        # Atualiza status apenas se a direção mudou
        if self.direcao.x > 0:
            self.status = 'right'
        elif self.direcao.x < 0:
            self.status = 'left'
        elif self.direcao.y > 0:
            self.status = 'down'
        elif self.direcao.y < 0:
            self.status = 'up'
            
        self.direcao = self.direcao.normalize() if self.direcao else self.direcao

    def animate(self):
        """Atualiza a animação do personagem"""
        now = pygame.time.get_ticks()
        
        #Só anima se o personagem estiver se movendo
        if self.direcao.magnitude() > 0:
            if now - self.last_update > self.animation_speed * 1000:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.status])
                self.image = self.animations[self.status][self.frame_index]
                self.image = pygame.transform.scale(self.image, (50, 50))
        else:
            # Mantém o primeiro frame quando parado
            self.frame_index = 0
            self.image = self.animations[self.status][self.frame_index]
            self.image = pygame.transform.scale(self.image, (50, 50))

    def movimentacao(self, dt):
        self.hitbox_rect.x += self.direcao.x * self.velocidade
        self.colisao('horizontal')
        self.hitbox_rect.y += self.direcao.y * self.velocidade
        self.colisao('vertical')

        # Limita o player dentro do mapa
        mapa_largura, mapa_altura = self.limites_mapa
        if self.hitbox_rect.left < 0:
            self.hitbox_rect.left = 0
        if self.hitbox_rect.top < 0:
            self.hitbox_rect.top = 0
        if self.hitbox_rect.right > mapa_largura:
            self.hitbox_rect.right = mapa_largura
        if self.hitbox_rect.bottom > mapa_altura:
            self.hitbox_rect.bottom = mapa_altura

        self.rect.center = self.hitbox_rect.center

    def colisao(self, direcao):
        for sprite in self.colisao_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direcao.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direcao.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direcao.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def levar_dano(self, dano):
        agora = pygame.time.get_ticks()
        if not hasattr(self, 'ultimo_dano'):
            self.ultimo_dano = 0
        if agora - self.ultimo_dano > 300:  # 1 segundo de cooldown
            self.jogo.vida_jogador -= dano
            print(f"Levou {dano} de dano! Vida atual: {self.jogo.vida_jogador}")
            self.ultimo_dano = agora

        if self.jogo.vida_jogador <= 0:
            self.jogo.game_over()


    def update(self, dt):
        self.entradas()
        self.movimentacao(dt)
        self.animate()


        
class Pet(pygame.sprite.Sprite):
    def __init__(self, player, grupos):
        super().__init__(grupos)
        self.player = player
        self.load_frames()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.last_update = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=self.get_follow_position())

    def load_frames(self):
        """Carrega os frames de animação do pet"""
        path = os.path.join('images', 'player', 'chico')
        self.frames = []
        i = 0
        while os.path.exists(os.path.join(path, f'{i}.png')):
            img = pygame.image.load(os.path.join(path, f'{i}.png')).convert_alpha()
            self.frames.append(img)
            i += 1

        if not self.frames:
            surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 100, 100), (10, 10), 10)
            self.frames.append(surf)

    def get_follow_position(self):
        """Define a posição do pet baseado na posição do player"""
        offset = pygame.Vector2(-40, 20)  # deslocamento em relação ao player
        return self.player.rect.center + offset

    def animate(self):
        """Anima o pet"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self, dt):
        self.animate()
        self.rect.center = self.get_follow_position()
