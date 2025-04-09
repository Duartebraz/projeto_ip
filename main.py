from configuracoes import *
from player import Player
from sprites import *
from grupos import TodosSprites
from os.path import join
from random import randint
from arma import *
from pygame.math import Vector2
from monstros import Galega, Perna, Monstro3

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela_interface = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Cabloquinho")
        self.relogio = pygame.time.Clock()
        self.rodando = True

        # Grupos
        self.todos_sprites = TodosSprites()
        self.colisao_sprites = pygame.sprite.Group()

        # Background grande
        self.fundo = pygame.image.load(join('images', 'Background.jpg')).convert()
        self.fundo = pygame.transform.scale(self.fundo, (1600, 1200))  

        # Sprites
        bg_width, bg_height = self.fundo.get_size()
        self.player = Player((400, 300), self.todos_sprites, self.colisao_sprites, (bg_width, bg_height))
        self.arma = Arma(self.player, self.todos_sprites)

        for i in range(15):
            x, y = randint(0, 1600), randint(0, 1200)
            ColisaoSprite((x, y), (self.todos_sprites, self.colisao_sprites))

        self.monstros = pygame.sprite.Group()

        x, y = randint(100, 1500), randint(100, 1100)

        Galega((x, y), self.todos_sprites, self.monstros, alvo=self.player, colisao_sprites=self.colisao_sprites.sprites() + self.monstros.sprites(), limites_mapa=(bg_width, bg_height))

        Perna((x, y), self.todos_sprites, self.monstros, alvo=self.player, colisao_sprites=self.colisao_sprites.sprites() + self.monstros.sprites(), limites_mapa=(bg_width, bg_height))
            
        Monstro3((x, y), self.todos_sprites, self.monstros, alvo=self.player, colisao_sprites=self.colisao_sprites.sprites() + self.monstros.sprites(), limites_mapa=(bg_width, bg_height))
    
    def rodar(self):
        while self.rodando:
            dt = self.relogio.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            # Atualiza lógica
            self.todos_sprites.update(dt)

            # Câmera: centraliza o player
            offset_x = self.player.rect.centerx - LARGURA_TELA // 6
            offset_y = self.player.rect.centery - ALTURA_TELA // 6
            

            # Limites do background
            bg_width, bg_height = self.fundo.get_size()

            # Limita o offset para não mostrar fora da imagem
            offset_x = max(0, min(offset_x, bg_width - LARGURA_TELA))
            offset_y = max(0, min(offset_y, bg_height - ALTURA_TELA))
            offset = pygame.Vector2(offset_x, offset_y)
            self.arma.update(offset)
            # Desenha background com offset
            self.tela_interface.blit(self.fundo, (-offset.x, -offset.y))

            # Desenha sprites com offset
            for sprite in self.todos_sprites:
                self.tela_interface.blit(sprite.image, sprite.rect.topleft - offset)

            pygame.display.update()

        pygame.quit()



if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
