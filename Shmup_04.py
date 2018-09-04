######################################
#
#         ***SHMUP_03***
#
#   01 player sprite and controles
#   02 enemy sprites
#   03 colision (and bullits)
#   04 adding  graphics
#
#####################################
import pygame
import random
from os import path

# path to images
img_dir = path.join(path.dirname(__file__), "img")

# variablen for windows size
WIDTH = 500
HEIGHT = 600
FPS = 60

# define color
WHITE =(255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup_02")
clock = pygame.time.Clock()

#===================================================
# player
class Player (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        # image scaling
        self.image = pygame.transform.scale(player_img, (50, 38))
        # kill black border
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH /2
        self.rect.bottom  = HEIGHT -10
        self.speedx = 0

    def update (self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
                self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        # move
        self.rect.x += self.speedx

        # border controler
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot (self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
#====================================================
# Enymy
class Mob (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3,  3)
        self.speedy = random.randrange(1, 8)

    def update (self):
        # move
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # border controler and give brith
        if self.rect.top > HEIGHT + 10 or self.rect.right < -20 or self.rect.left > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
#======================================================
# Bullets
class Bullet (pygame.sprite.Sprite):
    def __init__ (self,x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
#======================================================
# load all game garaphics
backround = pygame.image.load(path.join(img_dir,"stars.png")).convert()
backround_rect = backround.get_rect()
# player image
player_img = pygame.image.load(path.join(img_dir,"playerShip1_orange.png")).convert()
# meteor
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
# laser
laser_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
#========================================================
# spritecatalog player
all_sprites = pygame.sprite.Group()
# enemy
mobs = pygame.sprite.Group()
# bullets
bullets = pygame.sprite.Group()

# player add
player = Player()
all_sprites.add(player)

# enemy add
for i in range (8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
#=========================================================
# Game loop
running = True
while running:
    # keep loop running in the right speed
    clock.tick(FPS)
    # proces input (events)
    for event in pygame.event.get():
        # check fpr closing the window
        if event.type == pygame.QUIT:
            running = False

        # shoot im up
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update
    all_sprites.update()

    # check to see if a bullet hit a mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # if a mob is shoot up a new one will be allive
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if a mob hit the Player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # draw / render
    screen.fill(BLACK)
    screen.blit(backround, backround_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
