from configuracoes import *

class TodosSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_interface = pygame.display.get_surface()
        self.offset= pygame.Vector2()
    
    def draw(self,encontra_pos):
        self.offset.x = -(encontra_pos[0] - LARGURA_TELA/2)
        self.offset.y = -(encontra_pos[1] - ALTURA_TELA/2)
        for sprite in self:
            self.display_interface.blit(sprite.image, sprite.rect.topleft+ self.offset)
