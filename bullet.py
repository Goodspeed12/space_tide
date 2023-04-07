import pygame
import colors as c
import random as r

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img, enemy, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.left = x
        self.speedx = speed
        if enemy:
            self.speedx*=(-1)

    def update(self):
        self.rect.x += self.speedx
        #czasami randomowo zawirowania

        # kill if it moves off the top of the screen
        if self.rect.right > 1024:
            self.kill()