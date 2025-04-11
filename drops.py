import pygame
from os.path import join

class DropProjetil(pygame.sprite.Sprite):
    def __init__(self, pos, jogador, *groups):
        super().__init__(*groups)
        self.jogador = jogador
        self.image = pygame.image.load(join('images', 'drops', 'projetil_coletavel.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-5, -5)

    def update(self, dt=None):
        if self.hitbox_rect.colliderect(self.jogador.hitbox_rect):
            print("Pegou o drop de munição!")
            self.jogador.arma.municao += 7
            self.kill()


class DropVida(pygame.sprite.Sprite):
    def __init__(self, pos, jogador, *groups):
        super().__init__(*groups)
        self.jogador = jogador
        self.image = pygame.image.load(join('images', 'drops', 'vida_coletavel.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-5, -5)

    def update(self, dt=None):
        if self.hitbox_rect.colliderect(self.jogador.hitbox_rect):
            print("Pegou o drop de vida!")
            self.jogador.jogo.vida_jogador += 1
            self.kill()
            

class DropTempo(pygame.sprite.Sprite):
    def __init__(self, pos, jogador, horario, *groups):
        super().__init__(*groups)
        self.jogador = jogador
        self.horario = horario
        self.image = pygame.image.load(join('images', 'drops', 'tempo_coletavel.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-5, -5)

    def update(self, dt=None):
        if self.hitbox_rect.colliderect(self.jogador.hitbox_rect):
            print("Pegou o drop de tempo! Avançou 1 hora.")
            self.horario.avancar_hora(1)
            self.kill()

