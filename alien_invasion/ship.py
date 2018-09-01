import pygame
class Ship():
    def __init__(self,ai_settings,screen):
        #initialize the ship an sset ts starting position
        self.screen=screen
        self.ai_settings=ai_settings
        #load the shi image an get its rect
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        #start each ship at teh center bottom of the screen
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right=False
        self.moving_left=False
        #store a decimal value for the ships center

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left>0:
            self.center-=self.ai_settings.ship_speed_factor
        self.rect.centerx=self.center

    def blitme(self):
        #draw the sip at its current location
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        self.center=self.screen_rect.centerx
