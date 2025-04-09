import pygame
from configuracoes import *
from os.path import join

class Monstros(pygame.sprite.Sprite): 
    def __init__(self, pos, *groups, alvo, velocidade, vida, nome, colisao_sprites, limites_mapa):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images', 'enemys', nome, '0.png')).convert_alpha()
        self.rect =  self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(0,0)
        self.direcao = pygame.Vector2()
        self.velocidade = velocidade
        self.vida = vida
        self.alvo = alvo
        self.colisao_sprites = colisao_sprites
        self.limites_mapa = limites_mapa

    def seguir_alvo(self):
        vetor_para_player = pygame.Vector2(self.alvo.hitbox_rect.center) - pygame.Vector2(self.hitbox_rect.center)
        distancia = vetor_para_player.length()

        if distancia > 80:
            self.direcao = vetor_para_player.normalize()
        elif distancia < 60:
            self.direcao = -vetor_para_player.normalize()  # recua um pouco
        else:
            self.direcao = pygame.Vector2(0, 0)


    def movimentar(self, dt):
        self.hitbox_rect.x += self.direcao.x * self.velocidade * dt
        self.colisao('horizontal')
        self.hitbox_rect.y += self.direcao.y * self.velocidade * dt
        self.colisao('vertical')

        # Limita o monstro dentro do mapa
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
            if sprite == self:
                continue  # ignora colisão com ele mesmo

            if sprite.rect.colliderect(self.hitbox_rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direcao.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direcao.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direcao.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top


    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()

    def update(self, dt):
        self.seguir_alvo()
        self.movimentar(dt)


class Galega(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 5, vida = 2, nome = 'galega', colisao_sprites = colisao_sprites, limites_mapa = limites_mapa)

class Perna(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 7, vida = 2, nome = 'perna', colisao_sprites = colisao_sprites, limites_mapa = limites_mapa)

class Monstro3(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 4, vida = 2, nome = 'bilisome', colisao_sprites = colisao_sprites, limites_mapa = limites_mapa)
