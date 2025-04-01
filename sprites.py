from configuracoes import *

class ColisaoSprite(pygame.sprite.Sprite):
    def __init__(self,pos, tamanho, grupos):
        super().__init__(grupos)
        self.image = pygame.Surface(tamanho)
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
