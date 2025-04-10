from configuracoes import *
from player import Player, Pet
from sprites import *
from grupos import TodosSprites
from os.path import join
from random import randint
from pygame.math import Vector2
from arma import *
from monstros import Galega, Perna, Lobisomem, Zepilantra
from horario import Horario


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela_interface = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Cabloquinho")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.horario = Horario()

        # Vida
        self.imagem_vida = pygame.image.load(join('images', 'drops', 'vida_coletavel.png')).convert_alpha()
        self.imagem_vida = pygame.transform.scale(self.imagem_vida, (30, 30))
        self.vida_jogador = 3  # começa com 3 vidas

        # Grupos
        self.todos_sprites = TodosSprites()
        self.colisao_sprites = pygame.sprite.Group()
        self.monstros = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        # HUD
        self.imagem_municao = pygame.image.load(join('images', 'drops', 'projetil_coletavel.png')).convert_alpha()
        self.imagem_municao = pygame.transform.scale(self.imagem_municao, (38, 38))
        self.fonte = pygame.font.SysFont("Comic Sans MS", 20)

        self.carregar_cenario()

    def carregar_cenario(self):
        # Background grande
        self.fundo = pygame.image.load(join('images', 'Background.jpg')).convert()
        self.fundo = pygame.transform.scale(self.fundo, (1600, 1200))

        bg_width, bg_height = self.fundo.get_size()
        self.player = Player((400, 300), self.todos_sprites, self.colisao_sprites, (bg_width, bg_height))
        self.player.grupos = {
            'todos_sprites': self.todos_sprites,
            'coletaveis': self.coletaveis
        }
        self.player.jogo = self  # necessário para DropVida acessar vida_jogador

        self.pet = Pet(self.player, self.todos_sprites)
        self.arma = Arma(self.player, self.todos_sprites, self.monstros)
        self.player.arma = self.arma

        # Monstros
        for i in range(3):
            for classe in (Galega, Perna, Lobisomem, Zepilantra):
                x, y = randint(100, 1500), randint(100, 1100)
                classe((x, y), self.todos_sprites, self.monstros,
                alvo=self.player,
                horario=self.horario,
                colisao_sprites=self.colisao_sprites,
                limites_mapa=(bg_width, bg_height),
                groups_dict={
                    'todos_sprites': self.todos_sprites,
                    'coletaveis': self.coletaveis
                })


    def desenhar_hud_municao(self, tela):
        pos_x, pos_y = 5, 40
        tela.blit(self.imagem_municao, (pos_x, pos_y))
        texto_municao = self.fonte.render(f'{self.player.arma.municao}', True, (255, 255, 255))
        tela.blit(texto_municao, (pos_x + 35, pos_y + 5))

    def desenhar_hud_vida(self, tela):
        pos_x, pos_y = 5, 90
        colunas = 3
        for i in range(self.vida_jogador):
            linha = i // colunas
            coluna = i % colunas
            x = pos_x + coluna * 35
            y = pos_y + linha * 35
            tela.blit(self.imagem_vida, (x, y))

    def game_over(self):
        fonte_grande = pygame.font.SysFont("Comic Sans MS", 60)
        fonte_pequena = pygame.font.SysFont("Comic Sans MS", 28)

        texto_game_over = fonte_grande.render("Game Over", True, (255, 0, 0))
        texto_clique = fonte_pequena.render("Clique com o mouse para reiniciar", True, (255, 255, 255))

        rect_game_over = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40))
        rect_clique = texto_clique.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))

        esperando = True
        while esperando:
            self.tela_interface.fill((0, 0, 0))
            self.tela_interface.blit(texto_game_over, rect_game_over)
            self.tela_interface.blit(texto_clique, rect_clique)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
                    self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.vida_jogador = 3
        self.todos_sprites.empty()
        self.colisao_sprites.empty()
        self.monstros.empty()
        self.coletaveis.empty()
        self.carregar_cenario()

    def rodar(self):
        while self.rodando:
            dt = self.relogio.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            self.todos_sprites.update(dt)
            self.horario.atualizar()

            # Verifica dano do jogador por toque em monstros
            if pygame.sprite.spritecollide(self.player, self.monstros, dokill=False):
                self.vida_jogador -= 1
                pygame.time.delay(300)
                if self.vida_jogador <= 0:
                    self.game_over()

            # Câmera: centraliza o player
            offset_x = self.player.rect.centerx - LARGURA_TELA // 2
            offset_y = self.player.rect.centery - ALTURA_TELA // 2

            # Limites do background
            bg_width, bg_height = self.fundo.get_size()
            offset_x = max(0, min(offset_x, bg_width - LARGURA_TELA))
            offset_y = max(0, min(offset_y, bg_height - ALTURA_TELA))
            offset = pygame.Vector2(offset_x, offset_y)

            self.arma.update(offset)

            # Desenha background com offset
            self.tela_interface.blit(self.fundo, (-offset.x, -offset.y))

            # Desenha sprites com offset
            for sprite in self.todos_sprites:
                self.tela_interface.blit(sprite.image, sprite.rect.topleft - offset)

            self.horario.aplicar_filtro(self.tela_interface)
            self.horario.desenhar_hora(self.tela_interface)
            self.desenhar_hud_municao(self.tela_interface)
            self.desenhar_hud_vida(self.tela_interface)

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
