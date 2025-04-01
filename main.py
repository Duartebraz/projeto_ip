from configuracoes import *
from player import Player
from sprites import *

from random import randint

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela_interface = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
        pygame.display.set_caption("jogo cabloco")
        self.relogio = pygame.time.Clock()
        self.rodando = True

        #grupos
        self.todos_sprites = pygame.sprite.Group()
        self.colisao_sprites = pygame.sprite.Group()

        #sprites
        self.player = Player((400,300), self.todos_sprites, self.colisao_sprites)
        for i in range(6):
            x, y = randint( 0, LARGURA_TELA), randint (0, ALTURA_TELA)
            l,a = randint(60,100), randint(50,100)
            ColisaoSprite((x,y),(a,l),(self.todos_sprites,self.colisao_sprites))

    def rodar(self):
        while self.rodando: 
            #dt
            dt = self.relogio.tick(20)

            #loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            #atualizar
            self.todos_sprites.update(dt) 

            #atualizando frames
            self.tela_interface.fill('black')
            self.todos_sprites.draw(self.tela_interface)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    jogo= Jogo()
    jogo.rodar()
    