import sys
import pygame


class SimpleAnimation(object):
    """ A simple animation. Scrolls cyclically through a list of
        images, drawing them onto the screen in the same posision.    
    """
    def __init__(self, screen, pos, images, scroll_period, duration=-1):
        """ Create an animation.        
            
            screen: The screen to which the animation will be drawn
            pos: Position on the screen
            images: 
                A list of surface objects to cyclically scroll through
            scroll_period: 
                Scrolling period (in ms)
            duration:
                Duration of the animation (in ms). If -1, the 
                animation will have indefinite duration.
        """
        self.screen = screen
        self.images = images
        self.pos = pos
        self.scroll_period = scroll_period
        self.duration = duration
        
        self.img_ptr = 0
        self.duration_count = 0
        self.scroll_count = 0
        self.active = True
    
    def is_active(self):
        """ An animation is active from the moment of its creation and until the duration has passed.
        """
        return self.active
    
    def update(self, time_passed):
        """ time_passed: The time passed (in ms) since the previous update.
        """
        self.scroll_count += time_passed
        if self.scroll_count > self.scroll_period:
            self.scroll_count -= self.scroll_period
            self.img_ptr = (self.img_ptr + 1) % len(self.images)
        
        if self.duration >= 0:
            self.duration_count += time_passed
            if self.duration_count > self.duration:
                self.active = False

    def draw(self):
        """ Draw the animation onto the screen.
        """
        if self.active:
            cur_img = self.images[self.img_ptr]
            self.draw_rect = cur_img.get_rect().move(self.pos)
            self.screen.blit(cur_img, self.draw_rect)