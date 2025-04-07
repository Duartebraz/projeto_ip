from configuracoes import *
from random import choice, randint
from os.path import join
import pygame
import os

class ColisaoSprite(pygame.sprite.Sprite):
    def __init__(self, pos, grupos):
        super().__init__(grupos)
        
        # Tipos de sprites disponíveis
        self.tipos = ['poste', 'bilisome', 'galega', 'perna']
        self.tipo = choice(self.tipos)
        
        # Configurações de animação
        self.animations = self.load_animations()
        self.frame_index = 0
        self.animation_speed = 0.1 + randint(0, 10) * 0.01  # Velocidade aleatória
        self.last_update = pygame.time.get_ticks()
        
        # Imagem inicial
        self.image = self.animations[self.frame_index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=pos)
        
    def load_animations(self):
        """Carrega todos os frames de animação para este sprite"""
        frames = []
        path = join('images', 'enemys', self.tipo)
        
        # Carrega todos os frames disponíveis (0.png, 1.png, 2.png)
        frame_count = 0
        while os.path.exists(join(path, f'{frame_count}.png')):
            img = pygame.image.load(join(path, f'{frame_count}.png')).convert_alpha()
            frames.append(img)
            frame_count += 1
            
        # Se não encontrou frames, usa um placeholder
        if not frames:
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            pygame.draw.rect(surf, color, (0, 0, 50, 50))
            frames.append(surf)
            
        return frames
    
    def animate(self):
        """Atualiza a animação do sprite"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            self.image = self.animations[self.frame_index]
            self.image = pygame.transform.scale(self.image, (50, 50))
    
    def update(self, dt):
        self.animate()