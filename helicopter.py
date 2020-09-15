#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random

class Bullet:
    def __init__(self, screen, positionX, positionY, speed):
        self.speed = speed
        self.X=positionX
        self.Y=positionY
        self.screen=screen
    def move(self):
        self.X += self.speed
        
    def draw(self):
        self.rect= pygame.Rect(self.X+65, self.Y+28, 5, 5)
        pygame.draw.rect(self.screen, (0, 0, 128), self.rect)

class Bomber:
    def __init__(self, screen, positionX, positionY, speed):
        self.speed = speed
        self.X=positionX
        self.Y=positionY
        self.screen=screen
    def move(self):
        self.Y += self.speed
        
    def draw(self):
        self.rect= pygame.Rect(self.X+65, self.Y+28, 5, 5)
        pygame.draw.rect(self.screen, (0, 0, 128), self.rect)
        
class Helicopter:
    def __init__(self):
        
        self.CONST_MAX_INERCIA=10 
        self.CONST_incremento_inerciaY=0.01
        self.CONST_incremento_inerciaX=0.01
        self.CONST_GRAVITY=0
        self.JUMP_VELOCITY=8
        self.bullet_speed=5
        self.bomber_speed=4
        self.screen = pygame.display.set_mode((400, 708))
        self.helicopter = pygame.Rect(30, 25, 50, 50)
        
        self.bullets =[]
        self.bombers = []
        self.background = pygame.image.load("assets/background.png").convert()
        self.helicopterSprites = [pygame.image.load("assets/helicopter/helicopter_1.png").convert_alpha(),
                            pygame.image.load("assets/helicopter/helicopter_2.png").convert_alpha(),
                            pygame.image.load("assets/helicopter/helicopter_3.png").convert_alpha(),
                            pygame.image.load("assets/helicopter/helicopter_4.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
                            
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.posY = 350
        self.posX = 200
        self.jump = 0
        self.jumpSpeed = self.JUMP_VELOCITY
        self.gravity = self.CONST_GRAVITY
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.inerciaY=0
        self.inerciaX=0
        
        
    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def helicopterUpdate(self):
        
        if (self.inerciaY <-self.CONST_MAX_INERCIA):
            self.inerciaY=-self.CONST_MAX_INERCIA
        if (self.inerciaY >self.CONST_MAX_INERCIA):
            self.inerciaY=self.CONST_MAX_INERCIA
        
        if (self.inerciaX <-self.CONST_MAX_INERCIA):
            self.inerciaX=-self.CONST_MAX_INERCIA
        if (self.inerciaX >self.CONST_MAX_INERCIA):
            self.inerciaX=self.CONST_MAX_INERCIA
            
        if (self.inerciaY!=0):
            if (self.inerciaY<0):
                self.inerciaY+=self.CONST_incremento_inerciaY
            if (self.inerciaY>0):
                self.inerciaY-=self.CONST_incremento_inerciaY
        
        if (self.inerciaX!=0):
            if (self.inerciaX<0):
                self.inerciaX+=self.CONST_incremento_inerciaX
            if (self.inerciaX>0):
                self.inerciaX-=self.CONST_incremento_inerciaX
                
        self.posY += self.inerciaY  
        self.posX += self.inerciaX
        
        self.helicopter[0] = self.posX
        self.helicopter[1] = self.posY
        
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        
        if upRect.colliderect(self.helicopter):
            self.dead = True
        if downRect.colliderect(self.helicopter):
            self.dead = True
        if not 0 < self.helicopter[1] < 720:
            self.helicopter[1] = 50
            self.helicopterY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = self.CONST_GRAVITY
            
    def shootBullet(self):
        new_bullet = Bullet( self.screen, self.posX,self.posY, self.bullet_speed)
        self.bullets.append(new_bullet)
        
    def shootBomber(self):
        new_bomber = Bomber( self.screen, self.posX,self.posY, self.bomber_speed)
        self.bombers.append(new_bomber)
    
    def pintarMarcador(self): 
        self.screen.blit(self.font.render(str(self.counter),
                                     -1,
                                     (255, 255, 255)),
                        (200, 50))
              
    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                 
                if event.type == pygame.KEYDOWN:
                    print("X:",self.posX)
                    print("Y:",self.posY)
                    if event.key == pygame.K_UP:
                        print("UP")
                        self.inerciaY=self.inerciaY-1
                        print("inercia:",self.inerciaY)
                        
                    if event.key == pygame.K_DOWN:
                        print("DOWN")
                        self.inerciaY=self.inerciaY+1
                        
                    if event.key == pygame.K_LEFT:
                        print("K_LEFT")
                        self.inerciaX=self.inerciaX-1
                        print("inerciaX:",self.inerciaX)
                        
                    if event.key == pygame.K_RIGHT:
                        print("K_RIGHT")
                        self.inerciaX=self.inerciaX+1
                        
                    if event.key == pygame.K_SPACE:
                        print("K_SPACE")
                        self.shootBullet()
                        
                    if event.key == pygame.K_b:
                        print("K_b")
                        self.shootBomber()
       
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            
            self.pintarMarcador()
            
            if self.dead:
                self.sprite = 4
                
            self.sprite = (self.sprite +1 )%4
            self.screen.blit(self.helicopterSprites[self.sprite], (self.posX, self.posY))
            
            self.helicopterUpdate()
            
            for bullet in self.bullets:
                bullet.move()
                bullet.draw()
            
            for bomber in self.bombers:
                bomber.move()
                bomber.draw()            
            pygame.display.update()

if __name__ == "__main__":
    Helicopter().run()