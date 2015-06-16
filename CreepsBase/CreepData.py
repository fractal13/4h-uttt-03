import pygame
import pygame.mixer
import os, sys, random
from creep import Creep
from random import randint, choice

class CreepData():
    def __init__(self, width, height, cell_size, frame_rate):
        self.width      = width       # in cells
        self.height     = height      # in cells
        self.cell_size  = cell_size   # in pixels per cell
        self.frame_rate = frame_rate  # in desired frames per second
        print " This is my game."
        self.font_height_small  = 12
        self.font_height_medium = 8
        self.font_height_large = 18
        self.font_small = pygame.font.SysFont("jokerman",self.font_height_small)
        self.font_medium = pygame.font.SysFont("goudystout",self.font_height_medium)
        self.font_large = pygame.font.SysFont("jokerman", self.font_height_large)
        self.text_color = (82,227,220)
        self.background_color = (250, 92, 132)
        self.num_creeps = 5
        self.time_passed = 0

        # create a list of the creep images and their associated movement speeds
        self.CREEP_TYPES = (
            (os.path.join("images","partymanatee.png"), .08),  #HIGHER NUMBERS RESULT IN FASTER CREEPS
            (os.path.join("images","duck.png"), .08),
            (os.path.join("images","charm.png"), 2),
            (os.path.join("images","donut.png"), .08))

        # Define the image to use as your background tile image
        self.BG_TILE_IMG = pygame.image.load(os.path.join("images","brick_tile.png")).convert_alpha()

        # Define the size and location of the playing field (x, y, width, height)
        self.PLAYING_FIELD_RECT = pygame.Rect(10, 20, 450, 360)

        # set up data
        # define the size and location of the message board rectangle
        self.MESSAGE_BOARD_RECT = pygame.Rect(
                int(self.PLAYING_FIELD_RECT.topright[0])+9,
                self.PLAYING_FIELD_RECT.y, 
                (self.width*self.cell_size)-self.PLAYING_FIELD_RECT.topright[0]-14, 
                100)

        # Initialize the sound mixer and set it up to be ready to play the background music
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.game_music = "background.ogg"
        pygame.mixer.music.load(os.path.join("sounds", self.game_music))

        self.newGame()

    def newGame(self):
        self.creeps = pygame.sprite.Group()
        for i in range(self.num_creeps):
            creep_image = choice(self.CREEP_TYPES)          # SELECTS A RANDOM IMAGE FOR THE CREEP
            start_position_x = random.randrange(0, self.width*self.cell_size)
            start_position_y = random.randrange(0, self.height*self.cell_size)
            start_direction_x = choice([-1, 1])
            start_direction_y = choice([-1, 1])
            c = Creep(
                creep_image[0], 
                (start_position_x,start_position_y),
                (start_direction_x, start_direction_y),
                creep_image[1],
            self.PLAYING_FIELD_RECT)
            self.creeps.add(c)
            self.paused = False
            pygame.mixer.music.play(-1) # play and loop the background music

        return
    
    def evolve(self, keys, newkeys, buttons, newbuttons, mouse_position):
        # Check for button presses
        if pygame.K_q in newkeys:                               #Q to QUIT
            quit_event = pygame.event.Event(pygame.QUIT, {})
            pygame.event.post(quit_event)
        elif pygame.K_SPACE in newkeys:                         #SPACEBAR TO PAUSE
            self.paused = not self.paused
        elif pygame.K_r in newkeys:                             #R to RESTART
            self.newGame()

        if self.paused:
            return
        # If the mouse button was pressed, check to see if any creeps were clicked on

        # If all the creeps are dead, you won!
        if len(self.creeps) == 0:
            return

        if 1 in newbuttons:
            for creep in self.creeps:
                creep.mouse_click_event(mouse_position)
        # Update all the creeps
        for creep in self.creeps:
            creep.evolve((1000/self.frame_rate))
     
    def draw(self, surface):
        # Draw background
        rect = pygame.Rect(0, 0, self.width*self.cell_size, self.height*self.cell_size)
        surface.fill(self.background_color, rect)

        # Add a tiled background image
        self.draw_tiled_background(surface, self.BG_TILE_IMG)

        # Draw a section in the middle of the screen to use as our playing field
        playing_field_background_color = (247, 67, 112)           #SELECT A COLOR FOR THE PLAYING FIELD
        playing_field_border_width = 4                          #PICK A SIZE FOR THE PLAYING FIELD BORDER
        playingfield_border_color = pygame.Color('purple')       #PICK A COLOR FOR THE PLAYING FIELD BORDER
        self.draw_bordered_box(surface, self.PLAYING_FIELD_RECT, playing_field_background_color, playing_field_border_width, playingfield_border_color)

        # Draw all the creeps
        # Congratulate the player for winning the game
        if len(self.creeps) == 0:
            self.drawTextCenter("Congratulations!", surface, self.PLAYING_FIELD_RECT.center[0], self.PLAYING_FIELD_RECT.center[1]-(self.font_large.get_height()*2), self.font_large)
            self.drawTextCenter("you have killed all the whales!", surface, self.PLAYING_FIELD_RECT.center[0], self.PLAYING_FIELD_RECT.center[1]-(self.font_large.get_height()-5), self.font_large)
            self.drawTextCenter("Press 'q' to Quit, or 'r' to Restart", surface, self.PLAYING_FIELD_RECT.center[0], self.PLAYING_FIELD_RECT.center[1]+15, self.font_medium)
            return

        for c in self.creeps:
        
            c.draw(surface)
        # Draw the message board
        number_of_creeps = len(self.creeps)
        self.draw_message_board(surface, self.MESSAGE_BOARD_RECT, pygame.Color(101, 23, 235), ["Thingy Count: "+str(number_of_creeps), " ", "       Bailee ", "    is awesome!"])


    def drawTextLeft(self, text, surface, x, y, font):
        textobj = font.render(text, 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        return
    
    def drawTextCenter(self, text, surface, x, y, font):
        textobj = font.render(text, 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
        return

    def draw_tiled_background(self, surface, tile_image):
        # Fill the entire screen up with our tile image
        img_rect = tile_image.get_rect()                        #GET THE SIZE OF THE TILE
        nrows = int(surface.get_height() / img_rect.height) + 1 #DETERMINE HOW MANY ROWS OF TILES WE NEED
        ncols = int(surface.get_width() / img_rect.width) + 1   #DETERMINE HOW MANY COLUMNS OF TILES WE NEED
        # Loop over the rows and columns and draw the tiles
        for y in range(nrows):
            for x in range(ncols):
                img_rect.topleft = (x * img_rect.width, y * img_rect.height)
                surface.blit(tile_image, img_rect)
    def draw_bordered_box(self, surface, box_rect, box_color, border_width=0, border_color=pygame.Color('black')):
        if border_width:
            border_rect = pygame.Rect(box_rect.left - border_width,
                            box_rect.top - border_width,
                            box_rect.width + border_width * 2,
                            box_rect.height + border_width * 2)
            pygame.draw.rect(surface, border_color, border_rect)
        pygame.draw.rect(surface, box_color, box_rect)

    def draw_message_board(self, surface, box_rect, box_color, messages = []):
        self.draw_bordered_box(surface, box_rect, box_color)
        line_height = 0
        for m in messages:
            self.drawTextLeft(m, surface, box_rect.topleft[0]+2, box_rect.y+2+line_height, self.font_medium)
            line_height += self.font_medium.get_height()+2



