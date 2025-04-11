import pygame
from configuracoes import *
from os.path import join
from random import randint
from drops import DropProjetil, DropVida, DropTempo

class Monstros(pygame.sprite.Sprite): 
    def __init__(self, pos, *groups, alvo, velocidade, vida, nome, 
                colisao_sprites, limites_mapa, groups_dict=None, horario=None):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images', 'enemys', nome, '0.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.direcao = pygame.Vector2()
        self.velocidade = velocidade
        self.vida = vida
        self.alvo = alvo
        self.nome = nome
        self.colisao_sprites = colisao_sprites
        self.limites_mapa = limites_mapa
        self.groups_dict = groups_dict or {}
        self.horario = horario
        self.ultimo_ataque = pygame.time.get_ticks()
        self.cooldown_ataque = 1000
        #isso é para criar um cooldown de ataque na def atacar_alvo

        
    def seguir_alvo(self):
        vetor_para_player = pygame.Vector2(self.alvo.hitbox_rect.center) - pygame.Vector2(self.hitbox_rect.center)
        if vetor_para_player.length() != 0:
            self.direcao = vetor_para_player.normalize()
        else:
            self.direcao = pygame.Vector2()
        """vetor_para_player = pygame.Vector2(self.alvo.hitbox_rect.center) - pygame.Vector2(self.hitbox_rect.center)
        distancia = vetor_para_player.length()"""
        #tirei isso aqui porque quero agora que os inimigos vá pra cima e cole mesmo
        '''if distancia > 80:
            self.direcao = vetor_para_player.normalize()
        elif distancia < 60:
            self.direcao = -vetor_para_player.normalize()
        else:
            self.direcao = pygame.Vector2(0, 0)''' 
        #tirei isso aqui pra tentar resolver o problema dos monstros sem bater por distância

    def atacar_alvo(self):
        agora = pygame.time.get_ticks()
        distancia = pygame.Vector2(self.alvo.hitbox_rect.center).distance_to(self.hitbox_rect.center)
        if self.hitbox_rect.colliderect(self.alvo.hitbox_rect) or distancia <= 10:
            if agora - self.ultimo_ataque >= self.cooldown_ataque:
                if hasattr(self.alvo, 'levar_dano'):
                    self.alvo.levar_dano(1)
                    self.ultimo_ataque = agora


    def movimentar(self, dt):
        self.hitbox_rect.x += self.direcao.x * self.velocidade
        self.colisao('horizontal')
        self.hitbox_rect.y += self.direcao.y * self.velocidade
        self.colisao('vertical')

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
                continue

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
        print(f"{self.nome} levou {dano} de dano. Vida restante: {self.vida}")

        if self.vida <= 0:
            print(f"{self.nome} morreu.")
            if self.nome == 'poste':
                DropProjetil(self.rect.center, self.alvo, self.groups_dict['todos_sprites'], self.groups_dict['coletaveis'])
            elif self.nome == 'galega':
                DropVida(self.rect.center, self.alvo, self.groups_dict['todos_sprites'], self.groups_dict['coletaveis'])
            elif self.nome == 'bilisome':
                DropTempo(self.rect.center, self.alvo, self.horario, self.groups_dict['todos_sprites'], self.groups_dict['coletaveis'])
            self.kill()

    def update(self, dt):
        self.seguir_alvo()
        self.movimentar(dt)
        self.atacar_alvo()


#Classes específicas de monstros:

class Galega(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa, groups_dict=None, horario=None):
        super().__init__(pos, *groups, alvo=alvo, velocidade=randint(1, 2), vida=randint(1, 2),
                        nome='galega', colisao_sprites=colisao_sprites, limites_mapa=limites_mapa,
                        groups_dict=groups_dict, horario=horario)

class Perna(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa, groups_dict=None, horario=None):
        super().__init__(pos, *groups, alvo=alvo, velocidade=randint(1, 3), vida=1,
                        nome='perna', colisao_sprites=colisao_sprites, limites_mapa=limites_mapa,
                        groups_dict=groups_dict, horario=horario)

class Lobisomem(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa, groups_dict=None, horario=None):
        super().__init__(pos, *groups, alvo=alvo, velocidade=randint(1, 2), vida=randint(1, 2),
                        nome='bilisome', colisao_sprites=colisao_sprites, limites_mapa=limites_mapa,
                        groups_dict=groups_dict, horario=horario)

class Zepilantra(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites, limites_mapa, groups_dict=None, horario=None):
        super().__init__(pos, *groups, alvo=alvo, velocidade=randint(1, 2), vida=randint(1, 2),
                        nome='poste', colisao_sprites=colisao_sprites, limites_mapa=limites_mapa,
                        groups_dict=groups_dict, horario=horario)
