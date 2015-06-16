import os, sys
import pygame
from pygame.sprite import Sprite
from random import randint, choice
from math import sin, cos, radians
from vec2d import vec2d
from SimpleAnimation import SimpleAnimation


class Creep(Sprite):
    """ A creep is a sprite that bounces off walls and changes its direction from time to time.
    """
    def __init__(self, img_filename, init_position, init_direction, speed, playing_field_rect):
        Sprite.__init__(self)
        self.speed = speed
        self.PLAYING_FIELD_RECT = playing_field_rect
        
        # base_image holds the original image, positioned to angle 0.
        # the image will be rotated as the game progresses
        self.base_image = pygame.image.load(img_filename).convert_alpha()
        self.image = self.base_image
        
        # A vector specifying the creep's position on the screen
        self.pos = vec2d(init_position)

        # The direction is a normalized vector
        self.direction = vec2d(init_direction).normalized()

        # Start the creep in the ALIVE state
        self.state = Creep.ALIVE

        # The amount of health the creep starts with
        self.health = 15
        
        # When the creep runs out of health, this image is displayed
        self.explosion_img = pygame.image.load(os.path.join("images","explosion1.png")).convert_alpha()
        # To create an animated effect, we will rotate the image back and forth 90 degrees
        self.explosion_images = [self.explosion_img, pygame.transform.rotate(self.explosion_img, 90)]

        # Setup the sound effects
        self.creep_hit_sound = pygame.mixer.Sound(os.path.join("sounds", "creep_hit.ogg"))
        self.creep_explosion_sound = pygame.mixer.Sound(os.path.join("sounds", "creep_explode.ogg"))


    def evolve(self, time_passed):
        """ time_passed: The time passed (in ms) since the previous update.
        """
        if self.state == Creep.ALIVE:
            # Randomly change the creep's direction, based on how
            # long it's been since the last direction change.
            self._change_direction(time_passed)
            
            # Make the creep point in the correct direction.
            # Since our direction vector is in screen coordinates 
            # (i.e. right bottom is 1, 1), and rotate() rotates 
            # counter-clockwise, the angle must be inverted to 
            # work correctly.
            self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
            
            # Compute and apply the displacement to the position 
            # vector. The displacement is a vector, having the angle
            # of self.direction (which is normalized to not affect
            # the magnitude of the displacement)
            #
            displacement = vec2d(    
                self.direction.x * self.speed * time_passed,
                self.direction.y * self.speed * time_passed)

            # Move the creep according to the displacement calculated
            # above.
            self.pos += displacement
            
            # When the image is rotated, its size is changed.
            # We must take the size into account for detecting 
            # collisions with the walls.
            self.image_w, self.image_h = self.image.get_size()
            bounds_rect = self.PLAYING_FIELD_RECT.inflate(
                            -self.image_w, -self.image_h)
            
            if self.pos.x < bounds_rect.left:
                self.pos.x = bounds_rect.left
                self.direction.x *= -1
            elif self.pos.x > bounds_rect.right:
                self.pos.x = bounds_rect.right
                self.direction.x *= -1
            elif self.pos.y < bounds_rect.top:
                self.pos.y = bounds_rect.top
                self.direction.y *= -1
            elif self.pos.y > bounds_rect.bottom:
                self.pos.y = bounds_rect.bottom
                self.direction.y *= -1
        elif self.state == Creep.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.state = Creep.DEAD
                self.kill()
        elif self.state == Creep.DEAD:
            pass

    def draw(self, surface):
        # The creep image is placed at self.pos.
        # To allow for smooth movement even when the creep rotates
        # and the image size changes, its placement is always
        # centered.
        if self.state == Creep.ALIVE and self.health == 0:
            self._explode(surface)
        elif self.state == Creep.ALIVE:
            draw_pos = self.image.get_rect().move(
                self.pos.x - self.image_w / 2, 
                self.pos.y - self.image_h / 2)
            surface.blit(self.image, draw_pos)
            # Draw the health bar (it is 15x4 px)
            health_bar_x = self.pos.x - 7
            health_bar_y = self.pos.y - self.image_h / 2 - 6
            surface.fill(pygame.Color('red'), (health_bar_x, health_bar_y, 15, 4))          #BAD HEALTH
            surface.fill(pygame.Color('green'),(health_bar_x, health_bar_y, self.health, 4))#GOOD HEALTH
        elif self.state == Creep.EXPLODING:
            self.explode_animation.draw()
        elif self.state == Creep.DEAD:
            pass




    def is_alive(self):
        return self.state in (Creep.ALIVE, Creep.EXPLODING)
    
    def mouse_click_event(self, pos):
        # if the creep was clicked, decrease the creep's health
        if self._point_is_inside(vec2d(pos)):
            self.creep_hit_sound.play()
            self._decrease_health(3)
            



    #------------------ PRIVATE PARTS ------------------#
    (ALIVE, EXPLODING, DEAD) = range(3)             #KEEP TRACK OF THE STATE OF THE CREEP
    _counter = 0
    
    def _change_direction(self, time_passed):
        """ Turn by 45 degrees in a random direction once per
            .4 to .5 seconds.
        """
        self._counter += time_passed
        if self._counter > randint(300, 500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0
    def _point_is_inside(self, point):
        """ Is the point (given as a vec2d) inside a solid portion/color of the creep's image?
        """
        img_point = point - vec2d(
            int(self.pos.x - self.image_w / 2),
            int(self.pos.y - self.image_h / 2))

        try:
            pix = self.image.get_at(img_point)
            return pix[3] > 0
        except IndexError:
            return False

    def _decrease_health(self, n):
        """ Decrease the creep's health by n (or to 0, if it's currently less than n)
        """
        self.health = max(0, self.health - n)
    def _explode(self, surface):
        """ Starts the explosion animation that ends the Creep's life.
        """
        self.state = Creep.EXPLODING
        self.creep_explosion_sound.play()
        pos = ( self.pos.x - self.explosion_images[0].get_width() / 2,
                self.pos.y - self.explosion_images[0].get_height() / 2)
        self.explode_animation = SimpleAnimation(surface, pos, self.explosion_images, 100, 300)


