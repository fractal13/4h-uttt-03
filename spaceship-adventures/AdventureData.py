import pygame
import spaceship
import baddie
import random

class SpaceshipData:

    def __init__(self,width,height,frame_rate):
        pygame.mixer.init()
        self.bang_sound = pygame.mixer.Sound("gumpop.wav")
        self.font = pygame.font.SysFont("Times New Roman",36)
        self.font2 = pygame.font.SysFont("Courier New",20)
        self.frame_rate = frame_rate
        self.text_color = (255,0,0)
        self.width  = width
        self.height = height
        self.upper_limit = self.width/3
        self.spaceship_width = 20
        self.spaceship_height = 10
        self.spaceship = spaceship.Spaceship(self.spaceship_width,self.spaceship_height,0,(self.height / 2) - 10, (255,255,255))
        self.spaceship_speed = 5
        self.bullets = []
        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_color = (255,255,255)
        self.baddies = []
        self.baddie_width = 20
        self.baddie_height = 20
        self.baddie_color = (255,0,0)
        self.kills = 0
        self.score_color = ( 7, 245, 70)
        self.score_x = 10
        self.score_y = 30

        
        return

    def evolve(self, keys, newkeys, buttons, newbuttons, mouse_position):
        if pygame.K_LEFT in keys:
            self.spaceship.moveLeft(self.spaceship_speed)
        if pygame.K_RIGHT in keys:
            self.spaceship.moveRight(self.spaceship_speed,self.upper_limit)
        if pygame.K_UP in keys:
            self.spaceship.moveUp(self.spaceship_speed)
        if pygame.K_DOWN in keys:
            self.spaceship.moveDown(self.spaceship_speed,self.height)

        if pygame.K_SPACE in newkeys:
            self.bullets.append(self.spaceship.fire(self.bullet_width,self.bullet_height,self.bullet_color))
            self.bang_sound.play()

        if random.randint(1, self.frame_rate/2) == 1:
            self.addBaddie()

        live_bullets = []
        live_baddies = []

        if len(self.bullets) > 0 and len(self.baddies) > 0:
            bullet_id = 1
            for bullet in self.bullets:
                bullet.moveBullet()
                bullet.checkBackWall(self.width)
                for baddie in self.baddies:
                    x,y,w,h = baddie.getDimensions()
                    bullet.checkHitBaddie(x,y,w,h)
                    if bullet.getHit():
                        bullet.setAlive(False)
                        baddie.setAlive(False)
                        self.kills = self.kills + 1
                        bullet.hit = False
                    if bullet_id == 1:
                        if baddie.tick(0,0,self.height):
                            live_baddies.append(baddie)
                if bullet.alive:
                    live_bullets.append(bullet)
                bullet_id += 1
                    
        elif len(self.bullets) > 0 and len(self.baddies) < 1:
            for bullet in self.bullets:
                bullet.moveBullet()
                bullet.checkBackWall(self.width)
                if bullet.alive:
                    live_bullets.append(bullet)
                    
        elif len(self.bullets) < 1 and len(self.baddies) > 0:
            for baddie in self.baddies:
               if baddie.tick(0,0,self.height):
                    live_baddies.append(baddie)
        
        else:
            pass
      
        self.bullets = live_bullets
        self.baddies = live_baddies
            
        return

    def addBaddie(self):
        new_baddie = baddie.Baddie( self.baddie_width, self.baddie_height, self.width, random.randint(0,(self.height-self.baddie_height)), self.baddie_color )
        self.baddies.append( new_baddie )
                   
        return

    def draw(self,surface):
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.fill((0,0,0),rect )
        image = pygame.image.load("newandimproved.png")
        surface.blit(image, (0, 0))
        self.spaceship.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        for baddie in self.baddies:
            baddie.draw(surface)
        score_str = "Score: " + str(self.kills)
        self.drawTextLeft(surface, score_str, self.score_color, self.score_x, self.score_y, self.font2)
   
        return

    
    def drawTextLeft(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return

    def drawTextRight(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomright = (x, y)
        surface.blit(textobj, textrect)
        return
