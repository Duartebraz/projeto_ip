from configuracoes import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, grupos,colisao_sprites):
        super().__init__(grupos)
        self.image = pygame.image.load(join('images','player','down','0.png' )).convert_alpha()
        
        self.rect =  self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(0,0)

        #movimento
        self.direcao = pygame.Vector2()
        self.velocidade = 20
        self.colisao_sprites = colisao_sprites

    def entradas(self):
        teclas = pygame.key.get_pressed()
        self.direcao.x = int(teclas[pygame.K_d])- int(teclas[pygame.K_a])
        self.direcao.y = int(teclas[pygame.K_s])- int(teclas[pygame.K_w])
        self.direcao = self.direcao.normalize() if self.direcao else self.direcao

    def movimentacao(self,dt):
        self.hitbox_rect.x +=self.direcao.x * self.velocidade
        self.colisao('horizontal')
        self.hitbox_rect.y +=self.direcao.y * self.velocidade
        self.colisao('vertical')
        self.rect.center = self.hitbox_rect.center


    def colisao (self, direcao):
        for sprite in self.colisao_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direcao.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direcao.y <0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direcao.y >0: self.hitbox_rect.bottom = sprite.rect.top

    def update(self, dt):
        self.entradas()
        self.movimentacao(dt)