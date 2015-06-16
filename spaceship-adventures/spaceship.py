import pygame
import bullet

class Spaceship():

    def __init__(self,width,height,x,y,color):
        self.width  = width
        self.height = height
        self.x      = x
        self.y      = y
        self.color  = color
        self.image = pygame.image.load("banana-clip-art-6-spaceship.png")
        return

    def moveLeft(self, dx):
        self.x -= dx
        # check the wall
        if self.x < 0:
            self.x = 0
        return

    def moveRight(self, dx, upper_limit):
        self.x += dx
        # check the wall
        if self.x > upper_limit:
            self.x = upper_limit
        return

    def moveUp(self, dy):
        self.y -= dy
        # check the wall
        if self.y < 0:
            self.y = 0
        return

    def moveDown(self, dy, board_height):
        self.y += dy
        # check the wall
        if self.y > board_height - self.height:
            self.y = board_height - self.height
        return

    def fire(self,width,height,color, direction='normal'):
        return bullet.Bullet(width,height,(self.x + self.width) , (self.y + (self.height /2) - (height/2)),color, direction)
    
    def draw(self, surface):
        #rect = pygame.Rect( self.x, self.y, self.width, self.height )
        #pygame.draw.rect(surface, self.color, rect)
        surface.blit(self.image, (self.x, self.y))
        return
        
