#importando propriedades usadas no codigo------------------

import pygame, random
from pygame.locals import *

#Definindo tamanho da janela de jogo----------------------

SCREEN_WIDTH = 800 #Definindo largura
SCREEN_HEIGHT = 800 #Definindo comprimento

#Definindo propriedades dos elementos---------------------
SPEED = 10  #Propriedade Velocidade dos elementos
GRAVITY = 1  #Propriedade gravidade do jogo
GAME_SPEED = 10  #Propriedade Velocidade do jogo

GROUND_WIDTH = 2 * SCREEN_WIDTH #Propriedade de largura do chão
GROUND_HEIGHT = 100 #Propriedade de comprimento do chão

TUBO_WIDTH = 80 #Propriedade de largura do tubo
TUBO_HEIGHT = 500 #Propriedade de comprimento do tubo

TUBO_GAP = 200 #Propriedade de espaçamento entre os tubos

#Definindo uma classe para os tubos----------------------

class Tubo(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('tubo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TUBO_WIDTH,TUBO_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

#Definindo uma classe para o chão----------------------
        
class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_tubos(xpos):
    size = random.randint(100, 300)
    tubo = Tubo(False, xpos, size)
    tubo_inverted = Tubo(True, xpos, SCREEN_HEIGHT - size - TUBO_GAP)
    return (tubo, tubo_inverted)


#Definindo uma classe para o peixe----------------------

class Fish(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluefish1.png').convert_alpha(), 
                       pygame.image.load('bluefish2.png').convert_alpha(), 
                       pygame.image.load('bluefish3.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('bluefish1.png').convert_alpha() 
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED

#Depois de todas as classes definidas, começa o jogo-----

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('background-day.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

fish_group = pygame.sprite.Group()
fish = Fish()
fish_group.add(fish)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

tubo_group = pygame.sprite.Group()
for i in range(2):
    tubos = get_random_tubos(SCREEN_WIDTH * i + 800)
    tubo_group.add(tubos[0])
    tubo_group.add(tubos[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                fish.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(tubo_group.sprites()[0]):
        tubo_group.remove(tubo_group.sprites()[0])
        tubo_group.remove(tubo_group.sprites()[0])

        tubos = get_random_tubos(SCREEN_WIDTH * 2)

        tubo_group.add(tubos[0])
        tubo_group.add(tubos[1])

    fish_group.update()
    ground_group.update()
    tubo_group.update()

    fish_group.draw(screen)
    tubo_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()
    
# Criando condição para acabar o jogo

    if(pygame.sprite.groupcollide(fish_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(fish_group, tubo_group, False, False, pygame.sprite.collide_mask)):
        BACKGROUND = pygame.image.load('gameover.png')
        BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Game over
        input()
        break
        
