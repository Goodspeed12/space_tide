import pygame
import colors as c
from bullet import Bullet
from os import path

img_dir = path.join(path.dirname(__file__), 'images')
player_img = pygame.image.load(path.join(img_dir, "PlayerBlaster.png"))


class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, width, height, ship_width, ship_height, top_right, time_get_ticks):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.image = pygame.transform.scale(player_img, (ship_width, ship_height))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = 0
        self.rect.bottom = height / 2
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = time_get_ticks
        self.lives = 3
        self.hidden = False
        self.hide_timer = time_get_ticks
        self.width = width
        self.height = height
        self.top_right = top_right
        self.quantum_bombs = 3

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10

        if keystate[pygame.K_UP]:
            self.speedy = -10
        if keystate[pygame.K_DOWN]:
            self.speedy = 10

        self.rect.x += self.speedx

        # nowe
        self.rect.y += self.speedy

        # ograniczenia w poruszaniu sie po mapie
        if self.rect.right > self.width * self.top_right:
            self.rect.right = self.width * self.top_right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, all_sprites, bullets, now):
        #now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery, player_img, False, 40)
            all_sprites.add(bullet)
            bullets.add(bullet)
