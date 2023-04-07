from abc import ABC, abstractmethod
import colors as c
import random
import pygame
import bullet

LOW_SPEED = 6
HIGH_SPEED = 9

class Mob(pygame.sprite.Sprite):
    def __init__(self, image, width, height, ship_width, ship_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (ship_width, ship_height))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #self.rect.x = random.randrange(width - self.rect.width)
        self.rect.centerx = width
        self.rect.y = random.randrange(0+self.radius, height-self.radius)
        #self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(LOW_SPEED, HIGH_SPEED)
        self.width = width
        self.height = height
        self.score = 10

    def update(self):
        self.rect.x -= self.speedx
        #self.rect.y = self.speedy
        if self.rect.x < 0:
            Mob.kill(self)


    def shoot(self, all_sprites, bullets, now, image):
        pass

class BouncingMob(pygame.sprite.Sprite):
    def __init__(self, image, width, height, ship_width, ship_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(self.image, (ship_width, ship_height))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, c.RED, self.rect.center, self.radius)
        self.rect.centerx = width
        self.rect.y = random.randrange(0 + self.radius, height - self.radius)
        self.speedy = random.randrange(-LOW_SPEED, HIGH_SPEED)
        self.speedx =  HIGH_SPEED
        self.width = width
        self.height = height
        self.score = 30

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > self.height or self.rect.top <0:
            self.speedy*=(-1)
            self.speedx+=random.randrange(int(LOW_SPEED*.5), int(HIGH_SPEED*.5))

        if self.rect.x < 0:
            BouncingMob.kill(self)



    def shoot(self, all_sprites, bullets, now, image):
        pass

class ShootingMob(pygame.sprite.Sprite):
    def __init__(self, image, width, height, ship_width, ship_height, time_get_ticks):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (ship_width, ship_height))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #self.rect.x = random.randrange(width - self.rect.width)
        self.rect.centerx = width
        self.rect.y = random.randrange(0+self.radius, height-self.radius)
        #self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(LOW_SPEED, HIGH_SPEED)
        self.width = width
        self.height = height
        self.last_shot = time_get_ticks
        self.shoot_delay = 750
        self.score=20

    def update(self):
        self.rect.x -= self.speedx
        #self.rect.y = self.speedy
        if self.rect.x < 0:
            Mob.kill(self)

    def shoot(self, all_sprites, bullets, now, image):
        # now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            ebullet = bullet.Bullet(self.rect.left, self.rect.centery, image, True, 10 )
            all_sprites.add(ebullet)
            bullets.add(ebullet)